""" Run Simultions
"""

import csv
import os
import sys
from copy import deepcopy
import numpy as np
from pydss.pymaker.numeric import Wad, Rad
from pydss.token import Token
from pydss.spot import PipLike
from experiments.dutch_auctions.experiment import DutchAuctionsExperiment
from experiments.dutch_auctions.sim import (
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
    for timeframe in [
            # "01-11-2021",
            # "01-21-2021",
            # "02-22-2021",
            "05-19-2021",
            # "06-21-2021",
            # "09-05-2020",
    ]:
        timeframe_params = deepcopy(parameters)
        timeframe_params["Spotter"]["WETH"]["pip"] = PipLike(f"feeds/eth/{timeframe}.json")
        timeframe_params["GasOracle"]["price_feed_file"] = f"feeds/gas/{timeframe}.json"
        timeframe_params["Uniswap"]["pairs"]["0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"]["path"] = f"feeds/eth_dai_liquidity/{timeframe}.json"

        swept_params = sweep(
            {
                # "Clipper.WETH.chip": [Wad.from_number(0.001), Wad.from_number(0.01), Wad.from_number(0.1)],
                # "Clipper.WETH.tip": [Rad.from_number(100), Rad.from_number(500), Rad.from_number(1000)],
                "Clipper.WETH.chip": [Wad.from_number(0.001)],
                "Clipper.WETH.tip": [Rad.from_number(100)],
            },
            timeframe_params,
        )

        DutchAuctionsSims = [
            DutchAuctionsExperiment(
                contracts,
                keepers,
                sort_actions,
                ilk_ids,
                Token,
                stat_trackers,
                params,
            )
            for params in swept_params
        ]

        fieldnames = ['WETH_price', 'gas_price_gwei', 'num_new_barks', 'num_sales_taken', 'incentive_amount', 'num_unsafe_vaults', 'auction_debt', 'avg_time_to_liquidation']

        for i, DutchAuctionsSim in enumerate(DutchAuctionsSims):
            sim_name = f"DutchAuctions_{timeframe}_{i}_{}"
            filename = f"/bab-stablesims/experiments/dutch_auctions/results/05-19-2021/{sim_name}.csv"
            with open(filename, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

            DutchAuctionsSim.run(sim_name, filename=filename, fieldnames=fieldnames)
