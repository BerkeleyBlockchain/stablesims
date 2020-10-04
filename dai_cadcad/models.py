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
    """ Simple Bidding Model
    """

    spotter = state["spotter"]
    discount = extra.get("discount")

    if status["guy"] == user_id or not status["price"] or not discount:
        return None

    oracle = spotter["ilks"]["eth"]["val"]

    return {
        "price": oracle * Wad.from_number(1 - discount),
        "gas_price": Wad.from_number(15000000000),
    }


def flipper_eth_model_inchworm(status, user_id, _state, _extra):
    """ Makes the smallest valid bid.
    """

    if status["guy"] == user_id or not status["price"]:
        return None

    return {
        "price": status["price"] * status["beg"],
        "gas_price": Wad.from_number(15000000000),
    }


choose = {"flipper_eth": {"basic": flipper_eth_model_basic}}
