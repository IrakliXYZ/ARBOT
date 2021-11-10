# This file opens and closes positions on an exchange

# Import the modules
import os, ccxt

# Variables
api_key = os.environ['SUBACCOUNT_APIKEY']
api_secret = os.environ['SUBACCOUNT_SECRET']
subaccount = os.environ['SUBACCOUNT']


# Setup apis
exchange = ccxt.ftx({
    'enableRateLimit': True,
    'apiKey': api_key,
    'secret': api_secret,
    'headers': {'FTX-SUBACCOUNT': subaccount}
})


# Open market position on FTX
def open_position_market(pair, amount, leverage):
    # Buy on spot
    try:
        exchange.create_order(pair, 'market', 'buy', amount) # fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market buy:", e)
    
    # Short on futures
    try:
        exchange.create_order(pair, 'market', 'sell', amount, {'leverage': leverage}) # fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market short:", e)
# open_position_market('BTC-PERP', 0.0001, None, 2)


# Close market position on FTX
def close_position_market(pair, amount, leverage):
    # Sell on spot
    try:
        exchange.create_order(pair, 'market', 'sell', amount) # fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market sell:", e)
    
    # Long on futures
    try:
        exchange.create_order(pair, 'market', 'buy', amount, {'leverage': leverage}) # make reduce only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market long:", e)
# close_position_market('BTC-PERP', 0.0001, None, 2)




# Open limit position on FTX
def open_position_limit(pair, amount, leverage, price):
    # Buy on spot
    try:
        exchange.create_order(pair, 'limit', 'buy', amount, {'price': price}) # make post only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to limit buy:", e)
    
    # Short on futures
    try:
        exchange.create_order(pair, 'limit', 'sell', amount, {'price': price, 'leverage': leverage}) # make post only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to limit short:", e)


# Close limit position on FTX
def close_position_limit(pair, amount, leverage, price):
    # Sell on spot
    try:
        exchange.create_order(pair, 'limit', 'sell', amount, {'price': price}) # make post only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to limit sell:", e)
    
    # Long on futures
    try:
        exchange.create_order(pair, 'limit', 'buy', amount, {'price': price, 'leverage': leverage}) # make post only, fill or kill (IOC), reduce only
    except ccxt.ExchangeError as e:
        print("While trying to limit long:", e)