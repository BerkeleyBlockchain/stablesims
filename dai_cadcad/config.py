from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim
from constants import *

initial_state = {
  "vat": {
    "vaults": {
      "dummy_vault": {
        "id": "",             # Vault ID/address
        "eth": 0,             # Vault collateralization (ETH)
        "dai": 0,             # Vault debt (DAI)
      }
    }
  },
  "vow": {
    "debt_dai": 0,            # System debt (DAI)
    "surplus_dai": 0,         # System surplus (DAI)
  },
  "flipper": {                # Tend -> dent
    "auctions": {
      "dummy_flip": {
        "debt_to_flip": 0,    # Desired amount of DAI to be raised from auction
        "vault": "",          # Vault to send remaining ETH to after dent
        "lot_eth": 0,         # Current lot (ETH)
        "bid_dai": 0,         # Current bid (DAI)
        "bidder": "",         # Current highest bidder
        "expiry": 0,          # Auction expiration timestep
      }
    }
  },
  "flopper": {                # Dent
    "auctions": {
      "dummy_flop": {
        "lot_mkr": 0,         # Current lot (MKR)
        "bid_dai": 0,         # Current bid (DAI)
        "bidder": "",         # Current highest bidder
        "expiry": 0,          # Auction expiration timestep
      }
    }
  },
  "flapper": {                # Tend
    "auctions": {
      "dummy_flap": {
        "lot_dai": 0,         # Current lot (DAI)
        "bid_mkr": 0,         # Current bid (MKR)
        "bidder": "",         # Current highest bidder
        "expiry": 0,          # Auction expiration timestep
      }
    }
  },
  "keepers": {
    "dummy_keeper": {
      "profit": 0,
      "my_profit_threshold": 0
    }
  }
}

def policy_generator(keeper_id):
  def agent_policy(_params, substep, sH, s, **kwargs):
    keeper = s["keepers"]["keeper_id"]
    # Policy logic policy logic yada yada
    # Have it use keeper.info
    # Check my profits
    # Put up a flip bid
  return agent_policy


def update_vat(_params, substep, sH, s, _input, **kwargs):
  curr_vat = s["vat"]
  
  # Read in policy signals
  # Modify appropriate vaults, record in new_vat object
  # Merge new_vat and old_vat

  # E.g. warmup policies
  # Warmup signal = { "warmup": { "vaults": { ... } } }
  # new_vat = _params["warmup"]

  return ("vat", new_vat)

def update_vow(_params, substep, sH, s, _input, **kwargs):
  curr_vow = s["vow"]

  return ("vow", new_vow)

def update_flipper(_params, substep, sH, s, _input, **kwargs):
  curr_vat = s["vat"]
  
  # Read in policy signals
  # Modify appropriate vaults, record in new_vat object
  # Merge new_vat and old_vat

  # E.g. warmup policies
  # Warmup signal = { "warmup": { "vaults": { ... } } }
  # new_vat = _params["warmup"]

  return ("vat", new_vat)

def update_flopper(_params, substep, sH, s, _input, **kwargs):
  curr_vat = s["vat"]
  
  # Read in policy signals
  # Modify appropriate vaults, record in new_vat object
  # Merge new_vat and old_vat

  # E.g. warmup policies
  # Warmup signal = { "warmup": { "vaults": { ... } } }
  # new_vat = _params["warmup"]

  return ("vat", new_vat)

def update_flapper(_params, substep, sH, s, _input, **kwargs):
  curr_vat = s["vat"]
  
  # Read in policy signals
  # Modify appropriate vaults, record in new_vat object
  # Merge new_vat and old_vat

  # E.g. warmup policies
  # Warmup signal = { "warmup": { "vaults": { ... } } }
  # new_vat = _params["warmup"]

  return ("vat", new_vat)
