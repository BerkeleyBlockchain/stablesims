""""
//pragma solidity >=0.5.12;
import "./lib.sol";
interface VatLike {
    function move(address,address,uint) external;
}
"""


import require as require

from pymaker.numeric import Wad
from util import require


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
    def move(self, fro,to,amt):
        pass
    def move(self, adr,amt):
        pass
"""
/*
   This thing lets you sell some dai in return for gems.
 - `lot` dai in return for bid
 - `bid` gems paid
 - `ttl` single bid lifetime
 - `beg` minimum bid increase
 - `end` max auction duration
*/
"""
class Flapper:



#bid info
    class Bid :
        bid = 0;
        lot = 0 ;
        guy = 0;
        tic = 0
        end = 0



    """"
    // --- Events ---
    event Kick(
      uint256 id,
      uint256 lot,
      uint256 bid
    );
    """


    def __init__(self, vat, gem,msg) :

        self.msg = msg

        self.vat = VatLike(vat);
        self.gem = GemLike(gem);
        self.live = 1;
        self.bids = dict()
        self.ONE = Wad.from_number(1.00)
        self.beg = Wad.from_number(1.05)
        # 3 hours bidduration[seconds]
        self.ttl = 3 * 60 * 60;
        # 2 days total auction length  [seconds]
        self.tau = 2 * 24 * 60 * 60
        self.kicks = 0;
        self.live = 0
        self.vat = vat
        self.gem =gem


    def kick(self, lot, bid) :
        require(self.live == 1,"Flapper/not-live")

        require(self.kicks < -1,"Flapper/overflow")

        self.kicks+=1
        bid_id = self.kicks;

        self.bids[bid_id].bid = bid;
        self.bids[bid_id].lot = lot;
        self.bids[bid_id].guy = self.msg.sender;
        self.bids[bid_id].end = self.now+self.tau

        self.vat.move(self.msg.sender, self.address(self), lot);
        # emit Kick(id, lot, bid);

    def file(self,what, data):
        if (what == "beg"):
            self.beg = data;
        elif (what == "ttl"):
            self.ttl = data;
        elif (what == "tau"):
            self.tau = data;
        else:
            raise Exception("Flapper/file-unrecognized-param");
    def deal(self,bid_id):
        require(self.live == 1,"Flapper/not-live")
        require(self.bids[bid_id].tic != 0 and (self.bids[bid_id].tic < self.now or self.bids[bid_id].end < self.now),"Flapper/not-finished")
        self.vat.move(bid_id, self.bids[bid_id].guy, self.bids[bid_id].lot);
        self.gem.burn(bid_id, self.bids[bid_id].bid);
        del self.bids[bid_id];

    def tick(self, bid_id):
        require(self.bids[bid_id].end <= self.now, "Flapper/not-finished")
        require(self.bids[bid_id].tic == 0, "Flapper/bid-already-placed")
        self.bids[bid_id].lot = self.pad * self.bids[bid_id].lot

    def tend(self, bid_id, lot, bid,sender_id):
        require(self.live == 1,"Flapper/not-live")
        require(self.bids[bid_id].guy != 0,"Flapper/guy-not-set")
        require(self.bids[bid_id].tic > self.now or self.bids[bid_id].tic == 0,"Flapper/already-finished-tic")
        require(self.bids[bid_id].end > self.now,"Flapper/already-finished-end")
        require(lot == self.bids[bid_id].lot,"Flapper/lot-not-matching")
        require(bid >  self.bids[bid_id].bid,"Flapper/bid-not-higher")
        require(self.mul(bid, self.ONE) >= self.mul(self.beg, self.bids[bid_id].bid),"Flapper/insufficient-increase")

        if (self.msg.sender != self.bids[bid_id].guy):
            self.gem.move(self.msg.sender, self.bids[bid_id].guy, self.bids[bid_id].bid);
            self.bids[bid_id].guy = self.msg.sender;
        self.gem.move(self.msg.sender,sender_id, bid - self.bids[bid_id].bid);

        self.bids[bid_id].bid = bid;
        self.bids[bid_id].tic = self.add(self.now, self.ttl);




