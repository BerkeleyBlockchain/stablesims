""" Keeper Module
    Class-based representation of a keeper in the Maker ecosystem.
    By this, we mean any external agent, not just auction keepers.
    (contains only what is necessary for the simulation)
"""

from uuid import uuid4
import random

from pydss.pymaker.numeric import Wad, Rad, Ray


class Keeper:
    """
    ADDRESS = str
    ilks = dict[str: Token]
    """

    def __init__(self, ilks):
        """ `ilks` must be an array containing a configuration object for each ilk type of the
            following form:
            {"ilk_id": str, "token": Token, "init_balance": float}
        """
        self.ADDRESS = f"keeper-{uuid4().hex}"
        self.ilks = {}
        for ilk in ilks:
            self.ilks[ilk["ilk_id"]] = ilk["token"]
            self.ilks[ilk["ilk_id"]].transferFrom("", self.ADDRESS, ilk["init_balance"])

    def generate_actions_for_timestep(self, t):
        # take into account state["gas"]
        pass


class VaultKeeper(Keeper):
    """
    vat = Vat
    dai_join = DaiJoin
    gem_joins = dict[str: GemJoin]

    urns = dict[int: str]
    num_urns = int

    c_ratios = dict[str: float]
    """

    def __init__(self, vat, dai_join, ilks):
        """ Here, each ilk object in `ilks` must also contain a "gem_join" field with a GemJoin
            object, as well as a "c_ratio" field w/ the keeper's desired collateralization ratio.
        """

        self.vat = vat
        self.dai_join = dai_join
        self.gem_joins = {}
        self.urns = {}
        self.num_urns = 0
        self.c_ratios = {}

        for ilk in ilks:
            self.gem_joins[ilk["ilk_id"]] = ilk["gem_join"]
            self.c_ratios[ilk["ilk_id"]] = ilk["c_ratio"]

        super().__init__(ilks)

    def generate_urn_id(self):
        urn_id = f"urn-{self.num_urns}-{self.ADDRESS}"
        self.num_urns += 1
        return urn_id

    def open_vault(self, ilk_id, dink, dart):
        urn_id = self.generate_urn_id()
        self.urns[urn_id] = ilk_id
        # Lock collateral into the system
        self.gem_joins[ilk_id].join(self.ADDRESS, self.ADDRESS, dink)
        # Create a vault with the locked collateral
        # `vat.gem` and `vat.dai` use the Keeper's address, while `vat.urns` uses `urn_id`
        self.vat.frob(ilk_id, urn_id, self.ADDRESS, self.ADDRESS, dink, dart)

    def close_vault(self, urn_id):
        ilk_id = self.urns[urn_id]
        dink = Wad(0) - self.vat.urns[ilk_id][urn_id]["ink"]
        dart = Wad(0) - self.vat.urns[ilk_id][urn_id]["art"]
        # Zero out the vault, freeing collateral
        self.vat.frob(ilk_id, urn_id, self.ADDRESS, self.ADDRESS, dink, dart)
        # Withdraw freed collateral
        self.gem_joins[ilk_id].exit(self.ADDRESS, self.ADDRESS, Wad(0) - dink)
        del self.urns[urn_id]

    def open_max_vaults(self, actions):
        for ilk_id in self.ilks:
            vat_ilk = self.vat.ilks[ilk_id]
            if self.ilks[ilk_id].balanceOf(self.ADDRESS) > 0 and vat_ilk.spot > Ray(0):
                dink = Wad.from_number(self.ilks[ilk_id].balanceOf(self.ADDRESS))
                dart = Wad.from_number(1 / self.c_ratios[ilk_id]) * vat_ilk.spot * dink
                if dart > Wad(vat_ilk.dust) and Rad(dart * vat_ilk.rate) <= Rad(
                    dink * vat_ilk.spot
                ):
                    actions.append(
                        {
                            "key": "OPEN_VAULT",
                            "keeper": self,
                            "handler": self.open_vault,
                            "args": [ilk_id, dink, dart],
                            "kwargs": {},
                        }
                    )


class NaiveVaultKeeper(VaultKeeper):
    def generate_actions_for_timestep(self, t):
        actions = []
        self.open_max_vaults(actions)
        return actions


class AuctionKeeper(VaultKeeper):
    def find_bids_to_place(self, now, **kwargs):
        raise NotImplementedError

    def run_bidding_model(self, bid, ilk_id, **kwargs):
        raise NotImplementedError

    def place_bid(self, bid_id, price, ilk_id, now, **kwargs):
        raise NotImplementedError

    def find_bids_to_deal(self, now, **kwargs):
        raise NotImplementedError

    def deal_bid(self, bid_id, ilk_id, now, **kwargs):
        raise NotImplementedError


