"""
// SPDX-License-Identifier: AGPL-3.0-or-later
/// flop.sol -- Debt auction
// Copyright (C) 2018 Rain <rainbreak@riseup.net>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
pragma solidity >=0.5.12;
import "./lib.sol";
interface VatLike {
    function move(address,address,uint) external;
    function suck(address,address,uint) external;
}
interface GemLike {
    function mint(address,uint) external;
}
"""
import time

from pymaker.numeric import Wad
from util import require

"""
/*
   This thing creates gems on demand in return for dai.
 - `lot` gems in return for bid
 - `bid` dai paid
 - `gal` receives dai income
 - `ttl` single bid lifetime
 - `beg` minimum bid increase
 - `end` max auction duration
*/
"""


class Flopper:

    # messageclass

    # bid info
    class Bid:
        bid = 0;
        lot = 0;
        guy = 0;
        tic = 0
        end = 0

    def __init__(self, vat, gem, msg):
        self.wards = dict()
        self.message = msg
        self.wards[msg.sender] = 1;
        self.vat = vat
        self.gem = gem
        self.bids = dict()
        self.kicks = 0
        self.ADDRESS = "flapper"
        self.bid_id = 0;
        self.pads = 0.5
        self.ONE = Wad.from_number(1.00)
        self.beg = Wad.from_number(1.05)
        # 3 hours bidduration[seconds]
        self.ttl = 3 * 60 * 60;
        self.tau = 2 * 24 * 60 * 60


def file(self, what, data):
    if (what == "beg"):
        self.beg = data;
    elif (what == "pad"):
        self.pad = data;
    elif (what == "ttl"):
        self.ttl = data;
    elif (what == "tau"):
        self.tau = data;
    else:
        raise Exception("Flopper/file-unrecognized-param")


def kick(self, gal, lot, bid, now):
    require(self.live == 1, "Flapper/not-live")

    require(self.kicks > -1, "Flapper/overflow")

    self.kicks += 1
    self.bid_id += self.kicks;

    self.bids[self.bid_id].bid = bid;
    self.bids[self.bid_id].lot = lot;
    self.bids[self.bid_id].guy = gal;
    self.bids[self.bid_id].end = self.add(now, self.tau);


def tick(self, bid_id,now):
    require(self.bids[bid_id].end <= self.now,"Flapper/not-finished")
    require(self.bids[bid_id].tic == 0,"Flapper/bid-already-placed")
    self.bids[bid_id].lot = self.pad * self.bids[bid_id].lot
    self.bids[bid_id].end = now+ self.tau;


def dent(self, bid_id, lot, bid):
    require( (self.live == 1), "Flopper/not-live")
    require( (self.bids[bid_id].guy != 0),"Flopper/guy-not-set")
    require ( (self.bids[bid_id].tic > self.now or self.bids[id].tic == 0),"Flopper/already-finished-tic")
    require(self.bids[bid_id].end > self.now, "Flopper/already-finished-end")
    require(bid == self.bids[bid_id].bid,"Flopper/not-matching-bid")
    require(self.lot < self.bids[bid_id].lot,"Flopper/lot-not-lower")
    require(self.beg* lot <= self.bids[bid_id].lot,"Flopper/insufficient-decrease")
    if (self.message.sender != self.bids[bid_id].guy):
        self.vat.move(self.bids.message.sender, self.bids[bid_id].guy, bid);
        if (self.bids[bid_id].tic == 0):
            Ash = self.bids[bid_id].guy.Ash();
            self.bids[bid_id].guy.kiss(min(bid, Ash));

        self.bids[bid_id].guy = self.msg.sender;

    self.bids[bid_id].lot = lot;
    self.bids[bid_id].tic = int(self.now)+ self.ttl


def deal(self, sid):
    require(self.live == 1,"Flapper/not-live")
    require(self.bids[sid].tic != 0 and (self.bids[sid].tic < self.now or self.bids[sid].end < self.now), "Flapper/not-finished")
    self.vat.move(sid, self.bids[sid].guy, self.bids[sid].lot);
    self.gem.mint(sid, self.bids[sid].bid)
    del self.bids[sid];


