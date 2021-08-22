""" Run Simultions
sim="[SIM_NAME]" python3 run.py
"""

import os
import sys
from copy import deepcopy
import numpy as np
from pydss.pymaker.numeric import Wad, Rad
from pydss.token import Token
from pydss.spot import PipLike
from experiments.dutch_auctions.dutch_auctions_experiment import DutchAuctionsExperiment
from experiments.dutch_auctions.dutch_auctions_sim import (
    contracts,
    keepers,
    sort_actions,
    ilk_ids,
    stat_trackers,
    parameters,
)


def sweep(param_paths, init_parameters):
    """
    {
        "Clipper.WETH.chip": [...],
        "Clipper.WETH.tip": [...],
    }
    """
    final_param_values = zip(
        param_paths.keys(),
        np.array(np.meshgrid(*list(param_paths.values()))).reshape(
            len(param_paths), -1
        ),
    )

    for param_path, out_arr in final_param_values:
        param_paths[param_path] = list(out_arr)

    num_param_objs = len(list(param_paths.values())[0])
    param_objs = [deepcopy(init_parameters) for _ in range(num_param_objs)]

    for i, param_obj in enumerate(param_objs):
        for item in param_paths.items():
            param = param_obj
            param_path = item[0].split(".")
            for path_segment in param_path[: len(param_path) - 1]:
                param = param[path_segment]
            param[param_path[-1]] = item[1][i]
    return param_objs


if __name__ == "__main__":
    def run():
    paramObjs = sweep(
        {
            "Spotter.WETH.pip": [PipLike("price_feeds/eth_bear_10min.json")],
            "GasOracle.price_feed_file": ["price_feeds/gas/gas_bear_10min.json"],
            "Uniswap.pairs.0xa478c2975ab1ea89e8196811f51a7b7ade33eb11.path": ["price_feeds/eth_dai_bear_liquidity_10m.json"]
            "Clipper.WETH.chip": [Wad.from_number(0)],
            "Clipper.WETH.tip": [Rad.from_number(0)],
        },
        parameters,
    )

    DutchAuctionsSims = [
        DutchAuctionsExperiment(
            contracts,
            keepers,
            sort_actions,
            ilk_ids,
            Token,
            stat_trackers,
            paramObj,
        )
        for paramObj in paramObjs
    ]

    for i, DutchAuctionsSim in enumerate(DutchAuctionsSims):
        DutchAuctionsSim.run(f"DutchAuctions_{i}")
