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


def ilk_price(ilk_id):
    def track_stat(state, action):
        # TODO: Constantize the action keys somewhere
        if action["key"] == "POKE":
            if not state["stats"]["ilk_price"]:
                state["stats"]["ilk_price"] = {}
            state["stats"]["ilk_price"][ilk_id] = state["vat"].ilks[ilk_id].spot

    return track_stat


def num_new_bites():
    def track_stat(state, action):
        if action["key"] == "T_START":
            state["stats"]["num_new_bites"] = 0
        elif action["key"] == "BITE":
            state["stats"]["num_new_bites"] += 1

    return track_stat


def num_new_bids():
    def track_stat(state, action):
        if action["key"] == "T_START":
            state["stats"]["num_new_bids"] = 0
        elif action["key"] == "TEND" or action["key"] == "DENT":
            state["stats"]["num_new_bids"] += 1

    return track_stat


def keeper_balances():
    def track_stat(state, action):
        if action["key"] == "T_END":
            for keeper in state["keepers"]:
                state["stats"]["keeper_balances"][keeper.ADDRESS] = {
                    ilk_id: ilk_token.balanceOf(keeper.ADDRESS)
                    for ilk_id, ilk_token in state["ilks"]
                }

    return track_stat
