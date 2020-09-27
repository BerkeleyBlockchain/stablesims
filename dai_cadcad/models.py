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


def flipper_eth_model_basic(status, user_id, spotter, discount=0.15):
    """ Simple Bidding Model
    """
    if status["guy"] == user_id:
        return None

    oracle = spotter["ilks"]["eth"]["val"]

    return {"price": oracle * Wad.from_number(1 - discount)}


choose = {"flipper_eth": {"basic": flipper_eth_model_basic}}
