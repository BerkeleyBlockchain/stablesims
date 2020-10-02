""" Test for the `open_eth_vault` behavior.
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
]

exp = Experiment()

exp.append_configs(
    sim_configs=sim_configs.open_eth_vault_sim_config,
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
    vat = run["vat"][2]

    assert len(vat["urns"]["eth"]) == 1000, "Incorrect # of urns created"
    sample_urn = vat["urns"]["eth"][list(vat["urns"]["eth"].keys())[0]]
    assert sample_urn["ink"] == Wad.from_number(1), "Incorrect ink amount"
    spot = run["vat"][2]["ilks"]["eth"]["spot"]
    assert sample_urn["art"] == Wad.from_number(
        float(spot) * 0.9
    ), "Incorrect art amount"

    assert len(vat["gem"]["eth"]) == 1002, "Incorrect # of gem records"
    sample_gem = vat["gem"]["eth"][list(vat["gem"]["eth"].keys())[2]]
    assert sample_gem == Wad(0), "Incorrect gem"

    assert len(vat["dai"]) == 1002, "Incorrect # of DAI records"
    sample_dai = vat["dai"][list(vat["dai"].keys())[2]]
    assert sample_dai == Rad(
        Wad.from_number(float(spot) * 0.9) * vat["ilks"]["eth"]["rate"]
    ), "Incorrect DAI amount"

    assert (
        vat["ilks"]["eth"]["Art"] == Wad.from_number(1000) * sample_urn["art"]
    ), "Incorrect total DAI from ETH"

    assert vat["debt"] == Rad.from_number(1000) * sample_dai, "Incorrect total DAI"

    return run
