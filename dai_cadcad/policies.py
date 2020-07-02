from uuid import uuid4
from constants import *
from copy import deepcopy

def make_join(eth, dai):

  def join(_params, substep, sH, s, **kwargs):

    # Assert that we don't cross the ETH debt ceiling    
    assert (s["eth_ilk"]["debt_dai"] + dai < ETH_LINE)

    # Assert that this vault will be properly collateralized
    # TODO: Consider making the collateralization ratio assertion a helper function
    spot = s["eth_ilk"]["spot_rate"]
    assert (spot * eth >= dai)
    
    # Create the new vault to be joined
    vault_id = uuid4()
    new_vault = {
      "id": vault_id,
      "eth": eth,
      "dai": dai
    }

    # Pretty sure copying is necessary here
    # TODO: Consider making a copy+merge helper function
    new_vat = deepcopy(s["vat"])
    new_vat[vault_id] = new_vault

    return { "vat": new_vat }

  return join
  
def make_bite(id):

  def bite(_params, substep, sH, s, **kwargs):

    # Assert that vault is undercollateralized
    eth = s["vat"][id]["eth"]
    dai = s["vat"][id]["dai"]
    spot = spot = s["eth_ilk"]["spot_rate"]
    assert (spot * eth >= dai)

    # Create the flipper auction to be kicked
    auction_id = uuid4()
    stability_rate = s["eth_ilk"]["stability_rate"]
    debt_to_flip = dai * stability_rate
    initial_lot = min(eth, debt_to_flip/spot)
    new_auction = {
      "id": auction_id,
      "debt_to_flip": debt_to_flip,
      "vault": id,
      "lot_eth": initial_lot,
      "bid_dai": 0,
      "bidder": "",
      "expiry": FLIP_TAU
    }

    new_flipper = deepcopy(s["flipper"])
    new_flipper[auction_id] = new_auction

    return { "flipper": new_flipper }

  return bite