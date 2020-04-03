import numpy as np
import json

from .constants import *

def biased_coin(prob):
    return int(np.random.random() < prob)

def clamp_bas_price(price):
    # 1 BAS = price ETH
    return np.clip(price, 0, 10.0)

def clamp_bas_qty(qty): 
    # Max order size of $100,000
    return np.clip(qty, 0, 1e5)

def months_to_seconds(mths):
    return mths * 30 * 24 * 60 * 60


eth_prices = json.load(open('etherium.json'))

def get_eth_price(t):
    idx = ETH_DAY_OFFSET + (t // TRADES_PER_DAY)
    lin = (t % TRADES_PER_DAY) / (1. * TRADES_PER_DAY)
    if idx >= len(eth_prices) - 1:
        return eth_prices[-1]
    return eth_prices[idx] * (1.0 - lin) + eth_prices[idx + 1] * lin