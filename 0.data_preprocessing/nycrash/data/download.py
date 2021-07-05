# make sure to install these packages before running:
# pip install pandas
# pip install sodapy


import argparse
import pandas as pd
from sodapy import Socrata
import csv

def download(numberOfSamples : int):
    client = Socrata("data.cityofnewyork.us", None,  )
    dataset_name = "h9gi-nx95" # Only thing that changes between Socrata datasets
    filename = "data_{}.csv".format(numberOfSamples)

    data = client.get(dataset_identifier=dataset_name, 
                    content_type="csv", 
                    limit=numberOfSamples)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download NYC Motor Vehicle Crashes.',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-N', 
                        '--nbrows',
                        type=int,
                        default=100000, 
                        required=False,
                        help='The number of rows you want to download')
    args = parser.parse_args()

    download(args.nbrows)