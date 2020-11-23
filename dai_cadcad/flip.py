""" Flip Module
    Class-based representation of the Flip smart contract
    (contains only what is necessary for the simulation)
"""


class Flipper:
    ADDRESS = ""

    vat = None
    beg = None
    ttl = None
    tau = None
    kicks = None
    bids = {}
    ilk = None

    def __init__(self, vat, beg, ttl, tau, kicks, bids, ilk):
        """"""

        self.ADDRESS = f"flipper_{ilk}"

        self.vat = vat

        self.beg = beg
        self.ttl = ttl
        self.tau = tau
        self.kicks = kicks
        self.bids = bids
        self.ilk = ilk

    def kick(self, vat, usr, gal, tab, lot, bid, end):
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

        vat_flux(vat, self.ilk, "cat", "flipper_eth", lot)

    def tend(self, vat, bid_id, usr, lot, bid, now):
        """Places a tend bid on a Flipper auction."""

        curr_bid = self.bids[bid_id]

        assert (
            curr_bid["tic"] > now or curr_bid["tic"] == 0
        ), "Flipper/already-finishied-tic"
        assert curr_bid["end"] > now, "Flipper/already-finishied-end"

        assert lot == curr_bid["lot"], "Flipper/lot-not-matching"
        assert bid <= curr_bid["tab"], "Flipper/higher-than-tab"
        assert bid > curr_bid["bid"], "Flipper/bid-not-higher"
        assert (
            bid >= curr_bid["bid"] * self.beg or bid == curr_bid["tab"]
        ), "Flipper/insufficient-increase"

        if usr != curr_bid["guy"]:
            vat_move(vat, usr, curr_bid["guy"], curr_bid["bid"])
            curr_bid["guy"] = usr
        vat_move(vat, usr, curr_bid["gal"], bid - curr_bid["bid"])

        curr_bid["bid"] = bid
        curr_bid["tic"] = now + self.ttl

    def dent(self, vat, bid_id, usr, lot, bid, now):
        """Places a dent bid on a Flipper auction."""

        curr_bid = self.bids[bid_id]

        assert (
            curr_bid["tic"] > now or curr_bid["tic"] == 0
        ), "Flipper/already-finished-tic"
        assert curr_bid["end"] > now, "Flipper/already-finished-end"

        assert bid == curr_bid["bid"], "Flipper/not-matching-bid"
        assert bid == curr_bid["tab"], "Flipper/tend-not-finished"
        assert lot < curr_bid["lot"], "Flipper/lot-not-lower"
        assert lot * self.beg <= curr_bid["lot"], "Flipper/insufficient-decrease"

        if usr != curr_bid["guy"]:
            vat_move(vat, usr, curr_bid["guy"], curr_bid["bid"])
            curr_bid["guy"] = usr
        vat_flux(vat, self.ilk, "flipper_eth", curr_bid["usr"], curr_bid["lot"] - lot)

        curr_bid["lot"] = lot
        curr_bid["tic"] = now + self.ttl

    def deal(flipper, vat, cat, bid_id, now):
        """Deals out a Flipper auction."""

        curr_bid = flipper["bids"][bid_id]

        assert curr_bid["tic"] != 0 and (
            curr_bid["tic"] <= now or curr_bid["end"] <= now
        ), "Flipper/not-finished"

        cat_claw(cat, curr_bid["tab"])
        vat_flux(vat, flipper["ilk"], "flipper_eth", curr_bid["guy"], curr_bid["lot"])
        del flipper["bids"][bid_id]