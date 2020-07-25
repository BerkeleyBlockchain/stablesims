""" Prices Module

Contains functions for generating price feeds using numpy and the CoinGecko API.

Current approach is to sample from historical data, rather than fully simulating price feeds, or
just using historical data out-the-box.
"""

import numpy as np
from numpy.random import default_rng
from pycoingecko import CoinGeckoAPI

rng = default_rng()
cg = CoinGeckoAPI()


def generate_price_feed(coin_id, time_range, batch_size):
    """ Generates a price feed (in USD) for the given coin (ETH, DAI, MKR).

      Does this by:
      1. Obtaining the price distribution for `coin_id` (from the CoinGecko API) over `time_range`
      2. Batching it into `batch_factor` evenly-sized regions
      3. Fitting a normal curve to the same mean & SD as each region
      4. Sampling from each normal to create a time series (same # of datapoints)
    """

    res = cg.get_coin_market_chart_range_by_id(
        coin_id, "usd", time_range[0], time_range[1]
    )
    prices = [res["prices"][i][1] for i in range(len(res["prices"]))]

    generated_prices = []

    num_batches = len(prices) // batch_size

    for i in range(num_batches):
        sample = prices[i * batch_size : (i + 1) * batch_size]
        sample_mu = np.mean(sample)
        sample_sd = np.std(sample)
        generated_prices.extend(list(rng.normal(sample_mu, sample_sd, batch_size)))

    tail_size = len(prices) - (num_batches * batch_size)
    tail_sample = prices[-tail_size:]
    tail_mu = np.mean(tail_sample)
    tail_sd = np.std(tail_sample)
    generated_prices.extend(list(rng.normal(tail_mu, tail_sd, tail_size)))

    return (prices, generated_prices)
