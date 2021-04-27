"""
Class-based representation of the Flopper smart contract.
Contains only what is necessary for the simulation.
"""

from pydss.pymaker.numeric import Wad
from pydss.util import require


class Flopper:

    # bid info
    class Bid:
        bid = 0
        lot = 0
        guy = 0
        tic = 0
        end = 0

    def __init__(self, vat, gem):
        self.ADDRESS = "flopper"
        self.vat = vat
        self.gem = gem
        self.bids = dict()
        self.kicks = 0
        self.pad = Wad.from_number(1.5)
        self.beg = Wad.from_number(1.05)
        self.ttl = 3 * 60 * 60
        self.tau = 2 * 24 * 60 * 60


def file(self, what, data):
    if what == "beg":
        self.beg = data
    elif what == "pad":
        self.pad = data
    elif what == "ttl":
        self.ttl = data
    elif what == "tau":
        self.tau = data
    else:
        raise Exception("Flopper/file-unrecognized-param")


def kick(self, gal, lot, bid, now):
    require(self.live == 1, "Flapper/not-live")

    require(self.kicks > -1, "Flapper/overflow")

    self.kicks += 1
    bid_id = self.kicks

    self.bids[bid_id].bid = bid
    self.bids[bid_id].lot = lot
    self.bids[bid_id].guy = gal
    self.bids[bid_id].end = now + self.tau


def tick(self, bid_id, now):
    require(self.bids[bid_id].end <= now, "Flapper/not-finished")
    require(self.bids[bid_id].tic == 0, "Flapper/bid-already-placed")
    self.bids[bid_id].lot = self.pad * self.bids[bid_id].lot
    self.bids[bid_id].end = now + self.tau


def dent(self, bid_id, lot, bid, sender, now):
    require((self.live == 1), "Flopper/not-live")
    require((self.bids[bid_id].guy != 0), "Flopper/guy-not-set")
    require(
        (self.bids[bid_id].tic > now or self.bids[id].tic == 0),
        "Flopper/already-finished-tic",
    )
    require(self.bids[bid_id].end > now, "Flopper/already-finished-end")
    require(bid == self.bids[bid_id].bid, "Flopper/not-matching-bid")
    require(self.lot < self.bids[bid_id].lot, "Flopper/lot-not-lower")
    require(self.beg * lot <= self.bids[bid_id].lot, "Flopper/insufficient-decrease")
    if sender != self.bids[bid_id].guy:
        self.vat.move(sender, self.bids[bid_id].guy, bid)
        if self.bids[bid_id].tic == 0:
            Ash = self.bids[bid_id].guy.Ash()
            self.bids[bid_id].guy.kiss(min(bid, Ash))

        self.bids[bid_id].guy = sender

    self.bids[bid_id].lot = lot
    self.bids[bid_id].tic = int(now) + self.ttl


def deal(self, bid_id, now):
    require(self.live == 1, "Flapper/not-live")
    require(
        self.bids[bid_id].tic != 0
        and (self.bids[bid_id].tic < now or self.bids[bid_id].end < now),
        "Flapper/not-finished",
    )
    self.gem.mint(bid_id, self.bids[bid_id].bid)
    del self.bids[bid_id]
