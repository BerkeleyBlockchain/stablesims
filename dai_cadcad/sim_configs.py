""" Simulation Configurations Module

Contains cadCAD configuration objects for different simulations, along with a dummy object to
inherit from/reference.
"""

from cadCAD.configuration.utils import config_sim

dummy_sim_config = {
    "T": range(1),
    "N": 1,
    "M": {
        "SUMP": [0],  # Fixed DAI bid for Flopper auctions
        "DUMP": [0],  # Initial MKR lot for Flopper auctions
        "BUMP": [0],  # Fixed DAI lot for Flapper auctions
        "HUMP": [0],  # Surplus DAI threshold that enables Flapper auctions
        "FLIP_BEG": [0],  # Minimum DAI bid increase
        "FLIP_TAU": [0],  # Auction duration
        "FLOP_BEG": [0],  # Minimum ETH lot decrease
        "FLOP_TAU": [0],  # Auction duration
        "FLAP_BEG": [0],  # Minimum MKR bid increase
        "FLAP_TAU": [0],  # Auction duration
        "ETH_LINE": [0],  # ETH debt ceiling
        "ETH_DUST": [0],  # ETH debt floor
        "DSR": [0],  # Dai savings rate
        "WARM_TAU": [0],  # Vault-joining warmup duration
    },
}

# Note: at least one of the array fields w/in the "M" key should be of length > 1

# Otherwise, the `_params` dict gets passed in as a 1-element array to state update and policy
# functions

# This is likely a cadCAD bug

join_bite_sim_config = config_sim(
    {
        **dummy_sim_config,
        **{
            "M": {
                "SUMP": [0],
                "DUMP": [0],
                "BUMP": [0],
                "HUMP": [0],
                "FLIP_BEG": [0],
                "FLIP_TAU": [0],
                "FLOP_BEG": [0],
                "FLOP_TAU": [0],
                "FLAP_BEG": [0],
                "FLAP_TAU": [0],
                "ETH_LINE": [0, 160000],
                "ETH_DUST": [0],
                "DSR": [0],
                "WARM_TAU": [1, 1],
            }
        },
    }
)


read_dai_price_sim_config = config_sim(
    {
        **dummy_sim_config,
        **{
            "T": range(2),
            "M": {
                "SUMP": [0],
                "DUMP": [0],
                "BUMP": [0],
                "HUMP": [0],
                "FLIP_BEG": [0],
                "FLIP_TAU": [0],
                "FLOP_BEG": [0],
                "FLOP_TAU": [0],
                "FLAP_BEG": [0],
                "FLAP_TAU": [0],
                "ETH_LINE": [0, 160000],
                "ETH_DUST": [0],
                "DSR": [0],
                "WARM_TAU": [1, 1],
            },
        },
    }
)
