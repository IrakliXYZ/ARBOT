# # list available perp usd pairs v2
# # get the funding rates for btc +
# # find the best one v2
# # get prices/quotes +
# # calculate the difference +
# # get funding rates

# # get volumes/liquidity for a given amount (from orderbook)
# # calculate possible profits
# # if everything looks good, open a position (v2 will save fees by putting near market price maker orders)
# # if funding rate is positive (lots of longs) short the market with 3x leverage
# # buy spot with more real money
# # error check

# # for v2 - compounding the profits, saving with maker fees, finding best opportunities on multiple markets, 

# # Import the necessary packages
# import os, sys, ccxt, requests, time, datetime, json


# # Setup apis
# exchange = ccxt.ftx({
#     'enableRateLimit': True,
#     'apiKey': os.getenv('APIKEY'),
#     'secret': os.getenv('SECRET')
# })


# # Variables
# markets_url = "https://ftx.com/api/markets"
# funding_url = "https://ftx.com/api/funding_rates"
# maker_fee = float(os.getenv('MAKER_FEE'))
# taker_fee = float(os.getenv('TAKER_FEE'))
# amnt = float(input('Amount of money to invest: '))
# lvrg = float(input('Intended leverage (1-5): '))
# period = input('Period (hr, d, w, m, y): ')

# Available_FTX = ['BTC', 'ETH', 'SOL', 'BNB', 'FTT', 'MATIC', 'XRP', 'LTC', 'SUSHI', 'RAY', 'LINK', 'CRV', 'COMP', 'GRT', '1INCH']
# markets_response = requests.get(markets_url).json()['result']
# funding_response = requests.get(funding_url).json()['result']


# # Table maker
# def table(values):
#     first = values[0]
#     keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
#     widths = [max([len(str(v[k])) for v in values]) for k in keys]
#     string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
#     return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


# # Get PERP price, ask, bid
# def PERP(pair):
#     for i in markets_response:
#         if i['name'] == pair:
#             PERP_price = i['last']
#             PERP_ask = i['ask']
#             PERP_bid = i['bid']
#             return {'PERP_price': PERP_price, 'PERP_ask': PERP_ask, 'PERP_bid': PERP_bid}
# # print(pair + "PERP", PERP()['PERP_price'])


# # Get pair (/USD) price, ask, bid
# def USD(pair):
#     for i in markets_response:
#         if i['name'] == pair:
#             USD_price = i['last']
#             USD_ask = i['ask']
#             USD_bid = i['bid']
#             return {'USD_price': USD_price, 'USD_ask': USD_ask, 'USD_bid': USD_bid}
# # print(pair + "USD", USD()['USD_price'])


# # Calculate the percent difference between BTC-PERP and BTC/USD
# def difference(A, B):
#     return (A - B) / B
# # print(difference(BTCPERP()['BTCPERP_price'], BTCUSD()['BTCUSD_price']))


# # Get funding rates (1hr, 1d=24hr, 1w=7d, 1m=30d, 1y=365d)
# def funding_rates(pair):
#     for i in funding_response:
#         if i['future'] == pair:
#             rate = "{:.8f}".format(float(i['rate']))
#             return {'funding hr': rate, 'funding d': float(rate) * 24, 'funding w': float(rate) * 24 * 7, 'funding m': float(rate) * 24 * 30, 'funding y': float(rate) * 24 * 365}
# # print(funding_rates('BTC-PERP')['funding y'])


# # Calculate possible profits (amount, funding_rate, trading_fee, difference, leverage)
# def profit(amount, funding_rate, trading_fee, difference, leverage):
#     working_amount = amount * (leverage / (leverage + 1))
#     traded_amount = amount * 2
#     # print ("revenues =",(working_amount * funding_rate))
#     # print ("fees =",(traded_amount * trading_fee * 2))
#     # print ("difference =", (traded_amount * difference))
#     # print ("total =", (working_amount * funding_rate) - (traded_amount * trading_fee * 2) - (traded_amount * difference))
#     return (working_amount * funding_rate) - (traded_amount * trading_fee * 2) - (traded_amount * difference)


# # Effective rate calculator
# def effective_rate_calculator(profit, amount):
#     return (profit / amount) * 100


# # Generate a list of all available pairs
# def generate_list():
#     # Make a data header
#     data = []
#     data.append({
#         'pair': 'Name',
#         'funding_rate': 'Funding %/' + period,
#         'spread': 'Spread %',
#         'profit': 'Profits $',
#         'effective_rate': 'Effective Rate %/' + period
#     })

#     # loop through available coins and append to the list
#     for i in Available_FTX:
#         data.append({
#             'pair': i,
#             'funding_rate': "{:.5f}".format(float(funding_rates(i + '-PERP')['funding ' + period])),
#             'spread': "{:.5f}".format(float(difference(PERP(i + '-PERP')['PERP_price'], USD(i + '/USD')['USD_price'])) * 100),
#             'profit': "{:.2f}".format(profit(amnt, float(funding_rates(i + '-PERP')['funding ' + period]), maker_fee, difference(PERP(i + '-PERP')['PERP_price'], USD(i + '/USD')['USD_price']), lvrg)),
#             'effective_rate': "{:.3f}".format(effective_rate_calculator(profit(amnt, float(funding_rates(i + '-PERP')['funding ' + period]), maker_fee, difference(PERP(i + '-PERP')['PERP_price'], USD(i + '/USD')['USD_price']), lvrg), amnt))
#         })
#     return data
    

# data = generate_list()
# print(table(data))

# # # for loop to find the best rate
# # for i in data:
# #     if i['effective_rate'] == max(data, key=lambda x: x['effective_rate'])['effective_rate']:
# #         print("The best rate is:", i['pair'], "with an effective rate of", i['effective_rate'], "%/", period)
# 
# TODO:
# # for loop to find the best rate
# for i in data:
#     if i['effective_rate'] == max(data, key=lambda x: x['effective_rate'])['effective_rate']:
#         print("The best rate is:", i['pair'], "with an effective rate of", i['effective_rate'], "%/", period)


# Import sibling modules
import builder, tracker

amnt = float(input('Amount of money to invest: '))
lvrg = float(input('Intended leverage (1-5): '))
period = input('Period (h, d, w, m, y): ')


# print(builder.generate_table(amnt, lvrg, period))
tracker