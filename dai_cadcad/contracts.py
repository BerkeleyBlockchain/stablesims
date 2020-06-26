class Vat():
    def __init__(self):
        self.vaults = {}

    def get_vault(self, vault_id):
        return self.vaults[vault_id]

    def create_vault(self, vault_id, collat, debt):
        self.vaults[vault_id] = Vault(vault_id, collat, debt)

    def delete_vault(self, vault_id):
        del self.vaults[vault_id]


class Cat():
    def bite(self, vault_id, vat, vow, flipper):
        vault = vat.get_vault(vault_id)
        vat.delete_vault(vault_id)
        vow.add_vault(vault)
        flipper.start_auction(vault_id, vow)


class Vault():
    def __init__(self, collat, debt):
        self.vault_id = uuid()
        self.collat = collat
        self.debt = debt
        # Risk parameters (collat. ratio, debt ceilings, savings/stability rates)

    def get_collat(self):
        pass


class Vow():
    def __init__(self):
        self.vaults = {}
        self.debt = 0
        self.surplus = 0
        # Auction parameters (hump, bump, dump, sump)

    def get_vault(self, vault_id):
        return self.vaults[vault_id]

    def add_vault(self, vault):
        self.vaults[Vault.vault_id] = vault


class Auction():
    def __init__(self, expiry, bid, lot, auction_type):
        self.auction_id = uuid()
        self.expiry = expiry
        self.bid = bid
        self.lot = lot
        self.type = auction_type
        self.highest_bidder = ""

    def expired(self):
      pass
      # return self.duration >= self.expiry


class TendAuction(Auction):
  def accept_bid(self, bid, vault_id):
    # does assert belong in policy function?
    assert bid > self.bid
    assert self.expired() == False
    # assert bid - self.bid > FLOP_BEG/FLAP_BEG
    self.bid = bid
    self.highest_bidder = vault_id

  def end_auction(self):
    assert self.expired()
    # send lot (DAI) to self.highest_bidder
    # burn self.bid


class DentAuction(Auction):
   def accept_bid(self, lot, vault_id):
    # does assert belong in policy function?
    assert lot < self.lot
    assert self.expired() == False
    # assert self.bid - bid > FLOP_BEG/FLAP_BEG
    self.lot = lot
    self.highest_bidder = vault_id

  def end_auction(self):
    assert self.expired()
    # send lot (MKR) to self.highest_bidder
    # burn self.bid 

# class AuctionHouse():

class Flipper():
    def __init__(self):
        self.auctions = {}
        self.bid_exp = 0
        self.auction_exp = 0
        self.min_bid_incr = 0 # Tend
        self.min_lot_decr = 0 # Dent

    def get_auction(self, id):
        return self.auctions[id]

    def start_auction(self, vault_id, vow):
        vault = vow.get_vault(vault_id)
        auction = Auction(0, Dai(self.min_bid_incr), vault.get_collat(), "tend")
        self.kick_tend(id)
        self.kick_tend(id)
    
    def kick_tend(self, id):
        auction = self.get_auction(id)

    def kick_tend(self):
       auction = self.get_auction(id)
        # TODO: how to instantiate 2 different types of auctions

class Flopper():
    def __init__(self):
        self.auctions = []
        self.bid_exp = 0
        self.auction_exp = 0
        self.min_lot_decr = 0 # Dent
        self.debt_limit = 0

        def start_auction(self, vault_id, vow):
          vault = vow.get_vault(vault_id)
          auction = DentAuction(0, Dai(), vow.get_debt(), "dent")
          self.kick_dent(id)
          
        
        def kick_dent(self):
          auction = self.get_auction(id)



class Flapper():
    def __init__(self):
        self.auctions = []
        self.bid_exp = 0
        self.auction_exp = 0
        self.min_bid_incr = 0 # Tend

        def start_auction(self, vault_id, vow):
          vault = vow.get_vault(vault_id)
          auction = TendAuction(0, MKR(), vow.get_surplus(), "tend")
          self.kick_dent(id)
        
        def kick_dent(self):
          auction = self.get_auction(id)

