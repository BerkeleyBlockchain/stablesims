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
            state["stats"]["incentive_amount"] = Rad(0)
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


def auction_debt():
    def track_stat(state, action):
        if action["key"] == "T_START":
            state["stats"]["auction_debt"] = state["dog"].Dirt

    return track_stat
#net difference
def net_diff():
    def track_stat(state, results, action):
        if action["key"] == "T_START":
            state["stats"]["net_diff"] = Rad(0)
        elif action["key"] == "BARK":
            ilk_id = action["args"][0]
            clip = state["clippers"][ilk_id]
            tab = results[0]
            incentive = clip.tip + tab * Rad(clip.chip)
            state["stats"]["net_diff"] -= incentive
        elif action["key"] == "REDO":
            sale_id = action["args"][0]
            ilk_id = action["extra"]["ilk_id"]
            clip = state["clippers"][ilk_id]
            sale = clip.sales[sale_id]
            incentive = clip.tip + sale.tab * Rad(clip.chip)
            state["stats"]["net_diff"] -= incentive
        elif action["key"] == "TAKE":
            state["stats"]["net_diff"] += results[0]
    return track_stat


#differenceratio
def net_diff():
    def track_stat(state, results, action):
        if action["key"] == "T_START":
            state["stats"]["net_diff"] = Rad(1)
        elif action["key"] == "BARK":
            ilk_id = action["args"][0]
            clip = state["clippers"][ilk_id]
            tab = results[0]
            incentive = clip.tip + tab * Rad(clip.chip)
            state["stats"]["net_diff"] /= incentive
        elif action["key"] == "REDO":
            sale_id = action["args"][0]
            ilk_id = action["extra"]["ilk_id"]
            clip = state["clippers"][ilk_id]
            sale = clip.sales[sale_id]
            incentive = clip.tip + sale.tab * Rad(clip.chip)
            state["stats"]["net_diff"] /= incentive
        elif action["key"] == "TAKE":
            state["stats"]["net_diff"] *= results[0]
    return track_stat

#colateralization ratio
def colf():
    def track_stat(state, results, action):
        num = 0
        denom = 0
        if action["key"] == "TAKE":

            for i in results[1]:
                num+=Rad(i.ink * i.spot)
                denom+=Rad(i.art * i.rate)
            state["stats"]["col"] = num/denom
    return track_stat