class FlipperKeeper(AuctionKeeper):
    """
    flippers = dict[str: Flipper]
    """

    def __init__(self, vat, dai_join, ilks):
        """ Here, each ilk object in `ilks` must also contain a "flipper" field with a Flipper
            object.
        """

        self.flippers = {}
        for ilk in ilks:
            self.flippers[ilk["ilk_id"]] = ilk["flipper"]

        super().__init__(vat, dai_join, ilks)

    def generate_actions_for_timestep(self, t):
        actions = []
        self.open_max_vaults(actions)
        self.find_and_deal_bids(t, actions)
        self.find_and_place_bids(t, actions)
        return actions

    def find_bids_to_place(self, now, **kwargs):
        """ Must return a dict w/ ilk_ids as keys and lists of bids as values.
        """
        raise NotImplementedError

    def run_bidding_model(self, bid, ilk_id, **kwargs):
        raise NotImplementedError

    def place_bid(self, bid_id, price, ilk_id, now):
        if price > Wad(0):
            flipper = self.flippers[ilk_id]
            bid = flipper.bids[bid_id]

            if bid.bid == bid.tab:
                # Dent phase
                our_lot = Wad(bid.bid / Rad(price))
                if (
                    our_lot * flipper.beg <= bid.lot
                    and our_lot < bid.lot
                    and self.vat.dai.get(self.ADDRESS)
                    and self.vat.dai[self.ADDRESS] >= bid.bid
                ):
                    return {
                        "key": "DENT",
                        "keeper": self,
                        "handler": flipper.dent,
                        "args": [bid_id, self.ADDRESS, our_lot, bid.bid, now],
                        "kwargs": {},
                    }

            else:
                # Tend phase
                our_bid = Rad.min(Rad(bid.lot) * price, bid.tab)
                if (
                    (our_bid >= bid.bid * flipper.beg or our_bid == bid.tab)
                    and our_bid > bid.bid
                    and self.vat.dai.get(self.ADDRESS)
                    and self.vat.dai[self.ADDRESS]
                    >= (our_bid if self.ADDRESS != bid.guy else our_bid - bid.bid)
                ):
                    return {
                        "key": "TEND",
                        "keeper": self,
                        "handler": flipper.tend,
                        "args": [bid_id, self.ADDRESS, bid.lot, our_bid, now],
                        "kwargs": {},
                    }

        return None

    def find_and_place_bids(self, t, actions):
        bids_to_place = self.find_bids_to_place(t)
        for ilk_id in bids_to_place:
            for bid in bids_to_place[ilk_id]:
                stance = self.run_bidding_model(bid, ilk_id)
                action = self.place_bid(bid.id, stance["price"], ilk_id, t)
                if action:
                    actions.append(action)

    def find_bids_to_deal(self, now):
        bids = {}
        for ilk_id in self.ilks:
            bids[ilk_id] = list(
                filter(
                    lambda bid: bid.guy == self.ADDRESS
                    and bid.tic <= now
                    or bid.end <= now,
                    self.flippers[ilk_id].bids.values(),
                )
            )
        return bids

    def deal_bid(self, bid_id, ilk_id, now):
        return {
            "key": "DEAL",
            "keeper": self,
            "handler": self.flippers[ilk_id].deal,
            "args": [bid_id, now],
            "kwargs": {},
        }

    def find_and_deal_bids(self, t, actions):
        bids_to_deal = self.find_bids_to_deal(t)
        for ilk_id in bids_to_deal:
            for bid in bids_to_deal[ilk_id]:
                action = self.deal_bid(bid.id, ilk_id, t)
                if action:
                    actions.append(action)


class NaiveFlipperKeeper(FlipperKeeper):
    def find_bids_to_place(self, now):
        bids = {}
        for ilk_id in self.ilks:
            bids[ilk_id] = list(
                filter(
                    lambda bid: bid.guy != self.ADDRESS
                    and (bid.tic > now or bid.tic == 0)
                    and bid.end > now,
                    self.flippers[ilk_id].bids.values(),
                )
            )
        return bids

    def run_bidding_model(self, bid, ilk_id):
        curr_price = Wad(bid.bid) / bid.lot
        if (
            bid.guy == self.ADDRESS
            or bid.lot == Wad(0)
            or curr_price > Wad(self.vat.ilks[ilk_id].spot)
        ):
            return {"price": Wad(0)}

        if bid.bid == Rad(0):
            return {"price": Wad.from_number(0.05) * Wad(bid.tab / Rad(bid.lot))}

        return {
            "price": curr_price
            * (self.flippers[ilk_id].beg + Wad.from_number(random.uniform(0, 0.15)))
        }


class PatientFlipperKeeper(NaiveFlipperKeeper):
    def __init__(self, vat, dai_join, ilks, other_keepers):
        self.other_keepers = other_keepers
        super().__init__(vat, dai_join, ilks)

    def run_bidding_model(self, bid, ilk_id):
        if bid.tic != 0:
            return {"price": Wad(0)}
        for keeper in self.other_keepers:
            if self.vat.dai.get(keeper.ADDRESS, Rad(0)) >= bid.tab:
                return {"price": Wad(0)}

        return super().run_bidding_model(bid, ilk_id)


class SpotterKeeper(Keeper):
    """
    spotter = Spotter
    """

    def __init__(self, ilks, spotter):
        self.spotter = spotter
        super().__init__(ilks)

    def generate_actions_for_timestep(self, t):
        actions = []
        for ilk_id in self.ilks:
            actions.append(
                {
                    "key": "POKE",
                    "keeper": self,
                    "handler": self.spotter.poke,
                    "args": [ilk_id, t],
                    "kwargs": {},
                }
            )
        return actions


class BiteKeeper(Keeper):
    """
    cat = Cat
    vat = Vat
    """

    def __init__(self, ilks, cat, vat):
        self.cat = cat
        self.vat = vat
        super().__init__(ilks)

    def generate_actions_for_timestep(self, t):
        actions = []
        for ilk_id in self.ilks:
            ilk = self.vat.ilks[ilk_id]
            for urn in self.vat.urns[ilk_id].values():
                if Rad(urn.ink * ilk.spot) < Rad(urn.art * ilk.rate):
                    actions.append(
                        {
                            "key": "BITE",
                            "keeper": self,
                            "handler": self.cat.bite,
                            "args": [ilk_id, urn.ADDRESS, t],
                            "kwargs": {},
                        }
                    )
        return actions
