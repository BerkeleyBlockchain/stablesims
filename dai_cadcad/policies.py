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


# ---


# Behaviors


def open_eth_vault(vat, eth, dai):
    """ Opens a new vault with unjoined ETH collateral.
    """

    user_id = uuid4().hex
    gemjoin_join(vat, "eth", user_id, eth)
    vat_frob(vat, "eth", user_id, eth, dai)


def reduce_open_eth_vault(params, _substep, _state_hist, state):
    """ Executes all `open_eth_vault` policies for a timestep.
    """

    new_vat = deepcopy(state["vat"])
    dai_val = state["spotter"]["ilks"]["dai"]["val"]
    eth_val = state["spotter"]["ilks"]["eth"]["val"]

    if state["timestep"] < params["WARM_TAU"]:
        for _ in range(1000):
            # Open a vault w/ 1 ETH @ 175% collateralization
            # TODO: Associate this with an "Ideal" or "Basic" user behavior
            open_eth_vault(new_vat, 1, eth_val * 4 / 7)
        return {"vat": new_vat}
    if dai_val > 1:
        ddai_val = dai_val - 1
        prob = 5 * ddai_val + 0.05
        if random.random() <= prob:
            open_eth_vault(new_vat, 1, eth_val * 4 / 7)
            return {"vat": new_vat}

    return {}


# ---


# Join


def gemjoin_join(vat, ilk_id, user_id, wad):
    """ Records a collateral deposit in the Vat.
    """

    assert wad >= 0
    vat_slip(vat, ilk_id, user_id, wad)


def gemjoin_exit(vat, ilk_id, user_id, wad):
    """ Records a collateral withdrawal in the Vat.
    """

    vat_slip(vat, ilk_id, user_id, -wad)


def daijoin_join(vat, user_id, wad):
    """ Records an ERC-20 Dai deposit in the Vat.
    """

    vat_move(vat, "daijoin", user_id, wad)


def daijoin_exit(vat, user_id, wad):
    """ Records an ERC-20 Dai withdrawal in the Vat.
    """

    vat_move(vat, user_id, "daijoin", wad)


# ---


# Spotter


def spotter_peek(pip, timestep):
    """ Read in the price value at time `timestep` from feed `pip`.
    """

    with open(pip) as price_feed_json:
        return json.load(price_feed_json)[timestep]["price_close"]


def spotter_poke(spotter, vat, ilk_id, now):
    """ Gets the current `spot` value of the given Ilk.
    """

    ilk = spotter["ilks"][ilk_id]
    val = spotter_peek(ilk["pip"], now)
    ilk["val"] = val

    spot = val / spotter["par"] / ilk["mat"]

    vat_file(vat, ilk_id, "spot", spot)


# ---


# Vat


def vat_file(vat, ilk_id, what, data):
    """ Sets the `what` field for the given Ilk to `data`.
    """

    if what == "spot":
        vat["ilks"][ilk_id]["spot"] = data
    elif what == "line":
        vat["ilks"][ilk_id]["line"] = data
    elif what == "dust":
        vat["ilks"][ilk_id]["dust"] = data


def vat_slip(vat, ilk_id, user_id, wad):
    """ Adds to the collateral record of the user. Creates the record if necessary.
    """

    gem = vat["gem"][ilk_id].get(user_id, 0)
    gem += wad
    vat["gem"][ilk_id][user_id] = gem


def vat_flux(vat, ilk_id, src, dst, wad):
    """ Moves gem from one address to another. Assumes both addresses already exist.
    """

    vat["gem"][ilk_id][src] -= wad
    vat["gem"][ilk_id][dst] += wad


def vat_move(vat, src, dst, rad):
    """ Moves dai from one address to another. Assumes both addresses already exist.
    """

    vat["dai"][src] -= rad
    vat["dai"][dst] += rad


def vat_frob(vat, ilk_id, user_id, dink, dart):
    """ Sets an urn in the Vat and updates the collateral and Dai records approiately.

        Creates an urn and Dai record if they don't exist.
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
    dai = vat["dai"].get(user_id, 0)
    dai += dtab
    vat["dai"][user_id] = dai

    vat["urns"][ilk_id][user_id] = urn
    vat["ilks"][ilk_id] = ilk


def vat_grab(vat, ilk_id, user_id, dink, dart):
    """ Confiscates an urn.
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


def vow_fess(vow, tab):
    """ Pushes to the debt queue.
    """

    vow["Sin"] += tab


