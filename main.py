# list available perp usd pairs v2
# get the funding rates for btc +
# find the best one v2
# get prices/quotes +
# calculate the difference +
# get funding rates + (error checking?)

# get volumes/liquidity for a given amount (from orderbook)
# calculate possible profits
# if everything looks good, open a position (v2 will save fees by putting near market price maker orders)
# if funding rate is positive (lots of longs) short the market with 3x leverage
# buy spot with more real money
# error check

# for v2 - compounding the profits, saving with maker fees, finding best opportunities on multiple markets, 

# Import the necessary packages
import os, sys, ccxt, requests, time, datetime, json


# Setup apis
exchange = ccxt.ftx({
    'enableRateLimit': True,
    'apiKey': os.getenv('APIKEY'),
    'secret': os.getenv('SECRET')
})


# Variables
markets_url = "https://ftx.com/api/markets"
funding_url = "https://ftx.com/api/funding_rates"
maker_fee = float(os.getenv('MAKER_FEE'))
taker_fee = float(os.getenv('TAKER_FEE'))

# Table maker
def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


# Get PERP price, ask, bid
def PERP(pair):
    response = requests.get(markets_url).json()['result']
    for i in response:
        if i['name'] == pair:
            PERP_price = i['last']
            PERP_ask = i['ask']
            PERP_bid = i['bid']
            return {'PERP_price': PERP_price, 'PERP_ask': PERP_ask, 'PERP_bid': PERP_bid}
# print(pair + "PERP", PERP()['PERP_price'])


# Get pair (/USD) price, ask, bid
def USD(pair):
    response = requests.get(markets_url).json()['result']
    for i in response:
        if i['name'] == pair:
            USD_price = i['last']
            USD_ask = i['ask']
            USD_bid = i['bid']
            return {'USD_price': USD_price, 'USD_ask': USD_ask, 'USD_bid': USD_bid}
# print(pair + "USD", USD()['USD_price'])


# Calculate the percent difference between BTC-PERP and BTC/USD
def difference(A, B):
    return (A - B) / B
# print(difference(BTCPERP()['BTCPERP_price'], BTCUSD()['BTCUSD_price']))

# Get funding rates (1hr, 1d=24hr, 1w=7d, 1m=30d, 1y=365d)
def funding_rates(pair):
    response = requests.get(funding_url).json()['result']
    for i in response:
        if i['future'] == pair:
            rate = "{:.8f}".format(float(i['rate']))
            return {'funding hr': rate, 'funding d': float(rate) * 24, 'funding w': float(rate) * 24 * 7, 'funding m': float(rate) * 24 * 30, 'funding y': float(rate) * 24 * 365}
# print(funding_rates('BTC-PERP')['funding y'])

# Calculate possible profits (amount, funding_rate, trading_fee, difference, leverage)
def profit(amount, funding_rate, trading_fee, difference, leverage):
    working_amount = amount * (leverage / (leverage + 1))
    traded_amount = amount * 2
    # print ("revenues =",(working_amount * funding_rate))
    # print ("fees =",(traded_amount * trading_fee * 2))
    # print ("difference =", (traded_amount * difference))
    # print ("total =", (working_amount * funding_rate) - (traded_amount * trading_fee * 2) - (traded_amount * difference))
    return (working_amount * funding_rate) - (traded_amount * trading_fee * 2) - (traded_amount * difference)


# APR calculator
def apr_calculator(profit, amount):
    return (profit / amount) * 100

yearly_profit_btc = profit(10000, float(funding_rates('BTC-PERP')['funding y']), taker_fee, difference(PERP('BTC-PERP')['PERP_price'], USD('BTC/USD')['USD_price']), 3)
yearly_profit_eth = profit(10000, float(funding_rates('ETH-PERP')['funding y']), taker_fee, difference(PERP('ETH-PERP')['PERP_price'], USD('ETH/USD')['USD_price']), 3)
yearly_profit_sol = profit(10000, float(funding_rates('SOL-PERP')['funding y']), taker_fee, difference(PERP('SOL-PERP')['PERP_price'], USD('SOL/USD')['USD_price']), 3)

data = []

# loop through available coins and append to the list
data.append({
    'pair': 'Pair Name',
    'funding_rate': 'Funding Rate',
    'trading_fee': 'Trading Fees',
    'difference': 'Difference',
    'leverage': 'Leverage',
    'profit': 'Yearly Profits',
    'apr': 'APR'
})
data.append({
    'pair': 'BTC-PERP',
    'funding_rate': float(funding_rates('BTC-PERP')['funding y']),
    'trading_fee': taker_fee,
    'difference': difference(PERP('BTC-PERP')['PERP_price'], USD('BTC/USD')['USD_price']),
    'leverage': 3,
    'profit': yearly_profit_btc,
    'apr': apr_calculator(yearly_profit_btc, 10000)
})
data.append({
    'pair': 'ETH-PERP',
    'funding_rate': float(funding_rates('ETH-PERP')['funding y']),
    'trading_fee': taker_fee,
    'difference': difference(PERP('ETH-PERP')['PERP_price'], USD('ETH/USD')['USD_price']),
    'leverage': 3,
    'profit': yearly_profit_eth,
    'apr': apr_calculator(yearly_profit_eth, 10000)
})
data.append({
    'pair': 'SOL-PERP',
    'funding_rate': float(funding_rates('SOL-PERP')['funding y']),
    'trading_fee': taker_fee,
    'difference': difference(PERP('SOL-PERP')['PERP_price'], USD('SOL/USD')['USD_price']),
    'leverage': 3,
    'profit': yearly_profit_sol,
    'apr': apr_calculator(yearly_profit_sol, 10000)
})

print(table(data))