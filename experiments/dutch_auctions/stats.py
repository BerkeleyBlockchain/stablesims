""" Stats Module for Dutch Auctions experiments.
"""

from pydss.pymaker.numeric import Rad, Ray


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


def num_unsafe_vaults(ilk_id):
    def track_stat(state, action, results):
        ilk = state["vat"].ilks[ilk_id]
        if action["key"] == "T_END":
            state["stats"]["num_unsafe_vaults"] = len([
                1 for urn in state["vat"].urns[ilk_id].values()
                if ilk.spot > Ray(0) and Rad(urn.ink * ilk.spot) < Rad(urn.art * ilk.rate)
            ])

    return track_stat


def auction_debt():
    def track_stat(state, action, _results):
        if action["key"] == "T_END":
            state["stats"]["auction_debt"] = state["dog"].Dirt

    return track_stat


def avg_time_to_liquidation(ilk_id):
    unsafe_ts = {}
    liquidation_times = {}

    def is_unsafe(urn, ilk):
        return ilk.spot > Ray(0) and Rad(urn.ink * ilk.spot) < Rad(urn.art * ilk.rate)
        
    def track_stat(state, action, _results):
        if action["key"] == "T_END":
            ilk = state["vat"].ilks[ilk_id]

            for urn_address, urn in state["vat"].urns[ilk_id].items():
                if is_unsafe(urn, ilk) and urn_address not in unsafe_ts:
                    unsafe_ts[urn_address] = state["t"]
                elif urn_address in unsafe_ts and urn_address not in liquidation_times and not is_unsafe(urn, ilk):
                    del unsafe_ts[urn_address]

        if action["key"] == "BARK":
            urn_address = action["args"][1]
            liquidation_time = state["t"] - unsafe_ts[urn_address]
            liquidation_times[urn_address] = liquidation_time

            state["stats"]["avg_time_to_liquidation"] = sum(liquidation_times.values()) / len(liquidation_times)

    return track_stat
