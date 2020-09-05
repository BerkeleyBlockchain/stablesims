""" State Module

Contains the definition of the cadCAD system's state variables, along with dummy data as an
expected schema.
Additionally, it contains primitive state update functions (all the real logic is handled by the
policies).
"""

initial_state = {
    "cat": {"ilks": {"eth": {"chop": 1.13}}},  # Liquidation penalty rate
    "flapper": {
        "beg": 1.05,  # Minimum bid increase
        "tau": 2880,  # Auction duration (2 days @ minutely timesteps)
        "bids": {
            "dummy_bid": {
                "id": "dummy_bid",  # Bid ID (TOREMOVE?)
                "bid": 0,  # Current bid (MKR)
                "lot": 0,  # Current lot (DAI)
                "guy": "",  # Current highest bidder
                "end": 0,  # Auction expiry timestep
            }
        },
    },
    "flipper": {
        "beg": 1.05,  # Minimum bid increase
        "tau": 2880,  # Auction duration (2 days @ minutely timesteps)
        "bids": {
            "dummy_bid": {  # Called a "bid" but really it's a Flipper auction
                "id": "dummy_bid",  # Bid ID (TOREMOVE?)
                "bid": 0,  # Current bid (DAI)
                "lot": 0,  # Current lot (COLLAT)
                "guy": "",  # Current highest bidder
                "end": 0,  # Auction expiry timestep
                "usr": "",  # ID of urn being auctioned
                "gal": "vow",  # Recipient of bid (vow) (TOREMOVE?)
                "tab": 0,  # Desired amount of DAI to be raised
            }
        },
    },
    "flopper": {  # Dent
        "beg": 1.05,  # Minimum bid increase
        "pad": 1.5,  # Lot increase per timestep
        "tau": 2880,  # Auction duration (2 days @ minutely timesteps)
        "bids": {
            "dummy_bid": {
                "id": "",  # Bid ID (TOREMOVE?)
                "bid": 0,  # Current bid (DAI)
                "lot": 0,  # Current lot (MKR)
                "guy": "",  # Current highest bidder
                "end": 0,  # Auction expiry timestep
            }
        },
    },
    "keepers": {  # (TOREMOVE?)
        "dummy_keeper": {
            "keeper_id": "",  # Keeper ID
            "dai": 0,  # DAI balance
            "eth": 0,  # ETH balance
            "mkr": 0,  # MKR balance
            "flip_tolerance": 0,  # (TODO)
            "flop_tolerance": 0,  # (TODO)
            "flap_tolerance": 0,  # (TODO)
        }
    },
    "spotter": {},  # TODO
    "vat": {
        "sin": {"vow": 0,},  # System debt
        "dai": {"vow": 0,},  # System surplus
        "debt": 0,  # Total DAI issued
        "urns": {  # Vaults
            "dummy_urn": {
                "id": "dummy_urn",  # Vault ID (TOREMOVE?)
                "ink": 0,  # Vault collateral balance
                "art": 0,  # Vault debt (DAI)
                "bitten": False,  # Whether or not the vault has been bitten (CUSTOM) (TOREMOVE?)
            }
        },
        "ilks": {
            "eth": {
                "Art": 0,  # Total debt (DAI)
                "rate": 1,  # Accumulated stability fee rates
                "spot": 0,  # Collateral price w/ safety margin (max DAI per unit of collateral)
                "line": 0,  # Debt ceiling for ilk
                "dust": 0,  # Debt floor for ilk
            }
        },
    },
    "vow": {
        "dump": 0,  # Flop initial lot size
        "sump": 0,  # Flop fixed bid size
        "bump": 0,  # Flap fixed lot size
        "hump": 0,  # Surplus buffer
    },
}


def update_vat(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `vat` state variable.
    """

    new_vat = policy_signals.get("vat", state["vat"])
    return ("vat", new_vat)


def update_vow(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `vow` state variable.
    """

    new_vow = policy_signals.get("vow", state["vow"])
    return ("vow", new_vow)


def update_flipper(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `flipper` state variable.
    """

    new_flipper = policy_signals.get("flipper", state["flipper"])
    return ("flipper", new_flipper)


def update_flopper(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `flopper` state variable.
    """

    new_flopper = policy_signals.get("flopper", state["flopper"])
    return ("flopper", new_flopper)


def update_flapper(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `flapper` state variable.
    """

    new_flapper = policy_signals.get("flapper", state["flapper"])
    return ("flapper", new_flapper)


def update_keepers(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `keepers` state variable.
    """

    new_keepers = policy_signals.get("keepers", state["keepers"])
    return ("keepers", new_keepers)


def update_eth_ilk(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `eth_ilk` state variable.
    """

    new_eth_ilk = policy_signals.get("eth_ilk", state["eth_ilk"])
    return ("eth_ilk", new_eth_ilk)


def update_eth_price_usd(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `eth_price_usd` state variable.
    """

    new_eth_price_usd = policy_signals.get("eth_price_usd", state["eth_price_usd"])
    return ("eth_price_usd", new_eth_price_usd)


def update_dai_price_usd(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `dai_price_usd` state variable.
    """

    new_dai_price_usd = policy_signals.get("dai_price_usd", state["dai_price_usd"])
    return ("dai_price_usd", new_dai_price_usd)
