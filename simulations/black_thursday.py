""" Simulates the entirety of March 12th, 2020 (Black Thursday).
"""


from cadCAD.engine import ExecutionContext, ExecutionMode, Executor
from cadCAD.configuration import Experiment
from cadCAD import configs
from copy import deepcopy

from dai_cadcad import policies, state, sim_configs
from dai_cadcad.pymaker.numeric import Wad, Rad, Ray


def run_sim(socketio):
    """ Runs the simulation & checks the appropriate assertions.
    """

    def serialize_pymaker_numerics(state):
        if type(state) is not dict:
            if type(state) in (Wad, Rad, Ray):
                return float(state)
            return state
        for k, v in state.items():
            state[k] = serialize_pymaker_numerics(v)
        return state

    
    def stream_state(_params, _substep, _state_hist, state):
        state = deepcopy(state)
        socketio.emit('stream', serialize_pymaker_numerics(state['stats']))
        socketio.sleep(0.01)
        return {}
    

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
        {
            "policies": {
                "stream_state": stream_state
            },
            "variables": {}
        }
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
    raw_result, _tensor, _sessions = executor.execute()
