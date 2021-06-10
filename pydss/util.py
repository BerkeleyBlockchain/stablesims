""" Utility Module
    Contains utility functions such as those for raising exceptions.
"""
import json
import random


class RequireException(Exception):
    pass


def require(cond, message):
    """ Simple method to raise an exception with the given `message`
        if `cond` evaluates to False.
    """

    if not cond:
        raise RequireException(message)


def random_sample_gas():
    with open("../price_feeds/gas/eth_gas.json") as f:
        data = json.load(f)
    i = random.randint(0, len(data["data"]))
    return data["data"][i]["avgGasDay"]
