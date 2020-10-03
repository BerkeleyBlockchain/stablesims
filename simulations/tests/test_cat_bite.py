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
]

exp = Experiment()

exp.append_configs(
    sim_configs=sim_configs.cat_bite_sim_config,
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

    vat = run["vat"][8]
    old_vat = run["vat"][4]
    urn_id = list(vat["urns"]["eth"].keys())[0]
    old_urn = old_vat["urns"]["eth"][urn_id]
    old_urn_art = old_urn["art"]
    old_urn_ink = old_urn["ink"]
    urn = vat["urns"]["eth"][urn_id]
    urn_art = urn["art"]
    urn_ink = urn["ink"]
    rate = vat["ilks"]["eth"]["rate"]

    cat = run["cat"][8]
    chop = cat["ilks"]["eth"]["chop"]

    vow = run["vow"][8]

    flipper = run["flipper_eth"][8]
    bid_id = list(flipper["bids"].keys())[0]
    sample_bid = flipper["bids"][bid_id]
    tau = flipper["tau"]
    now = run["timestep"][8]

    assert vat["vice"] == Rad.from_number(1000) * Rad(rate * old_urn_art)
    assert vat["ilks"]["eth"]["Art"] == Wad(0)

    assert urn_ink == urn_art == Wad(0)

    assert cat["litter"] == Rad.from_number(1000) * Rad(old_urn_art * rate * chop)

    assert vat["sin"]["vow"] == Rad.from_number(1000) * Rad(rate * old_urn_art)
    assert vow["Sin"] == Rad.from_number(1000) * Rad(rate * old_urn_art)
    assert vow["Sin"] == Rad.from_number(1000) * Rad(rate * old_urn_art)

    assert flipper["kicks"] == 1000
    assert vat["gem"]["eth"]["flipper_eth"] == Wad.from_number(1000) * old_urn_ink

    assert sample_bid["bid"] == Rad(0)
    assert sample_bid["lot"] == old_urn_ink
    assert sample_bid["tab"] == Rad(old_urn_art * rate * chop)
    assert sample_bid["guy"] == "cat"
    assert sample_bid["gal"] == "vow"
    assert sample_bid["usr"] == urn_id
    assert sample_bid["tic"] == 0
    assert sample_bid["end"] == now + tau

    return run
