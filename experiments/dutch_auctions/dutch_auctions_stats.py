""" Stats Module for Dutch Auctions experiments.
"""


def num_new_barks():
    def track_stat(state, action):
        if action["key"] == "T_START":
            state["stats"]["num_new_barks"] = 0
        elif action["key"] == "BARK":
            state["stats"]["num_new_barks"] += 1

    return track_stat


def num_sales_taken():
    def track_stat(state, action):
        if action["key"] == "T_START":
            state["stats"]["num_sales_taken"] = 0
        elif action["key"] == "TAKE":
            state["stats"]["num_sales_taken"] += 1

    return track_stat


def net_debt():
    def track_stat(_state, _action):
        pass

    return track_stat


def incentive_bid_ratio():
    def track_stat(_state, _action):
        pass

    return track_stat


def collateralization_ratio():
    def track_stat(_state, _action):
        pass

    return track_stat


def num_redos():
    def track_stat(_state, _action):
        pass

    return track_stat
