""" Simulation Configurations Module

Contains cadCAD configuration objects for different simulations, along with a dummy object to
inherit from/reference.
"""

from cadCAD.configuration.utils import config_sim

from dai_cadcad.pymaker.numeric import Wad, Ray, Rad

base_sim_config = {
    "T": range(1),
    "N": 1,
    "M": {
        "CAT_BOX": [Rad.from_number(15000000)],
        "CAT_ETH_CHOP": [Wad.from_number(1.13)],
        "CAT_ETH_DUNK": [Rad.from_number(50000)],
        "FLAPPER_BEG": [Wad.from_number(1.05)],
        "FLAPPER_TTL": [180],  # (3 hours @ minutely timesteps)
        "FLAPPER_TAU": [2880],  # (2 days @ minutely timesteps)
        "FLIPPER_ETH_BEG": [Wad.from_number(1.05)],
        "FLIPPER_ETH_TTL": [180],
        "FLIPPER_ETH_TAU": [2880],
        "FLOPPER_BEG": [Wad.from_number(1.05)],
        "FLOPPER_PAD": [Wad.from_number(1.5)],
        "FLOPPER_TTL": [180],
        "FLOPPER_TAU": [2880],
        "SPOTTER_PAR": [Ray.from_number(1)],
        "SPOTTER_ETH_MAT": [Ray.from_number(1.5)],
        "SPOTTER_ETH_PIP": ["price_feeds/eth_black_thursday_10min.json"],
        "SPOTTER_DAI_PIP": ["price_feeds/dai_black_thursday_10min.json"],
        "SPOTTER_GAS_PIP": ["price_feeds/gas_black_thursday_10min.json"],
        "VAT_LINE": [Rad.from_number(1000000000)],
        "VAT_ILK_ETH_RATE": [Ray.from_number(1)],
        "VAT_ILK_ETH_LINE": [Rad.from_number(540000000)],
        "VAT_ILK_ETH_DUST": [Rad.from_number(100)],
        "VOW_DUMP": [Wad.from_number(250)],
        "VOW_SUMP": [Rad.from_number(50000)],
        "VOW_BUMP": [Rad.from_number(10000)],
        "VOW_HUMP": [Rad.from_number(20000)],
        "INIT_TIMESTEP": [0],
        "NUM_INIT_VAULTS": [1000],
        "dummy": [0],  # See note below
    },
}

# Note: at least one of the array fields w/in the "M" key should be of length > 1

# Otherwise, the `_params` dict gets passed in as a 1-element array to state update and policy
# functions

# This is likely a cadCAD bug

black_thursday_sim_config = config_sim(
    {
        **base_sim_config,
        **{
            "T": range(143),
            "M": {
                **base_sim_config["M"],
                "CAT_BOX": [Rad.from_number(150000000)],
                "FLIPPER_ETH_TTL": [18],
                "FLIPPER_ETH_TAU": [288],
                "NUM_INIT_VAULTS": [500],
            },
        },
    }
)

open_eth_vault_sim_config = config_sim(
    {
        **base_sim_config,
        #  **{"M": {**base_sim_config["M"], "VAT_ILK_ETH_RATE": [Ray.from_number(1.05)]}}
    }
)

cat_bite_sim_config = config_sim(
    {
        **base_sim_config,
        **{
            "T": range(2),
            "M": {
                **base_sim_config["M"],
                "SPOTTER_ETH_PIP": ["price_feeds/tests/eth_drop_half.json"],
                "SPOTTER_DAI_PIP": ["price_feeds/tests/perfect_dai_10.json"],
            },
        },
    }
)

flip_tend_deal_sim_config = config_sim(
    {
        **base_sim_config,
        **{
            "T": range(4),
            "M": {
                **base_sim_config["M"],
                "SPOTTER_ETH_PIP": ["price_feeds/tests/eth_drop_half.json"],
                "SPOTTER_DAI_PIP": ["price_feeds/tests/perfect_dai_10.json"],
                "FLIPPER_ETH_TTL": [1],
                "FLIPPER_ETH_TAU": [2],
                "NUM_INIT_VAULTS": [2],
            },
        },
    }
)
