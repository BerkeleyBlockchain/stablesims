""" Run Simultions
sim="[SIM_NAME]" python3 run.py
"""

import os
import sys
from copy import deepcopy
import numpy as np
from pydss.pymaker.numeric import Wad, Rad
from pydss.token import Token
from experiments.dutch_auctions.dutch_auctions_experiment import DutchAuctionsExperiment
from experiments.dutch_auctions.dutch_auctions_bear_sim import (
    contracts,
    keepers,
    sort_actions,
    ilk_ids,
    stat_trackers,
    parameters,
)

if __name__ == "__main__":
    sim_name = os.getenv("sim")

    if not sim_name:
        print("Please enter simulation name ")
        sys.exit()

    run(sim_name)


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


def run(sim):
    if sim == "DutchAuctionsBear":
        paramObjs = sweep(
            {
                "Clipper.WETH.chip": [Wad.from_number(0.08), Wad.from_number(0.10),],
                "Clipper.WETH.tip": [Rad.from_number(500), Rad.from_number(1000),],
            },
            parameters,
        )

        DutchAuctionsBearSims = [
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

        for i, DutchAuctionsBearSim in enumerate(DutchAuctionsBearSims):
            DutchAuctionsBearSim.run(f"DutchAuctionsBear_{i}")
