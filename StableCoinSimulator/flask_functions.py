import sys
sys.path.append("/Users/andrew/projects/bab-stablecoin_sims_research/StableCoinSimulator/simulator/PYLOB")

from random import randint
from simulator import *
from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

market = Market()
basis = BasisProtocol(int(1e7), market)
market.protocol = basis
traderPool = createTraderPool(basis, market, trader_demographics)
market.setTraderPool(traderPool)

cur_time = 0
market.usd_eth = 1 / get_eth_price(0)

trackers = {'usd_eth': [], 'bond_q_len': [], 'demand_ratio': [], 'ask_volume': [],
            'bid_volume': [], 'total_volume': [], 'circulation': []}

def track():
    trackers['usd_eth'].append(market.usd_eth)
    trackers['bond_q_len'].append(basis.bondQueueLength)
    trackers['demand_ratio'].append(market.demandRatio)
    trackers['ask_volume'].append(market.askVolume)
    trackers['bid_volume'].append(market.bidVolume)
    trackers['total_volume'].append(market.totalVolume)
    trackers['circulation'].append(market.getCirculation())

@app.route('/warmup')
def warmup():
    global cur_time
    NUM_TRADERS = trader_demographics['IdealTrader'] # We initially set it up with randomTraders

    for _ in range(NUM_ORDERS_INIT):
        market.usd_eth = 1.0 / get_eth_price(cur_time) 
        
        tid = randint(1, NUM_TRADERS)
        orders = traderPool[tid].marketStep()
        for order in orders:
            market.processOrder(order)
        cur_time += 1
        
    # Keep demandRatio constant at 0.5 when we start the market    
    market.demandRatio = 0.5
    return jsonify(market.prices['wavg_fair'][100:])

@app.route('/')
def hello_world():
    return 'Hello, World!'