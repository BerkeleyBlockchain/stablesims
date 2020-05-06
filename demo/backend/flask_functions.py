import sys
sys.path.append("/Users/andrew/projects/bab-stablecoin_sims_research/demo/backend/simulator/PYLOB")

from random import randint
from simulator import *

def track(trackers, market):
    trackers['usd_eth'].append(market.usd_eth)
    trackers['bond_q_len'].append(market.protocol.bondQueueLength)
    trackers['demand_ratio'].append(market.demandRatio)
    trackers['ask_volume'].append(market.askVolume)
    trackers['bid_volume'].append(market.bidVolume)
    trackers['total_volume'].append(market.totalVolume)
    trackers['circulation'].append(market.getCirculation())

def warmup(market):
    global cur_time
    NUM_TRADERS = market.params["trader_demographics"]['IdealTrader'] # We initially set it up with randomTraders

    for _ in range(market.params["NUM_ORDERS_INIT"]):
        market.usd_eth = 1.0 / get_eth_price(cur_time, market)
        
        tid = randint(1, NUM_TRADERS)
        orders = market.traderPool[tid].marketStep()
        for order in orders:
            market.processOrder(order)
        cur_time += 1
        
    # Keep demandRatio constant at 0.5 when we start the market
    market.demandRatio = 0.5
    

def trade(market, trackers):
    global cur_time
    NUM_TRADERS = market.params["trader_demographics"]['AverageTrader'] + market.params["trader_demographics"]['BasicTrader']
    OFFSET_TRADERS = market.params["trader_demographics"]['IdealTrader']
    
    for i in range(market.params["NUM_ORDERS_LIVE"]):
        market.usd_eth = 1 / get_eth_price(cur_time, market) 
        if i % market.params["TRACK_FREQ"] == 0:
            track(trackers, market)
            
        tid = randint(OFFSET_TRADERS + 1, OFFSET_TRADERS + NUM_TRADERS)
        orders = market.traderPool[tid].marketStep()
        for order in orders:
            market.processOrder(order)    
        cur_time += 1


def run(params, query):
    params = Params(params)
    market = Market(params)
    basis = BasisProtocol(int(1e7), market)
    market.protocol = basis
    traderPool = createTraderPool(basis, market, market.params["trader_demographics"])
    market.setTraderPool(traderPool)

    cur_time = 0
    market.usd_eth = 1 / get_eth_price(0, market)

    trackers = {'usd_eth': [], 'bond_q_len': [], 'demand_ratio': [], 'ask_volume': [],
                'bid_volume': [], 'total_volume': [], 'circulation': []}

    warmup(market)

    trade(market, trackers)
