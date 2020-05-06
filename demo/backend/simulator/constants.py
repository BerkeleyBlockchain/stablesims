from collections import OrderedDict

def Params(params):
    trader_demographics = OrderedDict()
    trader_demographics['IdealTrader'] = 5
    trader_demographics['AverageTrader'] = 500
    trader_demographics['BasicTrader'] = 100
    trader_demographics['InvestorTrader'] = 5

    defaults = {
        "ETH_DAY_OFFSET": 0,
        "TRADES_PER_DAY": 15000,
        "BOND_EXPIRY": 60 * (30 * 24 * 60 * 60),
        "BOND_DELAY": 15000,
        "BOND_RANGE": (0.99, 1.01),
        "BASE_SPREAD": 1e-3,
        "PRICE_NOISE": 1e-4,
        "VOL_MA_STEPS": 1000,
        "PRICE_MA_STEPS": 1000,
        "MARKET_SPEED": 0.2,
        "PRICE_SCALE": 1e-4,
        "VAR_SCALE": 1e-5,
        "BASIC_TRADER_THRESHOLD": 0.02,
        "trader_demographics": trader_demographics,
        "NUM_ORDERS_INIT": 3000,
        "NUM_ORDERS_LIVE": 600000,
        "TRACK_FREQ": 1000
    }

    for key in params:
        defaults[key] = params[key]
    
    return defaults

# NOTES
'''
    Can do 
        trades, idNum = market.processOrder(order)
    But don't use the return values unless needed for processing
    
    The orderbook is modified. It takes in the traderpool and messes with their balances. 
    Ideally this should be done in the market but its a pain in the butt. 
''' 