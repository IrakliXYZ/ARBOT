# This file keeps the program running and collects the data (FTX)

# Import the necessary packages
import time, csv

# Import sibling modules
import builder

# Variables and lists
pairs = ['BTC', 'ETH', 'SOL', 'BNB', 'FTT', 'MATIC', 'XRP', 'LTC', 'SUSHI', 'RAY', 'LINK', 'CRV', 'COMP', 'GRT', '1INCH']
leverages = [2, 3, 4, 5, 6, 7]
field_names = ['date_time', 'spread', 'funding_rate_h', 'funding_rate_w', 'profit_w', 'effective_rate_w', 'funding_rate_m', 'profit_m', 'effective_rate_m', 'funding_rate_y', 'profit_y', 'effective_rate_y']


# Open folder Tracker and create a csv file for the data
def make_file(pair, leverage):
    # Open the file
    file = open("Tracker/" + pair + "/" + str(leverage) + "x.csv", "w")
    # Write data headers to csv file
    file.write("Time, Spread %, Funding Rate %/H, Funding Rate %/W, Profit W, Effective Rate %/W, Funding Rate %/M, Profit M, Effective Rate %/M, Funding Rate %/Y, Profit Y, Effective Rate %/Y\n")
    print('done')


def write_file(pair, leverage):
            print("Writing file for pair: " + pair + " and leverage: " + str(leverage))
            # Open folder Tracker and corresponding pair and leverage
            with open("Tracker/" + pair + "/" + str(leverage) + "x" + ".csv", 'a') as csvfile:
                # Add data to a file
                writer = csv.writer(csvfile)
                writer.writerow(builder.generate_list(pair, leverage))

while True:
    # Loop through all pairs and leverages
    for pair in pairs:
        for leverage in leverages:
            write_file(pair, leverage)
    # Wait for 1 hour
    time.sleep(3600)