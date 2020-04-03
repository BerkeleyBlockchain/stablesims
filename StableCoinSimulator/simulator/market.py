from collections import defaultdict
from .PyLOB import OrderBook
from .constants import *
from .traders import InvestorTrader
import numpy as np

class Market:
    def __init__(self):
        self.demandRatio = 0.5 # in [0, 1]
        
        # ETH Trades
        self.usd_eth = 0.01
        
        self.orderbook = OrderBook(tick_size=0.0001)
        self.traderPool = {}
        
        self.prices = defaultdict(list)
        self.prices['MAday'] = [0]
        self.protocol = None
        self.marketSpeed = MARKET_SPEED
        
        self.askVolume = 0
        self.bidVolume = 0
        self.totalVolume = 0
        self.volMAvel = 1. / VOL_MA_STEPS
        self.priceMAvel = 1. / PRICE_MA_STEPS
        
    def setTraderPool(self, traderPool):
        self.traderPool = traderPool
        
        if self.protocol:
            basis = 0
            for trader in traderPool.values():
                basis += trader.bas
            self.protocol.totalSupply = basis
        
        self.orderbook.setTraderPool(traderPool)
        
    def getIdealETHValue(self):
        return self.marketSpeed * self.usd_eth + (1 - self.marketSpeed) * self.getCurrentETHValue()
        
    def getCurrentUSDValue(self, func_type='wavg_fair'):
        return self.getCurrentETHValue(func_type) / self.usd_eth
        
    ''' Returns the value of BASIS in USD '''
    def getCurrentETHValue(self, func_type='wavg_fair'):
        def avg_bidask():
            return (self.orderbook.getBestBid() + self.orderbook.getBestAsk()) / 2
        
        def wavg_bidask():
            bid_price, ask_price = self.orderbook.getBestBid(), self.orderbook.getBestAsk()
            bid_vol = self.orderbook.getVolumeAtPrice('bid', bid_price)
            ask_vol = self.orderbook.getVolumeAtPrice('ask', ask_price)
            total_vol = bid_vol + ask_vol
            return (bid_price * ask_vol + ask_price * bid_vol) / total_vol
        
        if self.orderbook.getBestBid() is None:
            if self.orderbook.getBestAsk() is not None: 
                return self.orderbook.getBestAsk() # ask, not bid
            else:
                return self.usd_eth # not ask, not bid
        elif self.orderbook.getBestAsk() is None:
            return self.orderbook.getBestBid() # not ask, bid
        
        func_list = {'avg_fair': avg_bidask, 'wavg_fair': wavg_bidask}
        
        return func_list[func_type]()
        
    def setProtocol(self, protocol):
        self.protocol = protocol
        
    def updateDemandRatio(self, factor):
        self.demandRatio *= factor
        self.demandRatio = np.clip(self.demandRatio, 0.1, 1.0)
    
    def getCirculation(self):
        circulation = 0
        for trader in self.traderPool.values():
            if isinstance(trader, InvestorTrader):
                continue
            circulation += trader.bas
        return circulation

    def getMAprice(self):
        return self.prices['MAday'][-1]
        
    def updateDemand(self):
        # MAprice returns the bas_usd price
        bas_eth = self.getMAprice() * self.usd_eth
        usd_eth = self.usd_eth
        delta = 0
        
        # Demand varies on the price
        if bas_eth < usd_eth and self.demandRatio < 0.8:
            delta = (usd_eth - bas_eth) / usd_eth
            self.updateDemandRatio(1 + delta * PRICE_SCALE)
        elif bas_eth > usd_eth and self.demandRatio > 0.2:   
            delta = (bas_eth - usd_eth) / usd_eth
            self.updateDemandRatio(1 - delta * PRICE_SCALE)
            
        # Demand based on variation
        var = 1e2 * ((usd_eth - bas_eth) / usd_eth) ** 2
        
        if var <= 1e-2 and self.demandRatio < 0.6: # 1 cent 
            self.updateDemandRatio(1 + VAR_SCALE)
        else:
            self.updateDemandRatio(1 - var * VAR_SCALE)
        
    def processOrder(self, quote):
        trades, idNum = self.orderbook.processOrder(quote, False, False)
        
        volumeTraded = sum([trade['qty'] for trade in trades])
        askVolDelta, bidVolDelta = 0, 0
        if quote['side'] == 'bid':
            askVolDelta += volumeTraded
        if quote['side'] == 'ask':
            bidVolDelta += volumeTraded

        self.bidVolume = self.bidVolume * (1 - self.volMAvel) + bidVolDelta * self.volMAvel
        self.askVolume = self.askVolume * (1 - self.volMAvel) + askVolDelta * self.volMAvel
        self.totalVolume = self.bidVolume + self.askVolume
        
        # Calculates and saves the prices
        for func in ['avg_fair', 'wavg_fair']:
            self.prices[func].append(self.getCurrentUSDValue(func))
            
        maPrice = (self.prices['MAday'][-1] * (1 - self.priceMAvel) + 
                   self.getCurrentUSDValue('wavg_fair') * self.priceMAvel)
        
        self.prices['MAday'].append(maPrice)
            
        # Updates the Demand Ratio and Protocol (in case needs to react to price changes)
        self.updateDemand()
            
        if self.protocol is not None:
            self.protocol.update()
            
        return trades, idNum