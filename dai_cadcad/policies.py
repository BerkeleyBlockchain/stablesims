from uuid import uuid4
from constants import *
from copy import deepcopy


# Vat

def make_join(eth, dai):

  def join(_params, substep, sH, s, **kwargs):

    debt_dai = s["eth_ilk"]["debt_dai"]
    assert (debt_dai + dai < ETH_LINE)
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


# Cat

def make_bite(vault_id):

  def bite(_params, substep, sH, s, **kwargs):

    eth = s["vat"][vault_id]["eth"]
    dai = s["vat"][vault_id]["dai"]
    spot = spot = s["eth_ilk"]["spot_rate"]
    assert (spot * eth >= dai)

    # Create the flipper auction to be kicked
    # Adding it to the flipper is the same as kicking it
    flip_id = uuid4()
    stability_rate = s["eth_ilk"]["stability_rate"]
    debt_to_flip = dai * stability_rate
    new_flip = {
      "flip_id": flip_id,
      "phase": "tend",
      "debt_to_flip": debt_to_flip,
      "vault": vault_id,
      "lot_eth": eth,
      "bid_dai": 0,
      "bidder": "",
      "expiry": FLIP_TAU
    }

    new_flipper = deepcopy(s["flipper"])
    new_flipper[flip_id] = new_flip

    return { "flipper": new_flipper }

  return bite


# Flipper

def make_flip_tend(flip_id, bid, keeper_id):

  def flip_tend(_params, substep, sH, s, **kwargs):
    
    # TODO: Check that `flip` exists?
    
    flip = s["flipper"][flip_id]

    # TODO: Check that `flip` has not expired?

    phase = flip["phase"]
    assert (phase == "tend")
    bid_dai = flip["bid_dai"]
    assert (bid > bid_dai * FLIP_BEG)
    # Not sure why we don't want to raise more, but this is from the smart contract
    # https://github.com/makerdao/dss/blob/master/src/flip.sol
    debt_to_flip = flip["debt_to_flip"]
    assert (bid <= debt_to_flip)

    new_flipper = deepcopy(s["flipper"])
    new_flip = new_flipper[flip_id]
    new_flip["bid_dai"] = bid
    new_flip["bidder"] = keeper_id
    if (bid == debt_to_flip):
      new_flip["phase"] = "dent"
    # TODO: Should timekeeping be handled here?
    new_flip["expiry"] -= 1

    return { "flipper": new_flipper }
  
  return flip_tend


def make_flip_dent(flip_id, lot, keeper_id):

  def flip_dent(_params, substep, sH, s, **kwargs):

    flip = s["flipper"][flip_id]

    lot_eth = flip["lot_eth"]
    assert (lot < lot_eth * FLIP_BEG)

    new_flipper = deepcopy(s["flipper"])
    new_flip = new_flipper[flip_id]
    new_flip["lot_eth"] = lot
    new_flip["bidder"] = keeper_id
    new_flip["expiry"] -= 1

    return { "flipper": new_flipper }

  return flip_dent


def make_flip_deal(flip_id, keeper_id):

  def flip_deal(_params, substep, sH, s, **kwargs):

    flip = s["flipper"][flip_id]

    expiry = flip["expiry"]
    assert (expiry == 0)

    # Move lot to bidder (remaining eth left in user vault)
    new_vat = deepcopy(s["vat"])
    new_vault = new_vat[flip["vault"]]
    lot = flip["lot_eth"]
    new_vault["eth"] -= lot
    # TODO: Should vault cleanup logic be handled here?
    new_keepers = deepcopy(s["keepers"])
    new_keeper = new_keepers[flip["bidder"]]
    new_keeper["eth"] += lot

    # Move bid to vow surplus
    new_vow = deepcopy(s["vow"])
    bid = flip["bid_dai"]
    new_vow["surplus_dai"] += bid
    new_keeper["dai"] -= bid

    return { "vat": new_vat, "keepers": new_keepers, "vow": new_vow }
  
  return flip_deal


# Flapper

def make_flap_tend(flap_id, bid, keeper_id):

  def flap_tend(_params, substep, sH, s, **kwargs):
    
    flap = s["flapper"][flap_id]

    bid_mkr = flap["bid_mkr"]
    assert (bid > bid_mkr * FLAP_BEG)

    new_flapper = deepcopy(s["flapper"])
    new_flap = new_flapper[flap_id]
    new_flap["bid_mkr"] = bid
    new_flap["bidder"] = keeper_id
    new_flap["expiry"] -= 1

    return { "flapper": new_flapper }

  return flap_tend


# Flopper

def make_flop_dent(flop_id, lot, keeper_id):

  def flop_dent(_params, substep, sH, s, **kwargs):

    flop = s["flopper"][flop_id]

    lot_mkr = flop["lot_mkr"]
    assert (lot < lot_mkr * FLOP_BEG)

    new_flopper = deepcopy(s["flopper"])
    new_flop = new_flopper[flop_id]
    new_flop["lot_mkr"] = lot
    new_flop["bidder"] = keeper_id
    new_flop["expiry"] -= 1

    return { "flopper": new_flopper }

  return flop_dent

