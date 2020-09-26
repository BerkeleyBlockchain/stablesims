""" Models Module

Contains the definition of the keeper bidding models.
Models are separated by level of complexity.

Access the models using the dictionary and the corresponding keys.
"""

# std_input as defined by the docs:
# {
#     "id": "",
#     "flapper": "",
#     "bid": "",
#     "lot": "",
#     "beg": "",
#     "guy": "",
#     "era": 0,
#     "tic": 0,
#     "end": 0,
#     "price": ""
# }

# should discount be passed in or something else
# oracle = get_price()  # get asset price from api


def simple_model(_std_input, _discount=0.15):
    """ Simple Bidding Model
    """
    stance = {"price": 0}  # default price set to 0
    return stance


def medium_model(std_input, discount=0.15):
    """ Simple Bidding Model
    """
    stance = {"price": 0}  # default price set to 0
    oracle = 100  # price of collat
    for line in std_input:  # iterate through standard input
        if line == "price":
            stance["price"] = oracle * (1 - discount)
    return stance  # according to docs, return dictionary"


def complex_model(_std_input, _discount=0.15):
    """ Simple Bidding Model
    """
    stance = {"price": 0}  # default price set to 0
    return stance


choose = {"simple": simple_model, "medium": medium_model, "complex": complex_model}
