# This file crunches the numbers

# Import the necessary packages
import os

# Import sibling modules
import sourcer

# Variables
maker_fee = float(os.getenv('MAKER_FEE'))
taker_fee = float(os.getenv('TAKER_FEE'))


# Calculate the percent difference between BTC-PERP and BTC/USD
def difference(A, B):
    return (A - B) / B
# print(difference(BTCPERP()['BTCPERP_price'], BTCUSD()['BTCUSD_price']))


# Calculate possible profits (amount, funding_rate, trading_fee, difference, leverage)
def profit(amount, funding_rate, trading_fee, difference, leverage):
    working_amount = amount * (leverage / (leverage + 1))
    traded_amount = amount * 2
    
    return (working_amount * funding_rate) - (traded_amount * trading_fee * 2) - (traded_amount * difference)


# Effective rate calculator
def effective_rate_calculator(profit, amount):
    return (profit / amount) * 100