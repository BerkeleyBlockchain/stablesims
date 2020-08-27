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


def join_all(params, _substep, _state_hist, state):
    """ Generates and executes all `join` operations.

        Currently, this only occurs in a 1-step warmup period.
    """

    if state["timestep"] < params["WARM_TAU"]:
        new_vat = deepcopy(state["vat"])
        new_eth_ilk = deepcopy(state["eth_ilk"])
        for _ in range(1000):
            join(150, 100, new_vat, new_eth_ilk)
        return {"vat": new_vat}
    return {}


# TODO: Be sure to remember the ETH_LINE assertion
def join(eth, dai, new_vat, new_eth_ilk):
    """ Executes a single `join` operation.

        Creates a new vault in the `vat` containing `eth` and `dai`.
    """

    # Create the new vault to be joined
    vault_id = uuid4().hex
    new_vault = {"vault_id": vault_id, "eth": eth, "dai": dai, "bitten": False}

    new_vat[vault_id] = new_vault

    new_eth_ilk["debt_dai"] += dai


# ---


# Cat


def bite_all(params, _substep, _state_hist, state):
    """ Generates and executes all `bite` operations.

        Searches through all vaults in the vat, and returns a list
        of `bite` policy functions for each undercollateralized one.
    """

    new_vat = deepcopy(state["vat"])
    new_flipper = deepcopy(state["flipper"])
    spot_rate = state["eth_ilk"]["spot_rate"]
    stability_rate = state["eth_ilk"]["stability_rate"]

    for vault_id in new_vat:

        vault = new_vat[vault_id]
        eth = vault["eth"]
        dai = vault["dai"]
        debt_to_flip = dai * stability_rate
        max_allowable_debt = spot_rate * eth

        if not vault["bitten"] and debt_to_flip > max_allowable_debt:
            flip_tau = params["FLIP_TAU"]
            bite(vault_id, debt_to_flip, eth, flip_tau, new_vat, new_flipper)

    return {"flipper": new_flipper, "vat": new_vat}


# TODO: Should we still do assertions within the function itself?
def bite(vault_id, debt_to_flip, eth, flip_tau, new_vat, new_flipper):
    """ Executes a single `bite` operation.

        Marks the given vault as bitten, and creates a new flip (effectively kicking it).
    """

    # Create the Flipper auction to be kicked (adding it to the flipper is the same as kicking it)
    flip_id = uuid4().hex
    new_flip = {
        "flip_id": flip_id,
        "phase": "tend",
        "debt_to_flip": debt_to_flip,
        "vault": vault_id,
        "lot_eth": eth,
        "bid_dai": 0,
        "bidder": "",
        "expiry": flip_tau,
    }

    new_flipper[flip_id] = new_flip
    new_vat[vault_id]["bitten"] = True


# ---


# Flipper


def make_flip_tend(flip_id, bid, keeper_id):
    """ Needs to be refactored to `_all()` convention.
    """

    def flip_tend(params, _substep, _state_hist, state):

        # TODO: Check that `flip` exists?

        flip = state["flipper"][flip_id]

        # TODO: Check that `flip` has not expired?

        phase = flip["phase"]
        assert phase == "tend"
        bid_dai = flip["bid_dai"]
        assert bid > bid_dai * params["FLIP_BEG"]
        # Not sure why we don't want to raise more, but this is from the smart contract
        # https://github.com/makerdao/dss/blob/master/src/flip.sol
        debt_to_flip = flip["debt_to_flip"]
        assert bid <= debt_to_flip

        new_flipper = deepcopy(state["flipper"])
        new_flip = new_flipper[flip_id]
        new_flip["bid_dai"] = bid
        new_flip["bidder"] = keeper_id
        if bid == debt_to_flip:
            new_flip["phase"] = "dent"
        # TODO: Should timekeeping be handled here?
        new_flip["expiry"] -= 1

        return {"flipper": new_flipper}

    return flip_tend


def make_flip_dent(flip_id, lot, keeper_id):
    """ Needs to be refactored to `_all()` convention.
    """

    def flip_dent(params, _substep, _state_hist, state):

        flip = state["flipper"][flip_id]

        phase = flip["phase"]
        assert phase == "dent"

        lot_eth = flip["lot_eth"]
        assert lot < lot_eth * params["FLIP_BEG"]

        new_flipper = deepcopy(state["flipper"])
        new_flip = new_flipper[flip_id]
        new_flip["lot_eth"] = lot
        new_flip["bidder"] = keeper_id
        new_flip["expiry"] -= 1

        return {"flipper": new_flipper}

    return flip_dent


