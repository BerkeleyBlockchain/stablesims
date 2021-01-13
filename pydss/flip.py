""" Flip Module
    Class-based representation of the Flip smart contract
    (contains only what is necessary for the simulation)

"""
from pydss.pymaker.numeric import Wad
from pydss.util import require


class Bid:
    """
    id = str
    bid = Rad
    lot = Wad
    guy = str
    tic = int
    end = int
    usr = str
    gal = str
    tab = Rad
    """

    def __init__(self, bid, lot, guy, tic, end, usr, gal, tab, bid_id):
        self.bid = bid
        self.lot = lot
        self.guy = guy
        self.tic = tic
        self.end = end
        self.usr = usr
        self.gal = gal
        self.tab = tab
        self.id = bid_id


class Flipper:
    """
    ADDRESS = str

    beg = Wad
    bids = dict[int: Bid]
    cat = Cat
    ilk_id = str
    kicks = int
    ttl = int
    tau = int
    vat = Vat
    """

    def __init__(self, vat, cat, ilk_id):
        """"""

        self.ADDRESS = f"flipper-{ilk_id}"

        self.vat = vat
        self.cat = cat
        self.ilk_id = ilk_id

        self.beg = Wad(0)
        self.bids = {}
        self.kicks = 0
        self.ttl = 0
        self.tau = 0

    def file(self, what, data):
        if what == "beg":
            self.beg = data
        elif what == "ttl":
            self.ttl = data
        elif what == "tau":
            self.tau = data
        elif what == "cat":
            self.cat = data
        else:
            raise Exception("Flipper/file-unrecognized-param")

    def kick(
        self, usr, gal, tab, lot, bid, now
    ):  # TODO: should these be instance attribute?
        """Kicks off a new Flip auction."""

        self.kicks += 1
        bid_id = self.kicks

        self.bids[bid_id] = Bid(
            bid, lot, "cat", 0, now + self.tau, usr, gal, tab, bid_id
        )

        self.vat.flux(self.ilk_id, "cat", "flipper_eth", lot)

    def tend(self, bid_id, usr, lot, bid, now):
        """Places a tend bid on a Flipper auction."""

        curr_bid = self.bids[bid_id]

        require(
            curr_bid.tic > now or curr_bid.tic == 0, "Flipper/already-finished-tic",
        )
        require(curr_bid.end > now, "Flipper/already-finished-end")

        require(lot == curr_bid.lot, "Flipper/lot-not-matching")
        require(bid <= curr_bid.tab, "Flipper/higher-than-tab")
        require(bid > curr_bid.bid, "Flipper/bid-not-higher")
        require(
            bid >= curr_bid.bid * self.beg or bid == curr_bid.tab,
            "Flipper/insufficient-increase",
        )

        if usr != curr_bid.guy:
            self.vat.move(usr, curr_bid.guy, curr_bid.bid)
            curr_bid.guy = usr
        self.vat.move(usr, curr_bid.gal, bid - curr_bid.bid)

        curr_bid.bid = bid
        curr_bid.tic = now + self.ttl

    def dent(self, bid_id, usr, lot, bid, now):
        """Places a dent bid on a Flipper auction."""

        curr_bid = self.bids[bid_id]

        require(curr_bid.tic > now or curr_bid.tic == 0, "Flipper/already-finished-tic")
        require(curr_bid.end > now, "Flipper/already-finished-end")

        require(bid == curr_bid.bid, "Flipper/not-matching-bid")
        require(bid == curr_bid.tab, "Flipper/tend-not-finished")
        require(lot < curr_bid.lot, "Flipper/lot-not-lower")
        require(lot * self.beg <= curr_bid.lot, "Flipper/insufficient-decrease")

        if usr != curr_bid.guy:
            self.vat.move(usr, curr_bid.guy, curr_bid.bid)
            curr_bid.guy = usr
        self.vat.flux(self.ilk_id, "flipper_eth", curr_bid.usr, curr_bid.lot - lot)

        curr_bid.lot = lot
        curr_bid.tic = now + self.ttl

    def deal(self, bid_id, now):
        """Deals out a Flipper auction."""

        curr_bid = self.bids[bid_id]

        require(
            curr_bid.tic != 0 and (curr_bid["tic"] <= now or curr_bid.end <= now),
            "Flipper/not-finished",
        )

        self.cat.claw(curr_bid.tab)
        self.vat.flux(self.ilk_id, "flipper_eth", curr_bid.guy, curr_bid.lot)
        del self.bids[bid_id]
