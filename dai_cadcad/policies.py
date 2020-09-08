""" Policies Module

Contains the definition of the cadCAD system's policies.
Policies are typically broken down into `{{policy_name}}_all()` and `{{policy_name}}()` functions,
where the `_all()` is the actual "policy" function passed into the PSUBs, and the other is a helper
function.

The helper function typically contains the actual policy logic,
from the perspective of a single actor/action (executing the policy once).

The `_all()` typically orchestrates how many times the policy should execute, and with what options,
as well as checking the necessary conditions.
"""

from uuid import uuid4
from copy import deepcopy
import json
import random


# Price Feeds


def read_dai_price_usd(params, _substep, _state_hist, state):
    """ Reads in the DAI price in USD for the given timestep from the local price feed.
    """

    timestep = state["timestep"]
    warm_tau = params["WARM_TAU"]
    if timestep >= warm_tau:
        with open("../price_feeds/dai.json") as dai_price_feed_json:
            dai_price_usd = json.load(dai_price_feed_json)[timestep - warm_tau][
                "price_close"
            ]
        return {"dai_price_usd": dai_price_usd}
    return {}


def read_eth_price_usd(params, _substep, _state_hist, state):
    """ Reads in the ETH price in USD for the given timestep from the local price feed.
    """

    timestep = state["timestep"]
    warm_tau = params["WARM_TAU"]
    if timestep >= warm_tau:
        with open("../price_feeds/eth.json") as eth_price_feed_json:
            eth_price_usd = json.load(eth_price_feed_json)[timestep - warm_tau][
                "price_close"
            ]
        return {"eth_price_usd": eth_price_usd}
    return {}


# ---


# Vat


def flux(vat, ilk_id, src, dst, wad):
    """ Moves gem from one address to another.
    """

    vat["gem"][ilk_id][src] -= wad
    vat["gem"][ilk_id][dst] += wad


def frob(vat, ilk_id, user_id, dink, dart):
    """ Sets an urn (whether it exists or not) in the Vat.
    """

    urn = deepcopy(vat["urns"][ilk_id].get(user_id, {"ink": 0, "art": 0}))
    ilk = deepcopy(vat["ilks"][ilk_id])

    urn["ink"] += dink
    urn["art"] += dart
    ilk["Art"] += dart

    dtab = ilk["rate"] * dart
    tab = ilk["rate"] * urn["art"]

    assert dart <= 0 or (
        ilk["Art"] * ilk["rate"] <= ilk["line"] and vat["debt"] <= vat["Line"]
    )
    assert (dart <= 0 <= dink) or tab <= urn["ink"] * ilk["spot"]
    assert urn["art"] == 0 or tab >= ilk["dust"]

    vat["debt"] += dtab
    vat["gem"][ilk_id][user_id] -= dink
    vat["dai"][user_id] += dtab

    vat["urns"][ilk_id][user_id] = urn
    vat["ilks"][ilk_id] = ilk


def reduce_frob(params, _substep, _state_hist, state):
    """ Executes all `frob` operations for a timestep.
    """

    new_vat = deepcopy(state["vat"])
    dai_val = state["spotter"]["ilks"]["dai"]["val"]
    eth_val = state["spotter"]["ilks"]["eth"]["val"]

    if state["timestep"] < params["WARM_TAU"]:
        for _ in range(1000):
            # Open a vault w/ 1 ETH @ 175% collateralization
            # TODO: Associate this with an "Ideal" or "Basic" user behavior
            frob(new_vat, "eth", uuid4().hex, eth_val, eth_val * 4 / 7)
        return {"vat": new_vat}
    if dai_val > 1:
        ddai_val = dai_val - 1
        prob = 5 * ddai_val + 0.05
        if random.random() <= prob:
            frob(new_vat, "eth", uuid4().hex, eth_val, eth_val * 4 / 7)
            return {"vat": new_vat}

    return {}


def grab(vat, ilk_id, user_id, dink, dart):
    """ Confiscates a vault.
    """

    urn = vat["urns"][ilk_id][user_id]
    ilk = vat["ilks"][ilk_id]

    urn["ink"] += dink
    urn["art"] += dart
    ilk["Art"] += dart

    dtab = ilk["rate"] * dart

    vat["gem"][ilk_id]["cat"] -= dink
    vat["sin"]["vow"] -= dtab
    vat["vice"] -= dtab


# ---


# Vow


def fess(vow, tab):
    """ Pushes to the debt queue.
    """

    vow["Sin"] += tab


# ---


# Cat


def bite(vat, vow, cat, flipper, ilk_id, user_id, now):
    """ Liquidates an undercollateralized vault and puts its collateral up for a Flipper auction.
    """

    ilk = vat["ilks"][ilk_id]

    rate = ilk["rate"]
    spot = ilk["spot"]

    ink = vat["urns"][ilk_id][user_id]["ink"]
    art = vat["urns"][ilk_id][user_id]["art"]

    assert spot > 0 and ink * spot < art * rate
    assert art > 0 and ink > 0

    grab(vat, ilk_id, user_id, -ink, -art)
    fess(vow, art * rate)

    milk = cat["ilks"][ilk_id]
    tab = art * rate * milk["chop"]

    flip_kick(flipper, vat, user_id, "vow", tab, ink, 0, now + flipper["tau"])


def reduce_bite(_params, _substep, _state_hist, state):
    """ Executes all `bite` operations for a timestep.
    """

    new_vat = deepcopy(state["vat"])
    new_vow = deepcopy(state["vow"])
    new_cat = deepcopy(state["cat"])
    new_flipper = deepcopy(state["flipper"])

    for user_id in new_vat["urns"]["eth"]:

        urn = new_vat["urns"]["eth"][user_id]
        ink = urn["ink"]
        art = urn["art"]

        ilk = new_vat["ilks"]["eth"]
        rate = ilk["rate"]
        spot = ilk["spot"]

        if ink * spot < art * rate:
            bite(
                new_vat,
                new_vow,
                new_cat,
                new_flipper,
                "eth",
                user_id,
                state["timestep"],
            )

    return {"cat": new_cat, "flipper": new_flipper, "vat": new_vat, "vow": new_vow}


# ---


# Flipper


def flip_kick(flipper, vat, user_id, gal, tab, lot, bid, end):
    """ Kicks off a Flip auction.
    """

    flipper["bids"][uuid4().hex] = {
        "bid": bid,
        "lot": lot,
        "guy": "cat",
        "end": end,
        "usr": user_id,
        "gal": gal,
        "tab": tab,
    }

    flux(vat, flipper["ilk"], "cat", "flipper", lot)


# ---


# Utility


def policy_reduce(policy_signal_dict_a, policy_signal_dict_b):
    """ Reduces policy signals by merging them into one dict.

        If there is an overlap in keys, the value of `policy_signal_dict_b` is taken.
    """

    return {**policy_signal_dict_a, **policy_signal_dict_b}
