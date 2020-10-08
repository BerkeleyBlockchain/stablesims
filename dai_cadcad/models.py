""" Models Module

Contains the definition of the keeper bidding models.
Models are separated by level of complexity.

Access the models using the dictionary and the corresponding keys.
"""
from dai_cadcad.pymaker.numeric import Wad


# status as defined by the docs:
# {
#     "id": "",
#     "flipper": "",
#     "flapper": "",
#     "flopper": "",
#     "bid": Rad(0),
#     "lot": Wad(0),
#     "tab": Rad(0),
#     "beg": Wad(0),
#     "guy": "",
#     "era": 0,
#     "tic": 0,
#     "end": 0,
#     "price": 0
# }


def flipper_eth_model_basic(status, user_id, state, extra):
    """ Makes the smallest valid bid.
    """

    spotter = state["spotter"]
    discount = extra["discount"]
    gas_price = extra["gas_price"]

    if status["guy"] == user_id or not status["price"]:
        return None

    if status["price"] == Wad(0):
        oracle = spotter["ilks"]["eth"]["val"]
        price = oracle * Wad.from_number(1 - discount)
    else:
        price = status["price"] * status["beg"]

    return {
        "price": price,
        "gas_price": gas_price,
    }


def flipper_eth_model_clever_boi(status, user_id, state, extra):
    """ Makes the smallest valid bid.
    """

    spotter = state["spotter"]
    discount = extra["discount"]

    if status["guy"] == user_id or not status["price"]:
        return None

    if status["price"] == Wad(0):
        oracle = spotter["ilks"]["eth"]["val"]
        price = oracle * Wad.from_number(1 - discount)
    else:
        price = status["price"] * status["beg"]

    return {
        "price": price,
    }


choose = {
    "flipper_eth": {
        "basic": flipper_eth_model_basic,
        "clever_boi": flipper_eth_model_clever_boi,
    }
}
