""" Utility Module
    Contains utility functions such as those for raising exceptions.
"""

import math
import json
import requests


class RequireException(Exception):
    pass


def require(cond, message):
    """ Simple method to raise an exception with the given `message`
        if `cond` evaluates to False.
    """

    if not cond:
        raise RequireException(message)


def get_timestamps(init_timestamp, duration, granularity):
    """ Returns a list of UNIX timestamps over the given duration,
        with the given granularity, assuming the given initial
        timestamp. All values in seconds.
    """
    num_steps = math.ceil(duration / granularity)
    return [init_timestamp + i * granularity for i in range(num_steps)]


def get_block_numbers(timestamps):
    """ Returns a list of block numbers for each timestamp
        in the given list.
    """
    block_numbers = []
    for timestamp in timestamps:
        block_number_query = (
            "query {"
            "blocks(first: 1, orderBy: timestamp, orderDirection: asc,"
            f'where: {{timestamp_gte: "{timestamp}"}}) {{'
            "number"
            "}"
            "}"
        )
        res = requests.post(
            "https://api.thegraph.com/subgraphs/name/blocklytics/ethereum-blocks",
            json={"query": block_number_query},
        )
        json_res = json.loads(res.text)
        block_numbers.append(int(json_res["data"]["blocks"][0]["number"]))
    return block_numbers


def scrape_liquidity(pair_id, init_timestamp, duration, granularity, dst_path):
    liquidity_feed = []
    block_numbers = get_block_numbers(
        get_timestamps(init_timestamp, duration, granularity)
    )
    for block_number in block_numbers:
        liquidity_query = (
            "query {"
            f'pair(id: "{pair_id}", block: {{number: {block_number}}}) {{'
            "token0 {"
            "symbol"
            "},"
            "token1 {"
            "symbol"
            "},"
            "reserve0,"
            "reserve1,"
            "}"
            "}"
        )
        res = requests.post(
            "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
            json={"query": liquidity_query},
        )
        json_res = json.loads(res.text)
        token0 = json_res["data"]["pair"]["token0"]["symbol"]
        token1 = json_res["data"]["pair"]["token1"]["symbol"]
        reserve0 = json_res["data"]["pair"]["reserve0"]
        reserve1 = json_res["data"]["pair"]["reserve1"]
        liquidity_feed.append({token0: reserve0, token1: reserve1})

    with open(dst_path, "w") as liquidity_feed_file:
        json.dump(liquidity_feed, liquidity_feed_file)
