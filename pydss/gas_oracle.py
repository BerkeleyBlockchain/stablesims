""" Gas Oracle Module
    Class-based representation of a Gas Oracle,
    used to model gas.
"""

import json

from pydss.pymaker.numeric import Wad


class GasOracle:
    """
    liquidity_feed_paths = dict[str: str]
    pairs = dict[str: dict: [str: float]]
    """

    def __init__(self, price_feed_file):
        self.price_feed_file = price_feed_file

    # TODO: rename with correct function name from dss
    def peek(self, now):
        with open(self.price_feed_file) as price_feed_json:
            # TODO: Constantize the "avgGasDay" field here
            # TODO: Format gas feed file to get rid of "data"
            return Wad.from_number(json.load(price_feed_json)["data"][now]["avgGasDay"])