def make_flip_deal(flip_id):
    """ Needs to be refactored to `_all()` convention.
    """

    def flip_deal(_params, _substep, _state_hist, state):

        flip = state["flipper"][flip_id]

        expiry = flip["expiry"]
        assert expiry == 0

        # Move DAI bid from Keeper to Vow surplus
        new_keepers = deepcopy(state["keepers"])
        new_keeper = new_keepers[flip["bidder"]]
        bid_dai = flip["bid_dai"]
        new_keeper["dai"] -= bid_dai
        new_vow = deepcopy(state["vow"])
        new_vow["surplus_dai"] += bid_dai

        # If not enough Dai raised, put remainder of debt in Vow

        # Move ETH lot from Vault to Keeper
        new_vat = deepcopy(state["vat"])
        new_vault = new_vat[flip["vault"]]
        lot_eth = flip["lot_eth"]
        new_vault["eth"] -= lot_eth
        # TODO: Should vault cleanup logic be handled here?
        new_keeper["eth"] += lot_eth

        # Delete Flipper auction
        new_flipper = deepcopy(state["flipper"])
        del new_flipper[flip_id]

        return {
            "vow": new_vow,
            "keepers": new_keepers,
            "vat": new_vat,
            "flipper": new_flipper,
        }

    return flip_deal


# ---


# Flapper


def make_flap_tend(flap_id, bid, keeper_id):
    """ Needs to be refactored to `_all()` convention.
    """

    def flap_tend(params, _substep, _state_hist, state):

        flap = state["flapper"][flap_id]

        bid_mkr = flap["bid_mkr"]
        assert bid > bid_mkr * params["FLAP_BEG"]

        new_flapper = deepcopy(state["flapper"])
        new_flap = new_flapper[flap_id]
        new_flap["bid_mkr"] = bid
        new_flap["bidder"] = keeper_id
        new_flap["expiry"] -= 1

        return {"flapper": new_flapper}

    return flap_tend


def make_flap_deal(flap_id):
    """ Needs to be refactored to `_all()` convention.
    """

    def flap_deal(_params, _substep, _state_hist, state):

        flap = state["flapper"][flap_id]

        expiry = flap["expiry"]
        assert expiry == 0

        # Burn Keeper's MKR bid
        bid_mkr = flap["bid_mkr"]
        new_keepers = deepcopy(state["keepers"])
        new_keeper = new_keepers[flap["bidder"]]
        new_keeper["mkr"] -= bid_mkr

        # Move DAI lot from Vow surplus to Keeper
        new_vow = deepcopy(state["vow"])
        lot_dai = flap["lot_dai"]
        new_vow["surplus_dai"] -= lot_dai
        new_keeper["dai"] += lot_dai

        # Delete Flapper auction
        new_flapper = deepcopy(state["flapper"])
        del new_flapper[flap_id]

        return {"keepers": new_keepers, "vow": new_vow, "flapper": new_flapper}

    return flap_deal


# ---


# Flopper


def make_flop_dent(flop_id, lot, keeper_id):
    """ Needs to be refactored to `_all()` convention.
    """

    def flop_dent(params, _substep, _state_hist, state):

        flop = state["flopper"][flop_id]

        lot_mkr = flop["lot_mkr"]
        assert lot < lot_mkr * params["FLOP_BEG"]

        new_flopper = deepcopy(state["flopper"])
        new_flop = new_flopper[flop_id]
        new_flop["lot_mkr"] = lot
        new_flop["bidder"] = keeper_id
        new_flop["expiry"] -= 1

        return {"flopper": new_flopper}

    return flop_dent


def make_flop_deal(flop_id):
    """ Needs to be refactored to `_all()` convention.
    """

    def flop_deal(_params, _substep, _state_hist, state):

        flop = state["flopper"][flop_id]

        expiry = flop["expiry"]
        assert expiry == 0

        # Move DAI bid from Keeper to Vow surplus
        new_keepers = deepcopy(state["keepers"])
        new_keeper = new_keepers[flop["bidder"]]
        bid_dai = flop["bid_dai"]
        new_keeper["dai"] -= bid_dai
        new_vow = deepcopy(state["vow"])
        new_vow["surplus_dai"] += bid_dai

        # Mint MKR lot
        lot_mkr = flop["lot_mkr"]
        new_keeper["mkr"] += lot_mkr

        # Delete Flopper auction
        new_flopper = deepcopy(state["flopper"])
        del new_flopper[flop_id]

        return {"vow": new_vow, "keepers": new_keepers, "flopper": new_flopper}

    return flop_deal


# ---


# Utility


def policy_reduce(policy_signal_dict_a, policy_signal_dict_b):
    """ Reduces policy signals by merging them into one dict.

        If there is an overlap in keys, the value of `policy_signal_dict_b` is taken.
    """

    return {**policy_signal_dict_a, **policy_signal_dict_b}
