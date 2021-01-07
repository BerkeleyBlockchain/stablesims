""" Flip Module
    Class-based representation of the Flip smart contract
    (contains only what is necessary for the simulation)

"""
from dai_cadcad.pymaker.numeric import Wad, Rad
from dai_cadcad.util import require


class Bid:
    bid = Rad(0)
    lot = Wad(0)
    guy = ""
    tic = ""  # Date
    end = ""  # Date
    usr = ""
    gal = ""
    tab = Rad(0)

    def __init__(self, bid, lot, guy, tic, end, usr, gal, tab):
        self.bid = bid
        self.lot = lot
        self.guy = guy
        self.tic = tic
        self.end = end
        self.usr = usr
        self.gal = gal
        self.tab = tab


class Flipper:
    ADDRESS = ""

    beg = None
    bids = {}
    cat = None
    ilk_id = None
    kicks = None
    ttl = None
    tau = None
    vat = None

    def __init__(self, beg, bids, cat, ilk_id, kicks, ttl, tau, vat):
        """"""

        self.ADDRESS = f"flipper_{ilk_id}"

        self.vat = vat
        self.cat = cat
        self.beg = beg
        self.ttl = ttl
        self.tau = tau
        self.kicks = kicks
        self.bids = bids
        self.ilk_id = ilk_id

    def kick(
        self, usr, gal, tab, lot, bid, end
    ):  # TODO: should these be instance attribute?
        """Kicks off a new Flip auction."""

        self.kicks += 1
        bid_id = self.kicks

        self.bids[bid_id] = {
            "bid": bid,
            "lot": lot,
            "guy": "cat",
            "tic": 0,
            "end": end,
            "usr": usr,
            "gal": gal,
            "tab": tab,
        }

        self.vat.flux(self.ilk_id, "cat", "flipper_eth", lot)

    def tend(self, bid_id, usr, lot, bid, now):
        """Places a tend bid on a Flipper auction."""

        curr_bid = self.bids[bid_id]

        require(
            curr_bid["tic"] > now or curr_bid["tic"] == 0,
            "Flipper/already-finishied-tic",
        )
        require(curr_bid["end"] > now, "Flipper/already-finishied-end")

        require(lot == curr_bid["lot"], "Flipper/lot-not-matching")
        require(bid <= curr_bid["tab"], "Flipper/higher-than-tab")
        require(bid > curr_bid["bid"], "Flipper/bid-not-higher")
        require(
            bid >= curr_bid["bid"] * self.beg or bid == curr_bid["tab"]
        ), "Flipper/insufficient-increase"

        if usr != curr_bid["guy"]:
            self.vat.move(usr, curr_bid["guy"], curr_bid["bid"])
            curr_bid["guy"] = usr
        self.vat.move(usr, curr_bid["gal"], bid - curr_bid["bid"])

        curr_bid["bid"] = bid
        curr_bid["tic"] = now + self.ttl

    def dent(self, bid_id, usr, lot, bid, now):
        """Places a dent bid on a Flipper auction."""

        curr_bid = self.bids[bid_id]

        require(
            curr_bid["tic"] > now or curr_bid["tic"] == 0
        ), "Flipper/already-finished-tic"
        require(curr_bid["end"] > now, "Flipper/already-finished-end")

        require(bid == curr_bid["bid"], "Flipper/not-matching-bid")
        require(bid == curr_bid["tab"], "Flipper/tend-not-finished")
        require(lot < curr_bid["lot"], "Flipper/lot-not-lower")
        require(lot * self.beg <= curr_bid["lot"], "Flipper/insufficient-decrease")

        if usr != curr_bid["guy"]:
            self.vat.move(usr, curr_bid["guy"], curr_bid["bid"])
            curr_bid["guy"] = usr
        self.vat.flux(
            self.ilk_id, "flipper_eth", curr_bid["usr"], curr_bid["lot"] - lot
        )

        curr_bid["lot"] = lot
        curr_bid["tic"] = now + self.ttl

    def deal(self, bid_id, now):
        """Deals out a Flipper auction."""

        curr_bid = self.bids[bid_id]

        require(
            curr_bid["tic"] != 0 and (curr_bid["tic"] <= now or curr_bid["end"] <= now),
            "Flipper/not-finished",
        )

        self.cat.claw(curr_bid["tab"])
        self.vat.flux(self.ilk_id, "flipper_eth", curr_bid["guy"], curr_bid["lot"])
        del self.bids[bid_id]
