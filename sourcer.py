# This file sources the data from FTX (more exchanges soon)

# Import the modules
import requests

# Variables
markets_url = "https://ftx.com/api/markets"
funding_url = "https://ftx.com/api/funding_rates"

available_FTX = ['BTC', 'ETH', 'SOL', 'BNB', 'FTT', 'MATIC', 'XRP', 'LTC', 'SUSHI', 'RAY', 'LINK', 'CRV', 'COMP', 'GRT', '1INCH']
available_leverages = [1, 2, 3, 4, 5, 6, 7]
markets_response = requests.get(markets_url).json()['result']
funding_response = requests.get(funding_url).json()['result']


# Get PERP price, ask, bid
def PERP(pair):
    for i in markets_response:
        if i['name'] == pair:
            PERP_price = i['last']
            PERP_ask = i['ask']
            PERP_bid = i['bid']
            return {'PERP_price': PERP_price, 'PERP_ask': PERP_ask, 'PERP_bid': PERP_bid}
# print(pair + "PERP", PERP()['PERP_price'])


# Get pair (/USD) price, ask, bid
def USD(pair):
    for i in markets_response:
        if i['name'] == pair:
            USD_price = i['last']
            USD_ask = i['ask']
            USD_bid = i['bid']
            return {'USD_price': USD_price, 'USD_ask': USD_ask, 'USD_bid': USD_bid}
# print(pair + "USD", USD()['USD_price'])


# Get funding rates (1hr, 1d=24hr, 1w=7d, 1m=30d, 1y=365d)
def funding_rates(pair):
    for i in funding_response:
        if i['future'] == pair:
            rate = "{:.8f}".format(float(i['rate']))
            return {'funding h': rate, 'funding d': float(rate) * 24, 'funding w': float(rate) * 24 * 7, 'funding m': float(rate) * 24 * 30, 'funding y': float(rate) * 24 * 365}
# print(funding_rates('BTC-PERP')['funding y'])