""" Keeper Module
    Class-based representation of a keeper in the Maker ecosystem.
    By this, we mean any external agent, not just auction keepers.
    (contains only what is necessary for the simulation)
"""

from uuid import uuid4

from dai_cadcad.pymaker.numeric import Wad, Rad


class Keeper:
    ADDRESS = ""

    vat = None
    dai_join = None
    gem_joins = {}

    urns = {}
    num_urns = 0

    def __init__(self, vat, dai_join, ilks):
        """ `ilks` must be an array containing a configuration object for each ilk type of the
            following form:
            {"gem_join": GemJoin}
        """

        self.ADDRESS = f"keeper-{uuid4().hex}"

        self.vat = vat
        self.dai_join = dai_join

        for ilk in ilks:
            self.gem_joins[ilk["ilk_id"]] = ilk["gem_join"]

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


class AuctionKeeper(Keeper):
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

    def find_bids(self, **kwargs):
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


class NaiveFlipperKeeper(FlipperKeeper):
    def find_bids(self, ilk_id=""):
        return self.flippers[ilk_id].bids

    def run_bidding_model(self, bid, ilk_id=""):
        if bid.guy == self.ADDRESS or not bid.lot:
            return {"price": Wad(0)}

        if bid.bid == Rad(0):
            return {"price": Wad(1)}

        return {"price": self.flippers[ilk_id].beg * Wad(bid.bid / Rad(bid.lot))}
