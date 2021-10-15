""" Stats Module
    A set of methods used to calculate statistics over the course of an
    experiment.
    Each such method is a higher-order function returning a `track_stat` method
    that takes in an Experiment object, an action key, and the address of the
    Keeper that executed said action.
    The higher-order function can take in whatever parameters it may need to
    provide to `track_stat`.
    Each `track_stat` function will be run after a Keeper executes in an action
    in a timestep, so an intended design pattern is to guard your logic in
    `track_stat` w/ a predicate that ensures you're only executing the method
    in response to a specific action you were listening for.
"""

from pydss.pymaker.numeric import Wad


def ilk_price(ilk_id):
    def track_stat(state, action, _results):
        # TODO: Constantize the action keys somewhere
        if action["key"] == "POKE":
            # if not state["stats"].get(f"{ilk_id}_price"):
            #     state["stats"][f"{ilk_id}_price"] = 0
            state["stats"][f"{ilk_id}_price"] = float(
                state["vat"].ilks[ilk_id].spot * state["spotter"].ilks[ilk_id].mat
            )

    return track_stat


def gas_price_gwei():
    def track_stat(state, action, _results):
        if action["key"] == "T_START":
            state["stats"]["gas_price_gwei"] = float(
                state["gas_oracle"].peek(state["t"]) * Wad.from_number(10 ** -9)
            )

    return track_stat


def num_new_bites():
    def track_stat(state, action, _results):
        if action["key"] == "T_START":
            state["stats"]["num_new_bites"] = 0
        elif action["key"] == "BITE":
            state["stats"]["num_new_bites"] += 1

    return track_stat


def num_bids_placed():
    def track_stat(state, action, _results):
        if action["key"] == "T_START":
            state["stats"]["num_bids_placed"] = 0
        elif action["key"] == "TEND" or action["key"] == "DENT":
            state["stats"]["num_bids_placed"] += 1

    return track_stat


def num_active_bids():
    def track_stat(state, _action, _results):
        state["stats"]["num_active_bids"] = {
            ilk_id: len(state["flippers"][ilk_id].bids) for ilk_id in state["flippers"]
        }

    return track_stat


def keeper_gem_balances():
    def track_stat(state, action, _results):
        if action["key"] == "T_END":
            if not state["stats"].get("keeper_balances"):
                state["stats"]["keeper_balances"] = {}
            for keeper_name in state["keepers"]:
                for keeper in state["keepers"][keeper_name]:
                    state["stats"]["keeper_balances"][keeper.ADDRESS] = {
                        ilk_id: state["vat"].gem[ilk_id].get(keeper.ADDRESS, 0)
                        for ilk_id in state["ilks"]
                    }

    return track_stat


def auction_debt():
    def track_stat(state, action, _results):
        if action["key"] == "T_START":
            state["stats"]["auction_debt"] = state["cat"].litter

    return track_stat
