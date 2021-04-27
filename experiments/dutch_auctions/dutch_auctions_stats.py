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
