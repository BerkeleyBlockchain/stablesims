""" Policies Module
    Contains the cadCAD policy functions used by the simulation, namely `dispatch`, `handle`, and
    `log`.
    `dispatch` dispatches a collection of events to happen in the current timestep.
    `handle` executes the events in a specific order (allowing for control over asynchrony)
    `log` performs any reporting or other side effects on the timesteps events (e.g. tracking stats)
"""

from copy import deepcopy


def make_call_from_action(action, state):
    """ Sample action:
        {
            "method": "vat.frob",
            "args": [i, u, v, w, dink, dart],
            "kwargs": {},
        }
    """

    state_var_name, method_name = ".".split(action["method"])
    obj = state[state_var_name]
    method = getattr(obj, method_name)
    method(*action["args"], **action["kwargs"])


def dispatch(params, substep, state_hist, state):
    state = deepcopy(state)
    signals = {"actions": {}}
    for dispatcher in params["DISPATCHERS"]:
        signals = {
            "actions": {
                **signals["actions"],
                **dispatcher(params, substep, state_hist, state)
            }
        }

    return signals


def handle(params, _substep, _state_hist, state):
    state = deepcopy(state)
    action_sort_key = params["ACTION_SORT_KEY"]
    actions = sorted(state["actions"], key=action_sort_key)
    signals = {}
    for action in actions:
        make_call_from_action(action, state)

    for state_var_name in state.keys():
        signals[state_var_name] = state[state_var_name]

    return signals


def log(params, substep, state_hist, state):
    state = deepcopy(state)
    signals = {}
    for logger in params["LOGGERS"]:
        signals = {
            **signals,
            **logger(params, substep, state_hist, state)
        }

    return signals
