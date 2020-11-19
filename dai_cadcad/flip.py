""" Flip Module
    Class-based representation of the Flip smart contract
    (contains only what is necessary for the simulation)
"""


class Flip:
    ADDRESS = "flip"

    vat = None
    beg = None
    ttl = None
    tau = None
    kicks = None
    bids = {}

    def __init__(self, vat, beg, ttl, tau, kicks, bids):
        """"""

        self.vat = vat

        self.beg = beg
        self.ttl = ttl
        self.tau = tau
        self.kicks = kicks
        self.bids = bids

    def flipper_kick(flipper, vat, user_id, gal, tab, lot, bid, end):
        """Kicks off a new Flip auction."""

        flipper["kicks"] += 1
        bid_id = flipper["kicks"]

        flipper["bids"][bid_id] = {
            "bid": bid,
            "lot": lot,
            "guy": "cat",
            "tic": 0,
            "end": end,
            "usr": user_id,
            "gal": gal,
            "tab": tab,
        }

        vat_flux(vat, flipper["ilk"], "cat", "flipper_eth", lot)

    def flipper_tend(flipper, vat, bid_id, user_id, lot, bid, now):
        """Places a tend bid on a Flipper auction."""

        curr_bid = flipper["bids"][bid_id]

        assert (
            curr_bid["tic"] > now or curr_bid["tic"] == 0
        ), "Flipper/already-finishied-tic"
        assert curr_bid["end"] > now, "Flipper/already-finishied-end"

        assert lot == curr_bid["lot"], "Flipper/lot-not-matching"
        assert bid <= curr_bid["tab"], "Flipper/higher-than-tab"
        assert bid > curr_bid["bid"], "Flipper/bid-not-higher"
        assert (
            bid >= curr_bid["bid"] * flipper["beg"] or bid == curr_bid["tab"]
        ), "Flipper/insufficient-increase"

        if user_id != curr_bid["guy"]:
            vat_move(vat, user_id, curr_bid["guy"], curr_bid["bid"])
            curr_bid["guy"] = user_id
        vat_move(vat, user_id, curr_bid["gal"], bid - curr_bid["bid"])

        curr_bid["bid"] = bid
        curr_bid["tic"] = now + flipper["ttl"]

    def flipper_dent(flipper, vat, bid_id, user_id, lot, bid, now):
        """Places a dent bid on a Flipper auction."""

        curr_bid = flipper["bids"][bid_id]

        assert (
            curr_bid["tic"] > now or curr_bid["tic"] == 0
        ), "Flipper/already-finished-tic"
        assert curr_bid["end"] > now, "Flipper/already-finished-end"

        assert bid == curr_bid["bid"], "Flipper/not-matching-bid"
        assert bid == curr_bid["tab"], "Flipper/tend-not-finished"
        assert lot < curr_bid["lot"], "Flipper/lot-not-lower"
        assert lot * flipper["beg"] <= curr_bid["lot"], "Flipper/insufficient-decrease"

        if user_id != curr_bid["guy"]:
            vat_move(vat, user_id, curr_bid["guy"], curr_bid["bid"])
            curr_bid["guy"] = user_id
        vat_flux(
            vat, flipper["ilk"], "flipper_eth", curr_bid["usr"], curr_bid["lot"] - lot
        )

        curr_bid["lot"] = lot
        curr_bid["tic"] = now + flipper["ttl"]

    def flipper_deal(flipper, vat, cat, bid_id, now):
        """Deals out a Flipper auction."""

        curr_bid = flipper["bids"][bid_id]

        assert curr_bid["tic"] != 0 and (
            curr_bid["tic"] <= now or curr_bid["end"] <= now
        ), "Flipper/not-finished"

        cat_claw(cat, curr_bid["tab"])
        vat_flux(vat, flipper["ilk"], "flipper_eth", curr_bid["guy"], curr_bid["lot"])
        del flipper["bids"][bid_id]