"""
Class-based representation of the Flapper smart contract.
Contains only what is necessary for the simulation.
"""

from pydss.pymaker.numeric import Wad
from pydss.util import require


class Flapper:

    # bid info
    class Bid:
        bid = 0
        lot = 0
        guy = 0
        tic = 0
        end = 0

    def __init__(self, vat, gem):
        self.ADDRESS = "flapper"
        self.vat = vat
        self.gem = gem
        self.live = 1
        self.bids = dict()
        self.beg = Wad.from_number(1.05)
        self.ttl = 3 * 60 * 60
        self.tau = 2 * 24 * 60 * 60
        self.kicks = 0
        self.live = 0
        self.vat = vat
        self.gem = gem

    def kick(self, lot, bid, now, sender):
        require(self.live == 1, "Flapper/not-live")

        require(self.kicks < -1, "Flapper/overflow")

        self.kicks += 1
        bid_id = self.kicks

        self.bids[bid_id].bid = bid
        self.bids[bid_id].lot = lot
        self.bids[bid_id].guy = sender
        self.bids[bid_id].end = now + self.tau

        self.vat.move(sender, self.ADDRESS, lot)

    def file(self, what, data):
        if what == "beg":
            self.beg = data
        elif what == "ttl":
            self.ttl = data
        elif what == "tau":
            self.tau = data
        else:
            raise Exception("Flapper/file-unrecognized-param")

    def deal(self, bid_id, sender, bid, now):
        require(self.live == 1, "Flapper/not-live")
        require(
            self.bids[bid_id].tic != 0
            and (self.bids[bid_id].tic < now or self.bids[bid_id].end < now),
            "Flapper/not-finished",
        )
        self.gem.transferFrom(sender, self.ADDRESS, bid - self.bids[bid_id].bid)
        self.gem.burn(bid_id, self.bids[bid_id].bid)
        del self.bids[bid_id]

    def tick(self, bid_id, now):
        require(self.bids[bid_id].end <= now, "Flapper/not-finished")
        require(self.bids[bid_id].tic == 0, "Flapper/bid-already-placed")
        # @Nathan TODO: This is the incorrect tick function, from flop.sol
        # Please transcribe the appropriate one from Maker's flap.sol
        # self.bids[bid_id].lot = self.pad * self.bids[bid_id].lot

    def tend(self, bid_id, lot, bid, sender, now):
        require(self.live == 1, "Flapper/not-live")
        require(self.bids[bid_id].guy != 0, "Flapper/guy-not-set")
        require(
            self.bids[bid_id].tic > now or self.bids[bid_id].tic == 0,
            "Flapper/already-finished-tic",
        )
        require(self.bids[bid_id].end > now, "Flapper/already-finished-end")
        require(lot == self.bids[bid_id].lot, "Flapper/lot-not-matching")
        require(bid > self.bids[bid_id].bid, "Flapper/bid-not-higher")
        require(
            bid >= self.beg * self.bids[bid_id].bid, "Flapper/insufficient-increase",
        )

        if sender != self.bids[bid_id].guy:
            self.gem.transferFrom(sender, self.bids[bid_id].guy, self.bids[bid_id].bid)
            self.bids[bid_id].guy = sender
        self.gem.transferFrom(sender, self.ADDRESS, bid - self.bids[bid_id].bid)

        self.bids[bid_id].bid = bid
        self.bids[bid_id].tic = now + self.ttl
        return [bid]
