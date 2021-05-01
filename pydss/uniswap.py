""" Uniswap Module
    Class-based representation of Uniswap,
    used to model the whole external market
    as an automated market maker.
"""

import requests

# from pydss.util import require


class Uniswap:
    """
    liq_feed = str
    pairs = dict[str: dict: [str: float]]
    """

    def __init__(self, liq_feed):
        self.liq_feed = liq_feed
        self.pairs = {}

    def get_liquidity(self, _pair_id, _timestamp):
        block_number_query = self.liq_feed
        res = requests.post(
            "https://api.thegraph.com/subgraphs/name/blocklytics/ethereum-blocks",
            json={"query": block_number_query},
        )
        print(res.text)
