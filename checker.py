# This file checks the funding fees and the balance of the account (FTX)

import os
import ccxt

# def table(values):
#     first = values[0]
#     keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
#     widths = [max([len(str(v[k])) for v in values]) for k in keys]
#     string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
#     return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


api_key = os.environ['FTX_APIKEY']
api_secret = os.environ['FTX_SECRET']
subaccount = os.environ['FTX_SUBACCOUNT']
exchange = ccxt.ftx({
            'apiKey': api_key,
            'secret': api_secret,
            'headers': {'FTX-SUBACCOUNT': subaccount},
            'enableRateLimit': True,
        })


# start = exchange.parse8601('2020-11-01T00:00:00Z')  # timestamp in milliseconds
# end = exchange.milliseconds()  # current timestamp in milliseconds

request = {
    # 'start_time': int(start / 1000),  # unix timestamp in seconds, optional
    # 'end_time': int(end / 1000),  # unix timestamp in seconds, optional
    # 'future': 'BTC-PERP',  # optional
}


response = exchange.private_get_funding_payments(request)


def sum_funding_payments():
    sum = 0
    for i in exchange.safe_value(response, 'result', []):
        if i['future'] == 'RAY-PERP':
            sum = sum + float(i['payment'])
    return sum * -1
# print(sum_funding_payments())