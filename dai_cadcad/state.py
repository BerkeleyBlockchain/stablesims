initial_state = {
  "vat": {
    "dummy_vault": {
      "vault_id": "",         # Vault ID
      "eth": 0,               # Vault collateralization (ETH)
      "dai": 0,               # Vault debt (DAI)
    }
  },
  "vow": {
    "debt_dai": 0,            # System debt (DAI)
    "surplus_dai": 0,         # System surplus (DAI)
  },
  "flipper": {                # Tend -> dent
    "dummy_flip": {
      "flip_id": "",          # Auction ID
      "phase": "",            # Auction phase ("tend" or "dent")
      "debt_to_flip": 0,      # Desired amount of DAI to be raised from auction
      "vault": "",            # Vault to send remaining ETH to after dent
      "lot_eth": 0,           # Current lot (ETH)
      "bid_dai": 0,           # Current bid (DAI)
      "bidder": "",           # Current highest bidder
      "expiry": 0,            # Auction expiration timestep
    }
  },
  "flapper": {                # Tend
    "dummy_flap": {
      "flap_id": "",          # Auction ID
      "lot_dai": 0,           # Current lot (DAI)
      "bid_mkr": 0,           # Current bid (MKR)
      "bidder": "",           # Current highest bidder
      "expiry": 0,            # Auction expiration timestep
    }
  },
  "flopper": {                # Dent
    "dummy_flop": {
      "flop_id": "",          # Auction ID
      "lot_mkr": 0,           # Current lot (MKR)
      "bid_dai": 0,           # Current bid (DAI)
      "bidder": "",           # Current highest bidder
      "expiry": 0,            # Auction expiration timestep
    }
  },
  "keepers": {
    "dummy_keeper": {
      "keeper_id": "",        # Keeper ID
      "dai": 0,               # DAI balance
      "eth": 0,               # ETH balance
      "mkr": 0,               # MKR balance
      "flip_tolerance": 0,    # (TODO)
      "flop_tolerance": 0,    # (TODO)
      "flap_tolerance": 0     # (TODO)
    }
  },
  "eth_ilk": {
    "debt_dai": 0,            # Total amount of DAI collateralized by ETH
    "spot_rate": 0,           # Conversion rate (max amount of DAI per ETH)
    "stability_rate": 0       # Stability fee rate
  },
}

def update_vat(_params, substep, sH, s, _input, **kwargs):
  curr_vat = s["vat"]
  # Set new_vat
  return ("vat", new_vat)

def update_vow(_params, substep, sH, s, _input, **kwargs):
  curr_vow = s["vow"]
  # Set new_vow
  return ("vow", new_vow)

def update_flipper(_params, substep, sH, s, _input, **kwargs):
  curr_flipper = s["flipper"]
  # Set new_flipper
  return ("flipper", new_flipper)

def update_flopper(_params, substep, sH, s, _input, **kwargs):
  curr_flopper = s["flopper"]
  # Set new_flopper
  return ("flopper", new_flopper)

def update_flapper(_params, substep, sH, s, _input, **kwargs):
  curr_flapper = s["flapper"]
  # Set new_flapper
  return ("flapper", new_flapper)

def update_keepers(_params, substep, sH, s, _input, **kwargs):
  curr_keepers = s["keepers"]
  # Set new_keepers
  return ("keepers", new_keepers)

def update_eth_ilk(_params, substep, sH, s, _input, **kwargs):
  curr_eth_ilk = s["eth_ilk"]
  # Set new_eth_ilk
  return ("eth_ilk", eth_ilk)
