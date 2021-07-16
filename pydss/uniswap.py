""" Uniswap Module
    Class-based representation of Uniswap,
    used to model the whole external market.
"""

import json
from pydss.pymaker.numeric import Wad, Rad


class Uniswap:
    """
    liquidity_feed_paths = dict[str: str]
    pairs = dict[str: dict: [str: float]]
    """

    def __init__(self, pairs):
        self.liquidity_feed_paths = {}
        self.pairs = {}
        for pair_id in pairs:
            pair = pairs[pair_id]
            self.liquidity_feed_paths[pair_id] = pair["path"]
            self.pairs[pair_id] = {pair["token0"]: 0, pair["token1"]: 0}

    def tick(self, t):
        for pair_id in self.pairs:
            with open(self.liquidity_feed_paths[pair_id]) as liquidity_feed_file:
                liquidity_feed = json.load(liquidity_feed_file)
                self.pairs[pair_id] = liquidity_feed[t]

    def get_slippage(self, pair_id, in_token, in_amt, t):
        self.tick(t)
        out_token = next(filter(lambda x: x != in_token, self.pairs[pair_id].keys()))
        in_reserve = Wad.from_number(float(self.pairs[pair_id][in_token]))
        out_reserve = Wad.from_number(float(self.pairs[pair_id][out_token]))
        initial_rate = in_reserve / out_reserve
        k = in_reserve * out_reserve
        new_in_reserve = in_reserve - in_amt
        new_out_reserve = k / new_in_reserve
        new_rate = new_in_reserve / new_out_reserve
        return (
            Rad(out_reserve - new_out_reserve),
            (new_rate - initial_rate) / initial_rate,
        )
