# This file builds the tables and dictionaries (FTX)

# Import the modules
import os, datetime

# Import sibling modules
import calculator, FTX_sourcer

# Variables
maker_fee = float(os.getenv('FTX_MAKER_FEE'))
taker_fee = float(os.getenv('FTX_TAKER_FEE'))

# Table maker
def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


# Generate only list dictionary
def generate_list(pair, lvrg):
    amnt = 10000.00
    pair_funding_rate = FTX_sourcer.funding_rates(pair + '-PERP')
    pair_funding_rate_h = float(pair_funding_rate['funding h'])
    pair_funding_rate_d = float(pair_funding_rate['funding d'])
    pair_funding_rate_w = float(pair_funding_rate['funding w'])
    pair_funding_rate_m = float(pair_funding_rate['funding m'])
    pair_funding_rate_y = float(pair_funding_rate['funding y'])
    calculated_spread = float(calculator.difference(FTX_sourcer.PERP(pair + '-PERP')['PERP_price'], FTX_sourcer.USD(pair + '/USD')['USD_price']))

    # data.append({
    #     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     calculated_spread,
    #     pair_funding_rate_h * 100,
    #     pair_funding_rate_d * 100,
    #     calculator.profit(amnt, pair_funding_rate_d, maker_fee, calculated_spread, lvrg),
    #     calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_d, maker_fee, calculated_spread, lvrg), amnt),
    #     pair_funding_rate_w * 100,
    #     calculator.profit(amnt, pair_funding_rate_w, maker_fee, calculated_spread, lvrg),
    #     calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_w, maker_fee, calculated_spread, lvrg), amnt),
    #     pair_funding_rate_m * 100,
    #     calculator.profit(amnt, pair_funding_rate_m, maker_fee, calculated_spread, lvrg), 
    #     calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_m, maker_fee, calculated_spread, lvrg), amnt), 
    #     pair_funding_rate_y * 100, calculator.profit(amnt, pair_funding_rate_y, maker_fee, calculated_spread, lvrg), 
    #     calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_y, maker_fee, calculated_spread, lvrg), amnt)
    # })
    # return data



    # return {
    #     # 'pair': pair,
    #     # 'amount': amnt,
    #     # 'leverage': lvrg,
    #     'date_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'spread %': calculated_spread,
    #     'funding_rate_h': pair_funding_rate_h * 100,
    #     'funding_rate_d': pair_funding_rate_d * 100,
    #     'profit_d': calculator.profit(amnt, pair_funding_rate_d, maker_fee, calculated_spread, lvrg),
    #     'effective_rate_d': calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_d, maker_fee, calculated_spread, lvrg), amnt),
    #     'funding_rate_w': pair_funding_rate_w * 100,
    #     'profit_w': calculator.profit(amnt, pair_funding_rate_w, maker_fee, calculated_spread, lvrg),
    #     'effective_rate_w': calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_w, maker_fee, calculated_spread, lvrg), amnt),
    #     'funding_rate_m': pair_funding_rate_m * 100,
    #     'profit_m': calculator.profit(amnt, pair_funding_rate_m, maker_fee, calculated_spread, lvrg),
    #     'effective_rate_m': calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_m, maker_fee, calculated_spread, lvrg), amnt),
    #     'funding_rate_y': pair_funding_rate_y * 100,
    #     'profit_y': calculator.profit(amnt, pair_funding_rate_y, maker_fee, calculated_spread, lvrg),
    #     'effective_rate_y': calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_y, maker_fee, calculated_spread, lvrg), amnt)
    # }


    return [
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        calculated_spread * 100,
        pair_funding_rate_h * 100,
        pair_funding_rate_w * 100,
        calculator.profit(amnt, pair_funding_rate_w, maker_fee, calculated_spread, lvrg),
        calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_w, maker_fee, calculated_spread, lvrg), amnt),
        pair_funding_rate_m * 100,
        calculator.profit(amnt, pair_funding_rate_m, maker_fee, calculated_spread, lvrg), 
        calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_m, maker_fee, calculated_spread, lvrg), amnt), 
        pair_funding_rate_y * 100,
        calculator.profit(amnt, pair_funding_rate_y, maker_fee, calculated_spread, lvrg), 
        calculator.effective_rate_calculator(calculator.profit(amnt, pair_funding_rate_y, maker_fee, calculated_spread, lvrg), amnt)
    ]
# print(generate_table(10000, 3))


# Generate a printable table of all available pairs with a header
def generate_table(amnt, lvrg, period):
    available_FTX = FTX_sourcer.available_FTX

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
        pair_funding_rate = float(FTX_sourcer.funding_rates(i + '-PERP')['funding ' + period])
        calculated_spread = float(calculator.difference(FTX_sourcer.PERP(i + '-PERP')['PERP_price'], FTX_sourcer.USD(i + '/USD')['USD_price']))
        calculated_profit = calculator.profit(amnt, pair_funding_rate, taker_fee, calculated_spread, lvrg)
        data.append({
            'pair': i,
            'funding_rate': "{:.4f}".format(pair_funding_rate * 100),
            'spread': "{:.4f}".format(calculated_spread * 100),
            'profit': "{:.2f}".format(calculated_profit),
            'effective_rate': "{:.2f}".format(calculator.effective_rate_calculator(calculated_profit, amnt))
        })
    return table(data)
# print(generate_table())