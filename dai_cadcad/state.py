""" State Module

Contains the definition of the cadCAD system's state variables, along with dummy data as an
expected schema.
Additionally, it contains primitive state update functions (all the real logic is handled by the
policies).
"""

from dai_cadcad.pymaker.numeric import Wad, Ray, Rad


initial_state = {
    "cat": {
        "litter": Rad(0),  # Amount of DAI up for liquidation
        "box": Rad(0),  # Max DAI up for liquidation
        "ilks": {"eth": {"chop": Wad.from_number(1.13), "dunk": Rad(0)}},
    },
    "flapper": {
        "beg": Wad.from_number(1.05),  # Minimum bid increase
        "ttl": 180,  # Bid duration (3 hours @ minutely timesteps)
        "tau": 2880,  # Auction duration (2 days @ minutely timesteps)
        "kicks": 0,  # Number of auctions kicked off
        "bids": {
            "dummy_bid": {
                "bid": Wad(0),  # Current bid (MKR)
                "lot": Rad(0),  # Current lot (DAI)
                "guy": "",  # Current highest bidder
                "tic": 0,  # Current bid expiry timestep
                "end": 0,  # Auction expiry timestep
            }
        },
    },
    "flipper_eth": {
        "ilk": "eth",  # Collateral type
        "beg": Wad.from_number(1.05),  # Minimum bid increase
        "ttl": 180,  # Bid duration (3 hours @ minutely timesteps)
        "tau": 2880,  # Auction duration (2 days @ minutely timesteps)
        "kicks": 0,  # Number of auctions kicked off
        "bids": {
            "dummy_bid": {  # Called a "bid" but really it's a Flipper auction
                "bid": Rad(0),  # Current bid (DAI)
                "lot": Wad(0),  # Current lot (COLLAT)
                "guy": "",  # Current highest bidder
                "tic": 0,  # Current bid expiry timestep
                "end": 0,  # Auction expiry timestep
                "usr": "",  # ID of urn being auctioned
                "gal": "vow",  # Recipient of bid (vow) (TOREMOVE?)
                "tab": Rad(0),  # Desired amount of DAI to be raised
            }
        },
    },
    "flopper": {  # Dent
        "beg": Wad.from_number(1.05),  # Minimum bid increase
        "pad": 1.5,  # Lot increase per timestep
        "ttl": 180,  # Bid duration (3 hours @ minutely timesteps)
        "tau": 2880,  # Auction duration (2 days @ minutely timesteps)
        "kicks": 0,  # Number of auctions kicked off
        "bids": {
            "dummy_bid": {
                "bid": Rad(0),  # Current bid (DAI)
                "lot": Wad(0),  # Current lot (MKR)
                "guy": "",  # Current highest bidder
                "tic": 0,  # Current bid expiry timestep
                "end": 0,  # Auction expiry timestep
            }
        },
    },
    "keepers": {  # (TOREMOVE?)
        "dummy_keeper": {
            "dai": 0,  # DAI balance
            "eth": 0,  # ETH balance
            "mkr": 0,  # MKR balance
            "flip_tolerance": 0,  # (TODO)
            "flop_tolerance": 0,  # (TODO)
            "flap_tolerance": 0,  # (TODO)
        }
    },
    "spotter": {
        "par": 1,  # Target price of DAI (USD/DAI)
        "ilks": {
            "eth": {
                "pip": "price_feeds/eth.json",  # Price feed file
                "val": Wad(0),  # Current USD price (cached for efficiency) (CUSTOM)
                "mat": Ray.from_number(1.5),  # Liquidation ratio
            },
            "dai": {  # DAI isn't an ilk but it makes the most sense to store price here
                "pip": "price_feeds/dai.json",
                "val": Wad(1),
                "mat": Ray.from_number(1),
            },
        },
    },
    "vat": {
        "sin": {"vow": Rad(0),},  # Unbacked DAI (system debt)
        "dai": {"daijoin": Rad(0), "vow": Rad(0),},  # Debt ledger
        "gem": {"eth": {"cat": Wad(0), "flipper_eth": Wad(0),}},  # Collateral ledger
        "debt": Rad(0),  # Total DAI issued
        "vice": Rad(0),  # Total unbacked DAI
        "Line": Rad(0),  # Total debt ceiling
        "urns": {  # Vaults
            "eth": {
                "dummy_urn": {
                    "ink": Wad(0),  # Vault collateral balance
                    "art": Wad(0),  # Vault debt (DAI)
                }
            }
        },
        "ilks": {
            "eth": {
                "Art": Wad(0),  # Total debt (DAI)
                "rate": Ray(1),  # Accumulated stability fee rates
                "spot": Ray(
                    0
                ),  # Collateral price w/ safety margin (max DAI per unit of collateral)
                "line": Rad(0),  # Debt ceiling for ilk
                "dust": Rad(0),  # Debt floor for ilk
            }
        },
    },
    "vow": {
        "Sin": Rad(0),  # Amount of debt queued
        "Ash": Rad(0),  # Amount of debt on auction
        "dump": Wad(0),  # Flop initial lot size
        "sump": Rad(0),  # Flop fixed bid size
        "bump": Rad(0),  # Flap fixed lot size
        "hump": Rad(0),  # Surplus buffer
    },
}


def update_cat(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `cat` state variable.
    """

    new_cat = policy_signals.get("cat", state["cat"])
    return ("cat", new_cat)


def update_flapper(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `flapper` state variable.
    """

    new_flapper = policy_signals.get("flapper", state["flapper"])
    return ("flapper", new_flapper)


def update_flipper_eth(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `flipper_eth` state variable.
    """

    new_flipper_eth = policy_signals.get("flipper_eth", state["flipper_eth"])
    return ("flipper_eth", new_flipper_eth)


def update_flopper(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `flopper` state variable.
    """

    new_flopper = policy_signals.get("flopper", state["flopper"])
    return ("flopper", new_flopper)


def update_keepers(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `keepers` state variable.
    """

    new_keepers = policy_signals.get("keepers", state["keepers"])
    return ("keepers", new_keepers)


def update_spotter(_params, _substep, _state_hist, state, policy_signals):
    """ Updates `spotter` state variable.
    """

    new_spotter = policy_signals.get("spotter", state["spotter"])
    return ("spotter", new_spotter)


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
