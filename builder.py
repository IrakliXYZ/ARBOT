# This file builds the tables and dictionaries

# Import the modules
import os

# Import sibling modules
import calculator, sourcer

# Variables
maker_fee = float(os.getenv('MAKER_FEE'))
taker_fee = float(os.getenv('TAKER_FEE'))

# Table maker
def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


# Generate only list dictionary
def generate_list(amnt, lvrg, period):
    available_FTX = sourcer.available_FTX

    data = []

    # Loop through available coins and append to the list
    for i in available_FTX:
        pair_funding_rate = float(sourcer.funding_rates(i + '-PERP')['funding ' + period])
        calculated_spread = float(calculator.difference(sourcer.PERP(i + '-PERP')['PERP_price'], sourcer.USD(i + '/USD')['USD_price'])) * 100
        calculated_profit = calculator.profit(amnt, pair_funding_rate, maker_fee, calculated_spread, lvrg)
        data.append({
            'pair': i,
            'funding_rate': pair_funding_rate * 100,
            'spread': calculated_spread,
            'profit': calculated_profit,
            'effective_rate': calculator.effective_rate_calculator(calculated_profit, amnt)
        })
    return data
# print(generate_table(10000, 3, 'w'))


# Generate a printable table of all available pairs with a header
def generate_table(amnt, lvrg, period):
    available_FTX = sourcer.available_FTX

    data = []

    # Make a data header
    data.append({
        'pair': 'Name',
        'funding_rate': 'Funding %/' + period,
        'spread': 'Spread %',
        'profit': 'Profits $',
        'effective_rate': 'Effective Rate %/' + period
    })

    # Loop through available coins and append to the list
    for i in available_FTX:
        pair_funding_rate = float(sourcer.funding_rates(i + '-PERP')['funding ' + period])
        calculated_spread = float(calculator.difference(sourcer.PERP(i + '-PERP')['PERP_price'], sourcer.USD(i + '/USD')['USD_price'])) * 100
        calculated_profit = calculator.profit(amnt, pair_funding_rate, maker_fee, calculated_spread, lvrg)
        data.append({
            'pair': i,
            'funding_rate': "{:.4f}".format(pair_funding_rate * 100),
            'spread': "{:.4f}".format(calculated_spread),
            'profit': "{:.2f}".format(calculated_profit),
            'effective_rate': "{:.2f}".format(calculator.effective_rate_calculator(calculated_profit, amnt))
        })
    return table(data)
# print(generate_table())