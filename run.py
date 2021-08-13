""" Run Simultions
sim="[SIM_NAME]" python3 run.py
"""

import os
import sys
from copy import deepcopy
import ipdb
from experiments.dutch_auctions.dutch_auctions_experiment import DutchAuctionsExperiment
from experiments.dutch_auctions.dutch_auctions_bear_sim import (
    contracts,
    keepers,
    sort_actions,
    ilk_ids,
    stat_trackers,
    parameters,
)


def sweep(paramPaths, initParameters):
    """
    {
        "Clipper.WETH.chip": [...],
        "Clipper.WETH.tip": [...],
    }
    """
    ipdb.set_trace()
    numParamObjs = len(list(paramPaths.values())[0])
    paramObjs = [deepcopy(initParameters) for _ in range(numParamObjs)]

    for i, paramObj in enumerate(paramObjs):
        for item in paramPaths.items():
            param = paramObj
            paramPath = item[0].split(".")
            for pathSegment in paramPath:
                param = param[pathSegment]
            param = item[1][i]
    return paramObjs

def run(sim):
    if sim == "DutchAuctionsBear":
        DutchAuctionsBear.run()


if __name__ == "__main__":
    # sim = os.getenv("sim")

    # if not (sim):
    #     print("Please enter simulation name ")
    #     sys.exit()

    # run(sim)
    paramObjs = sweep({
        "Clipper.WETH.chip": [0.03, 0.05, 0.08],
        "Clipper.WETH.tip": [10, 100, 1000]
    }, parameters)
    print(paramObjs)
