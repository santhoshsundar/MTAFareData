import re
import csv
import os
import os.path
import argparse
import platform
from mta_scrapper import *
from datetime import datetime
from requests import get
from bs4 import BeautifulSoup

"""
Get the fare link and dump data into csv
"""


def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        return datetime.strptime(arg_date_str, "%Y-%m-%d")
    except ValueError:
        msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(arg_date_str)
        raise argparse.ArgumentTypeError(msg)


def scrape(link, write):
    response = get(link)
    soup = BeautifulSoup(response.content, 'lxml')
    data = soup.find('body')

    dates = re.search(r'(0[1-9]|1[012])[- /.]((0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d)-(0[1-9]|1[012])[- /.]((0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d)', data.text)

    date = dates.group().split('-')

    fare_lists = data.text.split('\n')

    from_date = date[0]
    to_date = date[1]

    for index, i in enumerate(fare_lists):
        if index >= 3:
            fare_list = i.split(",")
            if(len(fare_list) > 1):
                for index1, i in enumerate(fare_list):
                    if index1 >= 2 and index1 <= len(fare_list)-2:
                        if fare_list[index1] == '00000000':
                            fare_list[index1] = 0
                        else:
                            fare_list[index1] = int(fare_list[index1].lstrip('0'))
                write.writerow([from_date, to_date, fare_list[0], fare_list[1], fare_list[2], fare_list[3], fare_list[4], fare_list[5], fare_list[6], fare_list[7], fare_list[8], fare_list[9], fare_list[10], fare_list[11], fare_list[12], fare_list[13], fare_list[14], fare_list[15], fare_list[16], fare_list[17], fare_list[18], fare_list[19], fare_list[20], fare_list[21], fare_list[22], fare_list[23]])


def fare_links(start, end):
    Header = ['From_Date', 'To_date', 'Remote_Station_ID', 'Station', 'Full_Fare', 'Senior_Citizen/Disabled', '7_Day_ADA_Farecard_Access_System_Unlimited', '30_Day_ADA_Farecard_Access_System_Unlimited', 'Joint_Rail_Road_Ticket', '7_Day_Unlimited', '30_Day_Unlimited', '14_Day_Reduced_Fare_Media_Unlimited', '1_Day_Unlimited', '14_Unlimited', '7_Day_Express_Bus_Pass', 'Transit_Check_Metrocard', 'LIB_Special_Senior', 'Rail_Road_Unlimited_No_Trade', 'Rail_Road_Unlimited_No_Trade', 'Mail_and_Ride_EZPass_Express', 'Mail_and_Ride_Unlimited', 'Path_2_Trip', 'Airtran_Full_Fare', 'Airtran_30_Day', 'Airtran_10_Trip', 'Airtran_Monthly']


    filename = "mta_fare_data.csv"

    if os.path.isfile(filename):
        with open(filename, mode='a+', encoding='utf-8') as f:
            write = csv.writer(f)
            print("path exist")

            links = get_fare_date(start, end)

            for link in links:
                print(link)
                scrape(link, write)
    else:
        with open(filename, mode='w', encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerow(Header)
            print("not path exist")

            links = get_fare_date(start, end)

            for link in links:
                print(link)
                scrape(link, write)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Type Dates to scrape data')
    parser.add_argument('start_date', type=valid_date_type, help='Type date in YYYY-MM-DD')
    parser.add_argument('end_date', type=valid_date_type, help='Type date in YYYY-MM-DD')
    args = parser.parse_args()

    # start_date = datetime(2016, 10, 1)
    # end_date = datetime(2016, 10, 22)

    fare_links(args.start_date, args.end_date)
