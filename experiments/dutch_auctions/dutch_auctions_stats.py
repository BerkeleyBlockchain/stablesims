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
    def track_stat(state, action, results):
        if action["key"] == "T_START":
            state["stats"]["auction_debt"] = state["dog"].Dirt

    return track_stat
#net difference
def net_difference():
    def track_stat(state, results, action):

        if action["key"] == "T_START" and "net_difference" not in state["stats"]:
            state["stats"]["net_difference"]["cumulative_incentive"] = Rad(0)
            state["stats"]["net_difference"]["cumulative_bid"] = Rad(0)
            state["stats"]["net_difference"]["cumulative_ratio"] = Rad(0)
            state["stats"]["started"] = True
        elif action["key"] == "BARK":
            ilk_id = action["args"][0]
            clip = state["clippers"][ilk_id]
            tab = results[0]
            state["stats"]["net_difference"]["cumulative_incentive"] \
                += clip.tip + tab * Rad(clip.chip)
            state["stats"]["net_difference"]["cumulative_ratio"] = \
                state["stats"]["net_difference"]["cumulative_bid"] \
                - state["stats"]["net_difference"]["cumulative_incentive"]
        elif action["key"] == "REDO":
            sale_id = action["args"][0]
            ilk_id = action["extra"]["ilk_id"]
            clip = state["clippers"][ilk_id]
            sale = clip.sales[sale_id]
            state["stats"]["net_difference"]["cumulative_incentive"] \
                += clip.tip + sale.tab * Rad(clip.chip)
            state["stats"]["net_difference"]["cumulative_ratio"] \
                = state["stats"]["net_difference"]["cumulative_bid"] \
                - state["stats"]["net_difference"]["cumulative_incentive"]
        elif action["key"] == "TAKE":
            state["stats"]["net_difference"]["cumulative_bid"] += results[0]
            if state["stats"]["net_difference"]["cumulative_incentive"] == 0:
                return 0
            state["stats"]["net_difference"]["cumulative_ratio"] \
                = state["stats"]["net_difference"]["cumulative_bid"] \
                - state["stats"]["net_difference"]["cumulative_incentive"]
    return track_stat


#differenceratio
def difference_ratio():
    def track_stat(state, results, action):

        if action["key"] == "T_START" and "difference_ratio" not in state["stats"]:
            state["stats"]["difference_ratio"]["cumulative_incentive"] = Rad(0)
            state["stats"]["difference_ratio"]["cumulative_bid"] = Rad(0)
            state["stats"]["difference_ratio"]["cumulative_ratio"] = Rad(0)
        elif action["key"] == "BARK":
            ilk_id = action["args"][0]
            clip = state["clippers"][ilk_id]
            tab = results[0]
            state["stats"]["difference_ratio"]["cumulative_incentive"]\
                += clip.tip + tab * Rad(clip.chip)
            state["stats"]["difference_ratio"]["cumulative_ratio"] = \
                state["stats"]["difference_ratio"]["cumulative_bid"]\
                / state["stats"]["difference_ratio"]["cumulative_incentive"]
        elif action["key"] == "REDO":
            sale_id = action["args"][0]
            ilk_id = action["extra"]["ilk_id"]
            clip = state["clippers"][ilk_id]
            sale = clip.sales[sale_id]
            state["stats"]["difference_ratio"]["cumulative_incentive"]\
                += clip.tip + sale.tab * Rad(clip.chip)
            state["stats"]["difference_ratio"]["cumulative_ratio"] \
                = state["stats"]["difference_ratio"]["cumulative_bid"] \
                / state["stats"]["difference_ratio"]["cumulative_incentive"]
        elif action["key"] == "TAKE":
            state["stats"]["difference_ratio"]["cumulative_bid"] += results[0]
            if state["stats"]["difference_ratio"]["cumulative_incentive"] == 0:
                return 0
            state["stats"]["difference_ratio"]["cumulative_ratio"] \
                = state["stats"]["difference_ratio"]["cumulative_bid"] \
                / state["stats"]["difference_ratio"]["cumulative_incentive"]
    return track_stat

#colateralization ratio
def collateralization_ratio():
    def track_stat(state, results, action):
        num = 0
        denom = 0
        if action["key"] == "TAKE":

            for i in state["vat"]["urns"]:
                num += Rad(i.ink * i.spot)
                denom += Rad(i.art * i.rate)
            state["stats"]["col"] = num/denom
    return track_stat
