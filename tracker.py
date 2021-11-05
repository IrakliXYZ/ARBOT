# This file keeps the program running and collects the data

# Import the necessary packages
import time

# Import sibling modules
import sourcer, builder

# # Run the script every hour and add the results to csv file
# while True:
#     def write_to_csv():
#         with open('tracker.csv', 'a') as f:
#             f.write(str(builder.generate_list()))
#             f.write('\n')
#     calculator.write_to_csv()
#     time.sleep(3600)
 
# Run the script every hour and add the results to csv file

# I have pairs, that have leverages, that have data (spread, profit, effective rate...) that have hourly data

for pair in sourcer.available_FTX:
    builder.generate_list(pair, 10000, lvrg)