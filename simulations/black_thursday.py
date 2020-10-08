""" Simulates the entirety of March 12th, 2020 (Black Thursday).
"""


from cadCAD.engine import ExecutionContext, ExecutionMode, Executor
from cadCAD.configuration import Experiment
from cadCAD import configs
import pandas as pd
import matplotlib.pyplot as plt

from dai_cadcad import policies, state, sim_configs


partial_state_update_blocks = [
    {
        "policies": {"init": policies.init},
        "variables": {
            "cat": state.update_cat,
            "flapper": state.update_flapper,
            "flipper_eth": state.update_flipper_eth,
            "flopper": state.update_flopper,
            "spotter": state.update_spotter,
            "vat": state.update_vat,
            "vow": state.update_vow,
            "keepers": state.update_keepers,
        },
    },
    {
        "policies": {"tick": policies.tick},
        "variables": {
            "vat": state.update_vat,
            "spotter": state.update_spotter,
            "stats": state.update_stats,
        },
    },
    {
        "policies": {"flipper_eth_deal_generator": policies.flipper_eth_deal_generator},
        "variables": {
            "vat": state.update_vat,
            "cat": state.update_cat,
            "flipper_eth": state.update_flipper_eth,
        },
    },
    {
        "policies": {"open_eth_vault_generator": policies.open_eth_vault_generator},
        "variables": {"vat": state.update_vat},
    },
    {
        "policies": {"cat_bite_generator": policies.cat_bite_generator},
        "variables": {
            "vat": state.update_vat,
            "vow": state.update_vow,
            "cat": state.update_cat,
            "flipper_eth": state.update_flipper_eth,
            "stats": state.update_stats,
        },
    },
    {
        "policies": {
            "keeper_bid_flipper_eth_generator": policies.keeper_bid_flipper_eth_generator
        },
        "variables": {
            "vat": state.update_vat,
            "flipper_eth": state.update_flipper_eth,
            "stats": state.update_stats,
        },
    },
]

exp = Experiment()

exp.append_configs(
    sim_configs=sim_configs.black_thursday_sim_config,
    initial_state=state.initial_state,
    partial_state_update_blocks=partial_state_update_blocks,
)

exec_mode = ExecutionMode()
exec_context = ExecutionContext(context=exec_mode.single_mode)
executor = Executor(exec_context=exec_context, configs=configs)


def run_sim():
    """ Runs the simulation & checks the appropriate assertions.
    """
    raw_result, _tensor, _sessions = executor.execute()
    result = pd.DataFrame(raw_result)
    cond_1 = result["subset"] == 0
    cond_2 = result["substep"] != 0
    run = result[cond_1 & cond_2]

    time = run["timestep"][::6]
    eth_usd_feed = [
        float(spotter["ilks"]["eth"]["val"]) for spotter in run["spotter"][5::6]
    ]
    # gas_wei_feed = [float(spotter["ilks"]["gas"]["val"]) for spotter in run["spotter"][5::6]]
    num_bites_feed = [stats["num_bites"] for stats in run["stats"][5::6]]
    num_bids_feed = [stats["num_bids"] for stats in run["stats"][5::6]]

    _, ax_1_1 = plt.subplots()

    color_1 = "tab:red"
    ax_1_1.set_title("System Progression")
    ax_1_1.set_xlabel("time (10m)")
    ax_1_1.set_ylabel("ETH/USD", color=color_1)
    ax_1_1.plot(time, eth_usd_feed, color=color_1, label="ETH price")
    ax_1_1.tick_params(axis="y", labelcolor=color_1)

    ax_1_2 = ax_1_1.twinx()

    color_2 = "tab:blue"
    color_3 = "tab:green"
    ax_1_2.plot(time, num_bites_feed, color=color_2, label="# liquidations")
    ax_1_2.plot(time, num_bids_feed, color=color_3, label="# bids")
    ax_1_2.legend()

    plt.show()

    return run
