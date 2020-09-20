""" Test for the `cat_bite` function.
"""


from cadCAD.engine import ExecutionContext, ExecutionMode, Executor
from cadCAD.configuration import Experiment
from cadCAD import configs
import pandas as pd

from dai_cadcad import policies, state, sim_configs


partial_state_update_blocks = [
    {
        "policies": {"tick": policies.tick},
        "variables": {
            "vat": state.update_vat,
            "spotter": state.update_spotter,
            "cat": state.update_cat,
            "flapper": state.update_flapper,
            "flipper_eth": state.update_flipper_eth,
            "flopper": state.update_flopper,
            "vow": state.update_vow,
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
        },
    },
]

exp = Experiment()

exp.append_configs(
    sim_configs=sim_configs.cat_bite_sim_config,
    initial_state=state.initial_state,
    partial_state_update_blocks=partial_state_update_blocks,
    # policy_ops=[policies.policy_reduce],
)

exec_mode = ExecutionMode()
exec_context = ExecutionContext(context=exec_mode.single_mode)
executor = Executor(exec_context=exec_context, configs=configs)


def run_test():
    """ Runs the simulation & checks the appropriate assertions.
    """
    raw_result, _tensor, _sessions = executor.execute()
    result = pd.DataFrame(raw_result)
    # cond_1 = result["run"] == 1
    # cond_2 = result["substep"] != 0
    # run = result[cond_1 & cond_2]

    return result
