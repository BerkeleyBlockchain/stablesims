""" Stats Module for Dutch Auctions experiments.
"""

from pydss.pymaker.numeric import Rad


def num_new_barks():
    def track_stat(state, action, _results):
        if action["key"] == "T_START":
            state["stats"]["num_new_barks"] = 0
        elif action["key"] == "BARK":
            state["stats"]["num_new_barks"] += 1

    return track_stat


def num_sales_taken():
    def track_stat(state, action, _results):
        if action["key"] == "T_START":
            state["stats"]["num_sales_taken"] = 0
        elif action["key"] == "TAKE":
            state["stats"]["num_sales_taken"] += 1

    return track_stat


def incentive_amount():
    def track_stat(state, action, results):
        if action["key"] == "T_START":
            state["stats"]["incentive_amount"] = 0
        elif action["key"] == "BARK":
            ilk_id = action["args"][0]
            clip = state["clippers"][ilk_id]
            tab = results[0]
            incentive = clip.tip + tab * Rad(clip.chip)
            state["stats"]["incentive_amount"] += incentive
        elif action["key"] == "REDO":
            sale_id = action["args"][0]
            ilk_id = action["extra"]["ilk_id"]
            clip = state["clippers"][ilk_id]
            sale = clip.sales[sale_id]
            incentive = clip.tip + sale.tab * Rad(clip.chip)
            state["stats"]["incentive_amount"] += incentive

    return track_stat
