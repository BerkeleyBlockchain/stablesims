""" Test for the `cat_bite` function.
"""


from cadCAD.engine import ExecutionContext, ExecutionMode, Executor
from cadCAD.configuration import Experiment
from cadCAD import configs
import pandas as pd

from dai_cadcad import policies, state, sim_configs

from dai_cadcad.pymaker.numeric import Wad, Rad


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
        "variables": {"vat": state.update_vat, "spotter": state.update_spotter,},
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
        },
    },
    {
        "policies": {
            "keeper_bid_flipper_eth_generator": policies.keeper_bid_flipper_eth_generator
        },
        "variables": {
            "vat": state.update_vat,
            "flipper_eth": state.update_flipper_eth,
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
]

exp = Experiment()

exp.append_configs(
    sim_configs=sim_configs.flip_tend_deal_sim_config,
    initial_state=state.initial_state,
    partial_state_update_blocks=partial_state_update_blocks,
)

exec_mode = ExecutionMode()
exec_context = ExecutionContext(context=exec_mode.single_mode)
executor = Executor(exec_context=exec_context, configs=configs)


def run_test():
    """ Runs the simulation & checks the appropriate assertions.
    """
    raw_result, _tensor, _sessions = executor.execute()
    result = pd.DataFrame(raw_result)
    cond_1 = result["run"] == 1
    cond_2 = result["substep"] != 0
    run = result[cond_1 & cond_2]

    post_bid_flipper = run["flipper_eth"][12]
    post_bid_spotter = run["spotter"][12]
    pre_bid_vat = run["vat"][6]
    post_bid_vat = run["vat"][12]
    post_deal_vat = run["vat"][24]
    pre_bid_cat = run["cat"][6]

    assert len(post_bid_flipper["bids"]) == 2

    placed_bid = post_bid_flipper["bids"][1]
    keeper = post_bid_flipper["bids"][1]["guy"]
    val = post_bid_spotter["ilks"]["eth"]["val"]
    spot = pre_bid_vat["ilks"]["eth"]["spot"]
    chop = pre_bid_cat["ilks"]["eth"]["chop"]

    assert placed_bid["bid"] == Rad(val) * Rad.from_number(85)
    assert placed_bid["lot"] == Wad.from_number(100)
    assert placed_bid["tab"] == Rad(Wad.from_number(float(spot) * 90) * chop)
    assert placed_bid["tic"] == 3
    assert placed_bid["end"] == 4
    assert placed_bid["usr"] == next(
        filter(lambda user: user != keeper, pre_bid_vat["urns"]["eth"].keys())
    )
    assert placed_bid["gal"] == "vow"

    assert post_bid_vat["dai"][keeper] == pre_bid_vat["dai"][keeper] - placed_bid["bid"]
    assert post_bid_vat["dai"]["vow"] == placed_bid["bid"]

    assert post_deal_vat["gem"]["eth"][keeper] == placed_bid["lot"]
    assert (
        post_deal_vat["gem"]["eth"]["flipper_eth"]
        == post_bid_vat["gem"]["eth"]["flipper_eth"] - placed_bid["lot"]
    )

    return run
