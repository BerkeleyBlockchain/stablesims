"""
Fetch Uniswap ETH/DAI liquidity data for a given timeframe
"""

import requests
import os
import json

def fetch_block_numbers_for_timestamps(from_timestamp, to_timestamp):
    query = f"""
    {{
        blocks(
            orderBy: timestamp,
            orderDirection: asc,
            where: {{timestamp_gte: {from_timestamp}, timestamp_lt: {to_timestamp}}})
        {{
            number
        }}
    }}"""

    blocks = requests.post(
        "https://api.thegraph.com/subgraphs/name/blocklytics/ethereum-blocks",
        json={"query": query}
    ).json()["data"]["blocks"]

    return [int(block["number"]) for block in blocks]

def fetch_liquidity_for_block_numbers(block_numbers):
    pairs = []
    for block_number in block_numbers:
        query = f"""
        {{
            pairs(
                block: {{number: {block_number}}},
                where: {{id: "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"}})
            {{
                token0 {{
                    symbol
                }}
                token1 {{
                    symbol
                }}
                reserve0
                reserve1
            }}
        }}"""

        pairs.append(requests.post(
            "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
            json={"query": query}
        ).json()["data"]["pairs"][0])

    return [{
        pair["token0"]["symbol"]: float(pair["reserve0"]),
        pair["token1"]["symbol"]: float(pair["reserve1"])
    } for pair in pairs]


if __name__ == "__main__":
    filename = os.getenv("filename")
    from_timestamp = os.getenv("from")
    to_timestamp = os.getenv("to")

    if not (filename or from_timestamp or to_timestamp):
        print("Please enter filename or from/to timestamps")
        sys.exit()

    block_numbers = fetch_block_numbers_for_timestamps(from_timestamp, to_timestamp)
    liquidity_feed = fetch_liquidity_for_block_numbers(block_numbers)

    liquidity_feed_fd = os.open(f"feeds/eth_dai_liquidity/{filename}.json", os.O_WRONLY | os.O_CREAT)
    os.write(liquidity_feed_fd, str.encode(json.dumps(liquidity_feed)))
    os.close(liquidity_feed_fd)
