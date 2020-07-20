from uuid import uuid4
from constants import *
from copy import deepcopy


# Vat

# TODO
# Be sure to remember the ETH_LINE assertion, and to add `eth` to `state.eth_ilk`'s `debt_dai`.
def join_all(_params, substep, sH, s, **kwargs):
    '''Generates and executes all `join` operations.'''
    new_vat = deepcopy(s["vat"])
    join(150, 100, new_vat)
    return {"vat": new_vat}


def join(eth, dai, new_vat):

    # Create the new vault to be joined
    vault_id = uuid4().hex
    new_vault = {
        "vault_id": vault_id,
        "eth": eth,
        "dai": dai,
        "bitten": False
    }

    new_vat[vault_id] = new_vault

# ---


# Cat

def bite_all(_params, substep, sH, s, **kwargs):
    '''Searches through all vaults in the vat, and returns a list
       of `bite` policy functions for each undercollateralized one.'''

    new_vat = deepcopy(s["vat"])
    new_flipper = deepcopy(s["flipper"])
    spot_rate = s["eth_ilk"]["spot_rate"]
    stability_rate = s["eth_ilk"]["stability_rate"]

    for vault_id in new_vat:

        vault = new_vat[vault_id]
        eth = vault["eth"]
        dai = vault["dai"]
        debt_to_flip = dai * stability_rate
        max_allowable_debt = spot_rate * eth

        if (not vault["bitten"] and debt_to_flip > max_allowable_debt):
            bite(vault_id, debt_to_flip, eth, new_vat, new_flipper)

    return {"flipper": new_flipper, "vat": new_vat}

# TODO: Should we still do assertions within the function itself?
def bite(vault_id, debt_to_flip, eth, new_vat, new_flipper):
    '''Modifies the passed-in vat and flipper state variables to reflect
       the given vault being bitten.'''

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
        "expiry": FLIP_TAU
    }

    new_flipper[flip_id] = new_flip
    new_vat[vault_id]["bitten"] = True

# ---


# Flipper

def make_flip_tend(flip_id, bid, keeper_id):

    def flip_tend(_params, substep, sH, s, **kwargs):

        # TODO: Check that `flip` exists?

        flip = s["flipper"][flip_id]

        # TODO: Check that `flip` has not expired?

        phase = flip["phase"]
        assert (phase == "tend")
        bid_dai = flip["bid_dai"]
        assert (bid > bid_dai * FLIP_BEG)
        # Not sure why we don't want to raise more, but this is from the smart contract
        # https://github.com/makerdao/dss/blob/master/src/flip.sol
        debt_to_flip = flip["debt_to_flip"]
        assert (bid <= debt_to_flip)

        new_flipper = deepcopy(s["flipper"])
        new_flip = new_flipper[flip_id]
        new_flip["bid_dai"] = bid
        new_flip["bidder"] = keeper_id
        if (bid == debt_to_flip):
            new_flip["phase"] = "dent"
        # TODO: Should timekeeping be handled here?
        new_flip["expiry"] -= 1

        return {"flipper": new_flipper}

    return flip_tend


def make_flip_dent(flip_id, lot, keeper_id):

    def flip_dent(_params, substep, sH, s, **kwargs):

        flip = s["flipper"][flip_id]

        phase = flip["phase"]
        assert (phase == "dent")

        lot_eth = flip["lot_eth"]
        assert (lot < lot_eth * FLIP_BEG)

        new_flipper = deepcopy(s["flipper"])
        new_flip = new_flipper[flip_id]
        new_flip["lot_eth"] = lot
        new_flip["bidder"] = keeper_id
        new_flip["expiry"] -= 1

        return {"flipper": new_flipper}

    return flip_dent


