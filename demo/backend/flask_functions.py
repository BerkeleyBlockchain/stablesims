import sys
sys.path.append("/Users/andrew/projects/bab-stablecoin_sims_research/demo/backend/simulator/PYLOB")

from random import randint
from simulator import *
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit, send
from eventlet import monkey_patch

monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'satoshi'
app.debug = True
app.host = 'localhost'

socketio = SocketIO(app, cors_allowed_origins="*")

def track(trackers, market):
    trackers['usd_eth'].append(market.usd_eth)
    trackers['bond_q_len'].append(market.protocol.bondQueueLength)
    trackers['demand_ratio'].append(market.demandRatio)
    trackers['ask_volume'].append(market.askVolume)
    trackers['bid_volume'].append(market.bidVolume)
    trackers['total_volume'].append(market.totalVolume)
    trackers['circulation'].append(market.getCirculation())

def warmup(market):
    NUM_TRADERS = market.params["trader_demographics"]['IdealTrader'] # We initially set it up with randomTraders
    TRACK_FREQ = market.params["TRACK_FREQ"]

    for i in range(market.params["NUM_ORDERS_INIT"]):
        market.usd_eth = 1.0 / get_eth_price(market.cur_time, market)
        if i % TRACK_FREQ == 0:
            emit("warmup", market.prices['wavg_fair'][-TRACK_FREQ:])
            socketio.sleep(0.01)

        tid = randint(1, NUM_TRADERS)
        orders = market.traderPool[tid].marketStep()
        for order in orders:
            market.processOrder(order)
        market.cur_time += 1

    # Keep demandRatio constant at 0.5 when we start the market
    market.demandRatio = 0.5
    

def trade(market, trackers):
    NUM_TRADERS = market.params["trader_demographics"]['AverageTrader'] + market.params["trader_demographics"]['BasicTrader']
    OFFSET_TRADERS = market.params["trader_demographics"]['IdealTrader']
    TRACK_FREQ = market.params["TRACK_FREQ"]

    for i in range(market.params["NUM_ORDERS_LIVE"]):
        market.usd_eth = 1 / get_eth_price(market.cur_time, market) 
        if i % TRACK_FREQ == 0:
            track(trackers, market)
            emit("data", market.prices['MAday'][-TRACK_FREQ:])
            socketio.sleep(0.01)

        tid = randint(OFFSET_TRADERS + 1, OFFSET_TRADERS + NUM_TRADERS)
        orders = market.traderPool[tid].marketStep()
        for order in orders:
            market.processOrder(order)    
        market.cur_time += 1
            


@socketio.on("run")
def run(params):
    params = Params(params)
    market = Market(params)
    basis = BasisProtocol(int(1e7), market)
    market.protocol = basis
    traderPool = createTraderPool(basis, market, market.params["trader_demographics"])
    market.setTraderPool(traderPool)

    market.usd_eth = 1 / get_eth_price(0, market)

    trackers = {'usd_eth': [], 'bond_q_len': [], 'demand_ratio': [], 'ask_volume': [],
                'bid_volume': [], 'total_volume': [], 'circulation': []}

    TRACK_FREQ = market.params["TRACK_FREQ"]

    warmup(market)

    emit("warmup", market.prices['wavg_fair'][-TRACK_FREQ:])
    socketio.sleep(0.01)

    trade(market, trackers)

    emit("data", market.prices['MAday'][-TRACK_FREQ:])
    emit("trackers", trackers)

socketio.run(app)