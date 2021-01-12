""" Keeper Module
    Class-based representation of a keeper in the Maker ecosystem.
    By this, we mean any external agent, not just auction keepers.
    (contains only what is necessary for the simulation)
"""

from uuid import uuid4

from pydss.pymaker.numeric import Wad, Rad


class Keeper:
    ADDRESS = ""

    ilks = {}

    def __init__(self, ilks):
        """ `ilks` must be an array containing a configuration object for each ilk type of the
            following form:
            {"ilk_id": str, "token": Token, "init_balance": float}
        """
        self.ADDRESS = f"keeper-{uuid4().hex}"
        for ilk in ilks:
            self.ilks[ilk["ilk_id"]] = ilk["token"]
            self.ilks[ilk["ilk_id"]].transferFrom("", self.ADDRESS, ilk["init_balance"])

    def execute_actions_for_timestep(self, t):
        pass


class VaultKeeper(Keeper):
    vat = None
    dai_join = None
    gem_joins = {}

    urns = {}
    num_urns = 0

    c_ratios = {}

    def __init__(self, vat, dai_join, ilks):
        """ Here, each ilk object in `ilks` must also contain a "gem_join" field with a GemJoin
            object, as well as a "c_ratio" field w/ the keeper's desired collateralization ratio.
        """

        self.vat = vat
        self.dai_join = dai_join

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


class AuctionKeeper(VaultKeeper):
    def find_bids(self, **kwargs):
        raise NotImplementedError

    def run_bidding_model(self, bid, **kwargs):
        raise NotImplementedError

    def place_bid(self, bid_id, price, now, **kwargs):
        raise NotImplementedError


class FlipperKeeper(AuctionKeeper):

    flippers = {}

    def __init__(self, vat, dai_join, ilks):
        """ Here, each ilk object in `ilks` must also contain a "flipper" field with a Flipper
            object.
        """

        for ilk in ilks:
            self.flippers[ilk["ilk_id"]] = ilk["flipper"]

        super().__init__(vat, dai_join, ilks)

    def execute_actions_for_timestep(self, t):
        actions = []
        if t == 0:
            for ilk_id in self.ilks:
                dink = Wad.from_number(self.ilks[ilk_id].balanceOf(self.ADDRESS))
                dart = (
                    Wad.from_number(1 / self.c_ratios[ilk_id])
                    * self.vat.ilks[ilk_id].spot
                    * dink
                )
                self.open_vault(ilk_id, dink, dart)
                actions.append({"key": "OPEN_VAULT"})
        else:
            bids = self.find_bids()
            for ilk_id in bids:
                for bid in bids[ilk_id]:
                    stance = self.run_bidding_model(bid)
                    action = self.place_bid(bid.id, stance["price"], t, ilk_id)
                    if action:
                        actions.append(action)
        return actions

    def find_bids(self, **kwargs):
        """ Must return a dict w/ ilk_ids as keys and lists of bids as values.
        """
        raise NotImplementedError

    def run_bidding_model(self, bid, **kwargs):
        raise NotImplementedError

    def place_bid(self, bid_id, price, now, ilk_id=""):
        # TODO: Make sure this aligns with the Flipper class

        flipper = self.flippers[ilk_id]
        bid = flipper.bids[bid_id]

        if bid.bid == bid.tab:
            # Dent phase
            our_lot = Wad(bid.bid / Rad(price))
            if (
                our_lot * flipper.beg <= bid.lot
                and our_lot < bid.lot
                and self.vat.dai[self.ADDRESS] >= bid.bid
            ):
                flipper.dent(bid_id, self.ADDRESS, our_lot, bid.bid, now)
                return {"key": "DENT"}

        else:
            # Tend phase
            our_bid = Rad.min(Rad(bid.lot) * price, bid.tab)
            if (
                (our_bid >= bid.bid * flipper.beg or our_bid == bid.tab)
                and our_bid > bid.bid
                and self.vat.dai[self.ADDRESS]
                >= (our_bid if self.ADDRESS != bid.guy else our_bid - bid.bid)
            ):
                flipper.tend(bid_id, self.ADDRESS, bid.lot, our_bid, now)
                return {"key": "TEND"}

        return None


class NaiveFlipperKeeper(FlipperKeeper):
    def find_bids(self):
        bids = []
        for ilk_id in self.ilks:
            bids.extend(self.flippers[ilk_id].bids)
        return bids

    def run_bidding_model(self, bid, ilk_id=""):
        if bid.guy == self.ADDRESS or not bid.lot:
            return {"price": Wad(0)}

        if bid.bid == Rad(0):
            return {"price": Wad(1)}

        return {"price": self.flippers[ilk_id].beg * Wad(bid.bid / Rad(bid.lot))}


class SpotterKeeper(Keeper):
    spotter = None

    def __init__(self, ilks, spotter):
        self.spotter = spotter
        super().__init__(ilks)

    def execute_actions_for_timestep(self, t):
        actions = []
        for ilk_id in self.ilks:
            self.spotter.poke(ilk_id, t)
            actions.append({"key": "POKE", "meta": {"ilk_id": ilk_id}})
        return actions


class BiteKeeper(Keeper):
    cat = None
    vat = None

    def __init__(self, ilks, cat, vat):
        self.cat = cat
        self.vat = vat
        super().__init__(ilks)

    def execute_actions_for_timestep(self, t):
        actions = []
        for ilk_id in self.ilks:
            ilk = self.vat.ilks[ilk_id]
            for urn in self.vat.urns[ilk_id].values():
                if Rad(urn.ink * ilk.spot) < Rad(urn.art * ilk.rate):
                    self.cat.bite(ilk_id, urn.ADDRESS, t)
                    actions.append(
                        {
                            "key": "BITE",
                            "meta": {"urn_addr": urn.ADDRESS, "ilk_id": ilk_id},
                        }
                    )
        return actions
