""""
//pragma solidity >=0.5.12;

import "./lib.sol";

interface VatLike {
    function move(address,address,uint) external;
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

    bids = dict()
    ONE = 1.00E18;
    beg = 1.05E18;
    #3 hours bidduration[seconds]
    ttl = 3*60*60;
    #2 days total auction length  [seconds]
    tau = 2 *24*60*60
    kicks = 0;
    live = 0
    now = time.time()

    """"
    // --- Events ---
    event Kick(
      uint256 id,
      uint256 lot,
      uint256 bid
    );
    """
    vat = None;
    gem = None

    def __init__(self, vat, gem,msg) :
        self.message = msg
        self.wards[msg.sender] = 1;
        self.vat = VatLike(vat);
        self.gem = GemLike(gem);
        self.live = 1;

    def add(self, x, y):
        z = x+y
        if z > x:
            return z
        return -1

    def mul(self, x, y):
        z = x * y
        if (y == 0 or (z // y == x)):
            return z
        return -1
    def kick(self, lot, bid) :
        if (self.live != 1):
            return "Flapper/not-live"
        if (self.kicks < -1):
            return "Flapper/overflow";
        sid = id(self)
        sid += self.kicks;

        self.bids[sid].bid = bid;
        self.bids[sid].lot = lot;
        self.bids[sid].guy = self.message.sender;
        self.bids[sid].end = self.add(self.now, self.tau);

        self.vat.move(self.msg.sender, self.address(self), lot);
        # emit Kick(id, lot, bid);
    """
    // --- Admin ---
    function file(bytes32 what, uint data) external note auth 
        if (what == "beg") beg = data;
        else if (what == "ttl") ttl = uint48(data);
        else if (what == "tau") tau = uint48(data);
        else revert("Flapper/file-unrecognized-param");
    
    """


    def tick(self, sid) :
        if self.bids[sid].end > self.now:
            return "Flapper/not-finished"
        if self.bids[sid].tic != 0:
            return "Flapper/bid-already-placed"
        self.bids[sid].end = self.add(self.now, self.tau);
    def tend(self, sid, lot, bid):
        if self.live != 1:
            return "Flapper/not-live"
        if self.bids[sid].guy == 0:
           return "Flapper/guy-not-set";
        if not (self.bids[sid].tic > self.now or self.bids[sid].tic == 0):
            return "Flapper/already-finished-tic"
        if not (self.bids[sid].end > self.now):
            return "Flapper/already-finished-end"

        if not (lot == self.bids[sid].lot):
            return "Flapper/lot-not-matching"
        if not (bid >  self.bids[sid].bid):
            return "Flapper/bid-not-higher";
        if not (self.mul(bid, self.ONE) >= self.mul(self.beg, self.bids[sid].bid)):
            return "Flapper/insufficient-increase"

        if (self.msg.sender != self.bids[sid].guy):
            self.gem.move(self.message.sender, self.bids[sid].guy, self.bids[sid].bid);
            self.bids[sid].guy = self.message.sender;

        self.gem.move(self.msg.sender, id(self.message.sender), bid - self.bids[sid].bid);

        self.bids[sid].bid = bid;
        self.bids[sid].tic = self.add(self.now, self.ttl);

    def deal( self,sid):
        if not(self.live == 1):
            return "Flapper/not-live"
        if not(self.bids[sid].tic != 0 and (self.bids[sid].tic < self.now or self.bids[sid].end < self.now)):
            return "Flapper/not-finished"
        self.vat.move(sid, self.bids[sid].guy, self.bids[sid].lot);
        self.gem.burn(sid, self.bids[sid].bid);
        del self.bids[sid];


    def cage(self, rad):
       self.live = 0;
       #self.vat.move(address(this), self.message.sender, rad);

    def yank(self, sid):
        if not(self.live == 0):
            return "Flapper/still-live"
        if not (self.bids[sid].guy != 0):
            return "Flapper/guy-not-set"
        #self.gem.move(address(this), self.bids[sid].guy, self.bids[sid].bid;
        del self.bids[sid];

