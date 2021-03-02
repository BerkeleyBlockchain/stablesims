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
class VatLike:
    def move(self, fro,to,amt):
        pass


"""
interface GemLike {
    function move(address,address,uint) external;
    function burn(address,uint) external;
}
"""
class GemLike:
    def mint(self, fro):
        pass

"""
interface VowLike {
    function Ash() external returns (uint);
    function kiss(uint) external;
}
"""
class VowLike:
    def Ash(self, fro):
        pass
    def kiss(self, fro):
        pass
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
    wards = dict()
    #messageclass
    message = 0;

    def rely(self, usr,send):
        if self.wards[send] != 1:
            self.wards[usr] = 1
    def deny(self, usr,send):
        if self.wards[send] != 1:
            self.wards[usr] = 0
#bid info
    class Bid :
        bid = 0;
        lot = 0 ;
        guy = 0;
        tic = 0
        end = 0

    pads = 0.5
    bids = dict()
    ONE = 1.00E18;
    beg = 1.05E18;
    # 3 hours bidduration[seconds]
    ttl = 3 * 60 * 60;
    # 2 days total auction length  [seconds]
    tau = 2 * 24 * 60 * 60
    kicks = 0;
    live = 0
    now = time.time()
    vow = 0
    def __init__(self, vat, gem,msg) :
        self.message = msg
        self.wards[msg.sender] = 1;
        self.vat = VatLike(vat);
        self.gem = GemLike(gem);
        self.live = 1;

    def add(self, x, y):
        z = x + y
        if z > x:
            return z
        return -1

    def mul(self, x, y):
        z = x * y
        if (y == 0 or (z // y == x)):
            return z
        return -1

    """ 

    // --- Admin ---
    function file(bytes32 what, uint data) external note auth {
        if (what == "beg") beg = data;
        else if (what == "pad") pad = data;
        else if (what == "ttl") ttl = uint48(data);
        else if (what == "tau") tau = uint48(data);
        else revert("Flopper/file-unrecognized-param");
    }
    """




    def kick(self, gal, lot, bid) :
        if (self.live != 1):
            return "Flapper/not-live"
        if (self.kicks < -1):
            return "Flapper/overflow";
        sid = id(self)
        sid += self.kicks;

        self.bids[sid].bid = bid;
        self.bids[sid].lot = lot;
        self.bids[sid].guy = gal;
        self.bids[sid].end = self.add(self.now, self.tau);

        # emit Kick(id, lot, bid);


    def tick(self, sid) :
        if self.bids[sid].end > self.now:
            return "Flapper/not-finished"
        if self.bids[sid].tic != 0:
            return "Flapper/bid-already-placed"
        self.bids[sid].lot = self.mul(self.pad, self.bids[sid].lot) / self.ONE;
        self.bids[sid].end = self.add(self.now, self.tau);
    def dent(self, sid, lot,  bid):
        if not(self.live == 1):
            return "Flopper/not-live";
        if not(self.bids[sid].guy != 0):
            return "Flopper/guy-not-set";
        if not(self.bids[sid].tic > self.now or self.bids[id].tic == 0):
            return "Flopper/already-finished-tic"
        if not(self.bids[sid].end > self.now):
            return "Flopper/already-finished-end"

        if not (bid == self.bids[sid].bid):
            return "Flopper/not-matching-bid"
        if not (self.lot <  self.bids[sid].lot):
            return "Flopper/lot-not-lower"
        if not (self.mul(self.beg, lot) <= self.mul(self.bids[sid].lot, self.ONE)):
            return "Flopper/insufficient-decrease"

        if (self.message.sender != self.bids[sid].guy):
            self.vat.move(self.bids.message.sender, self.bids[sid].guy, bid);
            if (self.bids[sid].tic == 0):
                Ash = VowLike(self.bids[sid].guy).Ash();
                VowLike(self.bids[sid].guy).kiss(min(bid, Ash));

            self.bids[sid].guy = self.msg.sender;


        self.bids[sid].lot = lot;
        self.bids[sid].tic = self.add(int(self.now), self.ttl);
    
    def deal(self, sid):
        if not (self.live == 1):
            return "Flapper/not-live"
        if not (self.bids[sid].tic != 0 and (self.bids[sid].tic < self.now or self.bids[sid].end < self.now)):
            return "Flapper/not-finished"
        self.vat.move(sid, self.bids[sid].guy, self.bids[sid].lot);
        self.gem.mint(sid, self.bids[sid].bid)
        del self.bids[sid];

    def cage(self ):
       self.live = 0;
       self.vow = self.message.sender;
       #self.vat.move(address(this), self.message.sender, rad);

    def yank(self, sid):
        if not(self.live == 0):
            return "Flapper/still-live"
        if not (self.bids[sid].guy != (0)):
            return "Flapper/guy-not-set"
        self.vat.suck(self.vow, self.bids[sid].guy, self.bids[sid].bid);
        del self.bids[sid];