def make_flip_deal(flip_id):

    def flip_deal(_params, substep, sH, s, **kwargs):

        flip = s["flipper"][flip_id]

        expiry = flip["expiry"]
        assert (expiry == 0)

        # Move DAI bid from Keeper to Vow surplus
        new_keepers = deepcopy(s["keepers"])
        new_keeper = new_keepers[flip["bidder"]]
        bid_dai = flip["bid_dai"]
        new_keeper["dai"] -= bid_dai
        new_vow = deepcopy(s["vow"])
        new_vow["surplus_dai"] += bid_dai

        # If not enough Dai raised, put remainder of debt in Vow

        # Move ETH lot from Vault to Keeper
        new_vat = deepcopy(s["vat"])
        new_vault = new_vat[flip["vault"]]
        lot_eth = flip["lot_eth"]
        new_vault["eth"] -= lot_eth
        # TODO: Should vault cleanup logic be handled here?
        new_keeper["eth"] += lot_eth

        # Delete Flipper auction
        new_flipper = deepcopy(s["flipper"])
        del new_flipper[flip_id]

        return {"vow": new_vow, "keepers": new_keepers, "vat": new_vat, "flipper": new_flipper}

    return flip_deal

# ---


# Flapper

def make_flap_tend(flap_id, bid, keeper_id):

    def flap_tend(_params, substep, sH, s, **kwargs):

        flap = s["flapper"][flap_id]

        bid_mkr = flap["bid_mkr"]
        assert (bid > bid_mkr * FLAP_BEG)

        new_flapper = deepcopy(s["flapper"])
        new_flap = new_flapper[flap_id]
        new_flap["bid_mkr"] = bid
        new_flap["bidder"] = keeper_id
        new_flap["expiry"] -= 1

        return {"flapper": new_flapper}

    return flap_tend


def make_flap_deal(flap_id):

    def flap_deal(_params, substep, sH, s, **kwargs):

        flap = s["flapper"][flap_id]

        expiry = flap["expiry"]
        assert (expiry == 0)

        # Burn Keeper's MKR bid
        bid_mkr = flap["bid_mkr"]
        new_keepers = deepcopy(s["keepers"])
        new_keeper = new_keepers[flap["bidder"]]
        new_keeper["mkr"] -= bid_mkr

        # Move DAI lot from Vow surplus to Keeper
        new_vow = deepcopy(s["vow"])
        lot_dai = flap["lot_dai"]
        new_vow["surplus_dai"] -= lot_dai
        new_keeper["dai"] += lot_dai

        # Delete Flapper auction
        new_flapper = deepcopy(s["flapper"])
        del new_flapper[flap_id]

        return {"keepers": new_keepers, "vow": new_vow, "flapper": new_flapper}

    return flap_deal

# ---


# Flopper

def make_flop_dent(flop_id, lot, keeper_id):

    def flop_dent(_params, substep, sH, s, **kwargs):

        flop = s["flopper"][flop_id]

        lot_mkr = flop["lot_mkr"]
        assert (lot < lot_mkr * FLOP_BEG)

        new_flopper = deepcopy(s["flopper"])
        new_flop = new_flopper[flop_id]
        new_flop["lot_mkr"] = lot
        new_flop["bidder"] = keeper_id
        new_flop["expiry"] -= 1

        return {"flopper": new_flopper}

    return flop_dent


def make_flop_deal(flop_id):

    def flop_deal(_params, substep, sH, s, **kwargs):

        flop = s["flopper"][flop_id]

        expiry = flop["expiry"]
        assert (expiry == 0)

        # Move DAI bid from Keeper to Vow surplus
        new_keepers = deepcopy(s["keepers"])
        new_keeper = new_keepers[flop["bidder"]]
        bid_dai = flop["bid_dai"]
        new_keeper["dai"] -= bid_dai
        new_vow = deepcopy(s["vow"])
        new_vow["surplus_dai"] += bid_dai

        # Mint MKR lot
        lot_mkr = flop["lot_mkr"]
        new_keeper["mkr"] += lot_mkr

        # Delete Flopper auction
        new_flopper = deepcopy(s["flopper"])
        del new_flopper[flop_id]

        return {"vow": new_vow, "keepers": new_keepers, "flopper": new_flopper}

    return flap_deal


# ---


# Utility

def policy_reduce(policy_value_a, policy_value_b):
    return {**policy_value_a, **policy_value_b}
