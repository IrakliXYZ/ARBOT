# This file opens and closes positions on an exchange (FTX, soon Binance)

# Import the modules
import os, ccxt


# Set settings for the exchange
def set_exchange(exchange, action, pair, amount, leverage, price):

    if exchange == 'ftx':
        api_key = os.environ['FTX_APIKEY']
        api_secret = os.environ['FTX_SECRET']
        subaccount = os.environ['FTX_SUBACCOUNT']
        exchange = ccxt.ftx({
                    'apiKey': api_key,
                    'secret': api_secret,
                    'headers': {'FTX-SUBACCOUNT': subaccount},
                    'enableRateLimit': True,
                })
        take_action(exchange, action, pair, amount, leverage, price)

    elif exchange == 'binance':
        api_key = os.environ['BINANCE_API_KEY']
        api_secret = os.environ['BINANCE_SECRET']
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        take_action(exchange, action, pair, amount, leverage, price)

    # elif exchange == 'coinbase':
    #     api_key = os.environ['COINBASE_API_KEY']
    #     api_secret = os.environ['COINBASE_SECRET']
    #     exchange = ccxt.coinbase({
    #         'apiKey': api_key,
    #         'secret': api_secret,
    #         'enableRateLimit': True,
    #     })
    #     take_action(exchange, action, pair, amount, leverage, price)

    # elif exchange == 'huobi':
    #     api_key = os.environ['HUOBI_API_KEY']
    #     api_secret = os.environ['HUOBI_SECRET']
    #     exchange = ccxt.huobi({
    #         'apiKey': api_key,
    #         'secret': api_secret,
    #         'enableRateLimit': True,
    #     })
    #     take_action(exchange, action, pair, amount, leverage, price)

    # elif exchange == 'kucoin':
    #     api_key = os.environ['KUCOIN_API_KEY']
    #     api_secret = os.environ['KUCOIN_SECRET']
    #     exchange = ccxt.kucoin({
    #         'apiKey': api_key,
    #         'secret': api_secret,
    #         'enableRateLimit': True,
    #     })
    #     take_action(exchange, action, pair, amount, leverage, price)

    else:
        print('Exchange not supported')


# Take action
def take_action(exchange, action, coin, amount, leverage, price):
    if action == 'open':
        open_position_market(exchange, coin, amount, leverage)
    elif action == 'close':
        close_position_market(exchange, coin, amount, leverage)
    elif action == 'open_limit':
        open_position_limit(exchange, coin, amount, leverage, price)
    elif action == 'close_limit':
        close_position_limit(exchange, coin, amount, leverage, price)
    else:
        print("Action not recognized")




# Actions
# Open market position on FTX
def open_position_market(exchange, coin, amount, leverage):
    # Set variables
    spot_pair = coin + '/USD'
    futures_pair = coin + '-PERP'

    # Buy on spot
    try:
        exchange.create_order(spot_pair, 'market', 'buy', amount) # fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market buy:", e)
    
    # Short on futures
    try:
        exchange.create_order(futures_pair, 'market', 'sell', amount, {'leverage': leverage}) # fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market short:", e)
# open_position_market('BTC-PERP', 0.0001, None, 2)


# Close market position on FTX
def close_position_market(exchange, coin, amount, leverage):
    # Set variables
    spot_pair = coin + '/USD'
    futures_pair = coin + '-PERP'

    # Sell on spot
    try:
        exchange.create_order(spot_pair, 'market', 'sell', amount) # fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market sell:", e)
    
    # Long on futures
    try:
        exchange.create_order(futures_pair, 'market', 'buy', amount, {'leverage': leverage}) # make reduce only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to market long:", e)
# close_position_market('BTC-PERP', 0.0001, None, 2)


# Limits
# Open limit position on FTX
def open_position_limit(exchange, coin, amount, leverage, price):
    # Set variables
    spot_pair = coin + '/USD'
    futures_pair = coin + '-PERP'
    
    # Buy on spot
    try:
        exchange.create_order(spot_pair, 'limit', 'buy', amount, {'price': price}) # make post only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to limit buy:", e)
    
    # Short on futures
    try:
        exchange.create_order(futures_pair, 'limit', 'sell', amount, {'price': price, 'leverage': leverage}) # make post only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to limit short:", e)


# Close limit position on FTX
def close_position_limit(exchange, coin, amount, leverage, price):
    # Set variables
    spot_pair = coin + '/USD'
    futures_pair = coin + '-PERP'
    
    # Sell on spot
    try:
        exchange.create_order(spot_pair, 'limit', 'sell', amount, {'price': price}) # make post only, fill or kill (IOC)
    except ccxt.ExchangeError as e:
        print("While trying to limit sell:", e)
    
    # Long on futures
    try:
        exchange.create_order(futures_pair, 'limit', 'buy', amount, {'price': price, 'leverage': leverage}) # make post only, fill or kill (IOC), reduce only
    except ccxt.ExchangeError as e:
        print("While trying to limit long:", e)
