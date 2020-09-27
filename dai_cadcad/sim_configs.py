""" Simulation Configurations Module

Contains cadCAD configuration objects for different simulations, along with a dummy object to
inherit from/reference.
"""

from cadCAD.configuration.utils import config_sim

from dai_cadcad import util

base_sim_config = {
    "T": range(1),
    "N": 1,
    "M": {
        "CAT_BOX": [util.float_to_rad(15000000)],
        "CAT_ETH_CHOP": [util.float_to_wad(1.13)],
        "CAT_ETH_DUNK": [util.float_to_rad(50000)],
        "FLAPPER_BEG": [1.05],
        "FLAPPER_TTL": [180],
        "FLAPPER_TAU": [2880],
        "FLIPPER_ETH_BEG": [1.05],
        "FLIPPER_ETH_TTL": [180],
        "FLIPPER_ETH_TAU": [2880],
        "FLOPPER_BEG": [1.05],
        "FLOPPER_PAD": [1.5],
        "FLOPPER_TTL": [180],
        "FLOPPER_TAU": [2880],
        "SPOTTER_PAR": [util.float_to_ray(1)],
        "SPOTTER_ETH_MAT": [util.float_to_ray(1.5)],
        "SPOTTER_ETH_PIP": ["price_feeds/eth.json"],
        "SPOTTER_DAI_PIP": ["price_feeds/dai.json"],
        "VAT_LINE": [util.float_to_rad(1000000000)],
        "VAT_ILK_ETH_RATE": [util.float_to_ray(1)],
        "VAT_ILK_ETH_LINE": [util.float_to_rad(540000000)],
        "VAT_ILK_ETH_DUST": [util.float_to_rad(100)],
        "VOW_DUMP": [util.float_to_wad(250)],
        "VOW_SUMP": [util.float_to_rad(50000)],
        "VOW_BUMP": [util.float_to_rad(10000)],
        "VOW_HUMP": [util.float_to_rad(20000)],
        "WARM_TAU": [1, 1],  # Vault-joining warmup duration
    },
}

# Note: at least one of the array fields w/in the "M" key should be of length > 1

# Otherwise, the `_params` dict gets passed in as a 1-element array to state update and policy
# functions

# This is likely a cadCAD bug

open_eth_vault_sim_config = config_sim(
    {
        **base_sim_config,
        #  **{"M": {**base_sim_config["M"], "VAT_ILK_ETH_RATE": [util.float_to_ray(1.05)]}}
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