# ---


# Cat


def cat_bite(vat, vow, cat, flipper, ilk_id, user_id, now):
    """ Liquidates an undercollateralized vault and puts its collateral up for a Flipper auction.
    """

    ilk = vat["ilks"][ilk_id]

    rate = ilk["rate"]
    spot = ilk["spot"]

    ink = vat["urns"][ilk_id][user_id]["ink"]
    art = vat["urns"][ilk_id][user_id]["art"]

    assert spot > 0 and ink * spot < art * rate
    assert art > 0 and ink > 0

    vat_grab(vat, ilk_id, user_id, -ink, -art)
    vow_fess(vow, art * rate)

    milk = cat["ilks"][ilk_id]
    tab = art * rate * milk["chop"]
    cat["litter"] += tab

    flipper_kick(flipper, vat, user_id, "vow", tab, ink, 0, now + flipper["tau"])


def reduce_cat_bite(_params, _substep, _state_hist, state):
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
            cat_bite(
                new_vat,
                new_vow,
                new_cat,
                new_flipper,
                "eth",
                user_id,
                state["timestep"],
            )

    return {"cat": new_cat, "flipper": new_flipper, "vat": new_vat, "vow": new_vow}


def cat_claw(cat, rad):
    """ Subtracts from the measure of Dai up for liquidation.
    """

    cat["litter"] -= rad


# ---


# Flipper


def flipper_kick(flipper, vat, user_id, gal, tab, lot, bid, end):
    """ Kicks off a new Flip auction.
    """

    flipper["bids"][uuid4().hex] = {
        "bid": bid,
        "lot": lot,
        "guy": "cat",
        "tic": 0,
        "end": end,
        "usr": user_id,
        "gal": gal,
        "tab": tab,
    }

    vat_flux(vat, flipper["ilk"], "cat", "flipper", lot)


def flipper_tend(flipper, vat, bid_id, user_id, lot, bid, now):
    """ Places a tend bid on a Flipper auction.
    """

    curr_bid = flipper["bids"][bid_id]

    assert curr_bid["tic"] > now or curr_bid["tic"] == 0
    assert curr_bid["end"] > now

    assert lot == curr_bid["lot"]
    assert bid <= curr_bid["tab"]
    assert bid > curr_bid["bid"]
    assert bid >= curr_bid["bid"] * flipper["beg"] or bid == curr_bid["tab"]

    if user_id != curr_bid["guy"]:
        vat_move(vat, user_id, curr_bid["guy"], curr_bid["bid"])
        curr_bid["guy"] = user_id
    vat_move(vat, user_id, curr_bid["gal"], bid - curr_bid["bid"])

    curr_bid["bid"] = bid
    curr_bid["tic"] = now + flipper["ttl"]


def flipper_dent(flipper, vat, bid_id, user_id, lot, bid, now):
    """ Places a dent bid on a Flipper auction.
    """

    curr_bid = flipper["bids"][bid_id]

    assert curr_bid["tic"] > now or curr_bid["tic"] == 0
    assert curr_bid["end"] > now

    assert bid == curr_bid["bid"]
    assert bid == curr_bid["tab"]
    assert lot < curr_bid["lot"]
    assert lot * flipper["beg"] <= curr_bid["lot"]

    if user_id != curr_bid["guy"]:
        vat_move(vat, user_id, curr_bid["guy"], curr_bid["bid"])
        curr_bid["guy"] = user_id
    vat_flux(vat, flipper["ilk"], "flipper", curr_bid["usr"], curr_bid["lot"] - lot)

    curr_bid["lot"] = lot
    curr_bid["tic"] = now + flipper["ttl"]


def flipper_deal(flipper, vat, cat, bid_id, now):
    """ Deals out a Flipper auction.
    """

    curr_bid = flipper["bids"][bid_id]

    assert curr_bid["tic"] != 0 and (curr_bid["tic"] < now or curr_bid["end"] < now)

    cat_claw(cat, curr_bid["tab"])
    vat_flux(vat, flipper["ilk"], "flipper", curr_bid["guy"], curr_bid["lot"])
    del flipper["bids"][bid_id]


# ---


# Utility


def policy_reduce(policy_signal_dict_a, policy_signal_dict_b):
    """ Reduces policy signals by merging them into one dict.

        If there is an overlap in keys, the value of `policy_signal_dict_b` is taken.
    """

    return {**policy_signal_dict_a, **policy_signal_dict_b}
