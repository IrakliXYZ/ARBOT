# This file keeps the program running and collects the data

# Import the necessary packages
import time, datetime, json

# Import sibling modules
import sourcer, builder

# pairs, that have leverages, that have data (spread, profit, effective rate...) that have hourly data
while True:
    for pair in sourcer.available_FTX:
        for leverage in sourcer.available_leverages:
            # Get the data
            data = builder.generate_list(pair, 10000, leverage)

            # Add the data to the json file
            with open('tracker.json', 'a') as f:
                # Problem here: need to format correctly in multidimensional way
                f.write(json.dumps({'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'pair': pair, 'leverage': leverage, 'data': data} ))
                f.write(',\n')

    # Wait for the next hour
    time.sleep(10)

# loop that runs every hour and adds the builder.generate_list(pair, amnt, lvrg) data to the json file



