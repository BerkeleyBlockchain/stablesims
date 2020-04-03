from collections import OrderedDict

# ETH trading settings
ETH_DAY_OFFSET = 0
TRADES_PER_DAY = 15000

# BOND settings
BOND_EXPIRY = 60 * (30 * 24 * 60 * 60) # 60 months
BOND_DELAY = 15000 # Steps 
BOND_RANGE = (0.99, 1.01)

# MARKET price settings 
BASE_SPREAD = 1e-3 # 0.1% 
PRICE_NOISE = 1e-4
VOL_MA_STEPS = 1000
PRICE_MA_STEPS = 1000
MARKET_SPEED = 0.2

# DEMAND ratio settings
PRICE_SCALE = 1e-4
VAR_SCALE = 5e-4

# TRADER settings
BASIC_TRADER_THRESHOLD = 0.02 # trades when BAS < 0.95 or BAS > 1.05

# TRADER demographics 
trader_demographics = OrderedDict()
trader_demographics['IdealTrader'] = 5
trader_demographics['AverageTrader'] = 500
trader_demographics['BasicTrader'] = 200
trader_demographics['InvestorTrader'] = 5

# SIMULATION SETTINGS 
NUM_ORDERS_INIT = PRICE_MA_STEPS * 3
NUM_ORDERS_LIVE = 600000

# TRACKING settings 
TRACK_FREQ = 100 # Track every 50 steps

# NOTES
'''
    Can do 
        trades, idNum = market.processOrder(order)
    But don't use the return values unless needed for processing
    
    The orderbook is modified. It takes in the traderpool and messes with their balances. 
    Ideally this should be done in the market but its a pain in the butt. 
''' 
