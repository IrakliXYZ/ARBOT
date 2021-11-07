# This file keeps the program running and collects the data

# Import the necessary packages
import time, datetime, json

# Import sibling modules
import sourcer, builder


# Open folder Tracker and create a csv file for the data
def write_file(pair, leverage):
    # Open the file
    file = open("Tracker/" + pair + "/" + leverage + ".csv", "w")
    # Write data headers to csv file
    file.write("Time, Spread %, Funding Rate H, Funding Rate D, Profit D, Effective Rate D, Funding Rate W, Profit W, Effective Rate W, Funding Rate M, Profit M, Effective Rate M, Funding Rate Y, Profit Y, Effective Rate Y\n")


pairs = ['BTC', 'ETH', 'SOL', 'BNB', 'FTT', 'MATIC', 'XRP', 'LTC', 'SUSHI', 'RAY', 'LINK', 'CRV', 'COMP', 'GRT', '1INCH']
leverages = ['2x', '3x', '4x', '5x', '6x', '7x']


for pair in pairs:
    for leverage in leverages:
        # Open folder Tracker and create a csv file for the data
        def write_file(pair, leverage):
            # Open the file
            file = open("Tracker/" + pair + "/" + leverage + ".csv", "w")
            # Write data to csv file
            file.write(builder.data) # + "\n"
