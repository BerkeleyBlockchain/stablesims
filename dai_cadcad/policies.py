from uuid import uuid4
from constants import *
from copy import deepcopy


def make_join(eth, dai):

  def join(_params, substep, sH, s, **kwargs):

    # Assert that we don't cross the ETH debt ceiling    
    debt_dai = s["eth_ilk"]["debt_dai"]
    assert (debt_dai + dai < ETH_LINE)

    # Assert that this vault will be properly collateralized
    # TODO: Consider making the collateralization ratio assertion a helper function
    spot = s["eth_ilk"]["spot_rate"]
    assert (spot * eth >= dai)
    
    # Create the new vault to be joined
    vault_id = uuid4()
    new_vault = {
      "vault_id": vault_id,
      "eth": eth,
      "dai": dai
    }

    # Pretty sure copying is necessary here
    # TODO: Consider making a copy+merge helper function
    new_vat = deepcopy(s["vat"])
    new_vat[vault_id] = new_vault

    return { "vat": new_vat }

  return join


def make_bite(vault_id):

  def bite(_params, substep, sH, s, **kwargs):

    # Assert that vault is undercollateralized
    eth = s["vat"][vault_id]["eth"]
    dai = s["vat"][vault_id]["dai"]
    spot = spot = s["eth_ilk"]["spot_rate"]
    assert (spot * eth >= dai)

    # Create the flipper auction to be kicked
    # Adding it to the flipper is the same as kicking it
    flip_id = uuid4()
    stability_rate = s["eth_ilk"]["stability_rate"]
    debt_to_flip = dai * stability_rate
    # TODO: How is the initial fixed ETH lot decided?
    # Here, I assume it uses the current conversion rate
    initial_lot = min(eth, debt_to_flip/spot)
    new_auction = {
      "flip_id": flip_id,
      "phase": "tend",
      "debt_to_flip": debt_to_flip,
      "vault": vault_id,
      "lot_eth": initial_lot,
      "bid_dai": 0,
      "bidder": "",
      "expiry": FLIP_TAU
    }

    new_flipper = deepcopy(s["flipper"])
    new_flipper[flip_id] = new_auction

    return { "flipper": new_flipper }

  return bite


def make_resolve_flip_tend(flip_id):
  
  def resolve_flip_tend(_params, substep, sH, s, **kwargs):

    # Assert that flip is in tend phase
    phase = s["flipper"][flip_id]["phase"]
    assert (phase == "tend")
    
    # Assert that the debt has been covered
    # TODO: Should we actually make this assertion?
    debt_to_flip = s["flipper"][flip_id]["debt_to_flip"]
    bid_dai = s["flipper"][flip_id]["bid_dai"]
    assert (bid_dai >= debt_to_flip)

    # Reward winning bidder with lot & withdraw bid
    bidder = s["flipper"][flip_id]["bidder"]
    lot_eth = s["flipper"][flip_id]["lot_eth"]
    new_keepers = deepcopy(s["keepers"])
    new_keepers[bidder]["eth"] += lot_eth
    new_keepers[bidder]["dai"] -= bid_dai
    
    # Withdraw lot from vault
    vault_id = s["flipper"][flip_id]["vault"]
    new_vat = deepcopy(s["vat"])
    new_vat[vault_id]["eth"] -= lot_eth

    # Move flip to dent phase
    new_flipper = deepcopy(s["flipper"])
    new_flipper[flip_id]["phase"] = "dent"
    new_flipper[flip_id]["debt_to_flip"] -= bid_dai
    # TODO: How is new initial ETH lot decided?
    new_flipper[flip_id]["lot_eth"] = 0
    # TODO: How is new fixed DAU bid decided?
    new_flipper[flip_id]["bid_dai"] = 0

    return {
      "keepers": new_keepers,
      "vat": new_vat,
      "flipper": new_flipper
    }




