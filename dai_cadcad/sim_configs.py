""" Simulation Configurations Module

Contains cadCAD configuration objects for different simulations, along with a dummy object to
inherit from/reference.
"""

from cadCAD.configuration.utils import config_sim

base_sim_config = {
    "T": range(1),
    "N": 1,
    "M": {
        "CAT_ETH_CHOP": [1.13],
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
        "SPOTTER_PAR": [1],
        "SPOTTER_ETH_MAT": [1.5],
        "VAT_LINE": [948000000],
        "VAT_ILK_ETH_RATE": [1],
        "VAT_ILK_ETH_LINE": [540000000],
        "VAT_ILK_ETH_DUST": [100],
        "VOW_DUMP": [250],
        "VOW_SUMP": [50000],
        "VOW_BUMP": [10000],
        "VOW_HUMP": [20000],
        "WARM_TAU": [1, 1],  # Vault-joining warmup duration
    },
}

# Note: at least one of the array fields w/in the "M" key should be of length > 1

# Otherwise, the `_params` dict gets passed in as a 1-element array to state update and policy
# functions

# This is likely a cadCAD bug

open_eth_vault_sim_config = config_sim(
    {**base_sim_config, **{"M": {**base_sim_config["M"], "VAT_ILK_ETH_RATE": [1.05]}}}
)
