# # list available perp usd pairs v2
# # get the funding rates for btc +
# # find the best one v2
# # get prices/quotes +
# # calculate the difference +
# # get funding rates
# # calculate possible profits

# # get volumes/liquidity for a given amount (from orderbook)
# # if everything looks good, open a position (v2 will save fees by putting near market price maker orders)
# # if funding rate is positive (lots of longs) short the market with 3x leverage
# # buy spot with more real money
# # error check

# # for v2 - compounding the profits, saving with maker fees, finding best opportunities on multiple markets, 

# # Import the necessary packages
# import os, sys, ccxt, requests, time, datetime, json


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
import builder, controller

# exchange = input('Enter the exchange you want to use: (ftx) ')
# action = input('Enter the action you want to perform: (open, close) ')
# coin = input('Enter the pair you want to use: (BTC, ETH, SOL...) ')
# amount = float(input('Amount of money to invest: '))
# leverage = float(input('Intended leverage (1-5): '))
# # period = input('Period (h, d, w, m, y): ')
# price = None

# controller.set_exchange(exchange, action, coin, amount, leverage, price)

print(builder.generate_table(1000, 2, 'm'))