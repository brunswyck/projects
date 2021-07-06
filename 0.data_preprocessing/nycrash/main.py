import numpy as np

from dfops import DfOps as Dops
from pathlib import PurePath

# https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

file_location = PurePath("data", "data_100000.csv")
df_crash = Dops.import_data_from_csv(fp=file_location, low_memory=False, nrows=2500)

crash = Dops(df_crash, 40, 1080)
print(crash.df.shape)  # (100000, 29)
crash.sort_index()
# drop rows if nan treshold is met
# df.dropna(thresh=2)
"""
must have:
- dataset contains no missing values ("" or null)
- no duplicates
- values are consolidated (eg Truck = truck)
- data format is correct
- no blank spaces (ex: " I love python " => "I love python")
"""

# one hot encoding + flattening = combining columns into one
# flatten highly correlated columns to a lower dimension

# print(dop_crash.df.head(20))
# crash_date               crash_time
# 2021-04-14T00:00:00.000  5:32

# parse the date in "crash_date"
# empty date = NaT
date_format = '%Y-%m-%dT%H:%M:%S.%f'
date_sample = "2021-04-14T00:00:00.000"
# tested with dop_crash.convert_string_to_date(date_sample, date_format)
crash.parse_date_column("crash_date", date_format)
# dop_crash.print_datatypes()

# target variable = location
# format location = (latitude, longitude)

# deal with '\n,  \n(40.69754, -73.98312)' newline chars
find = r'\r+|\n+|\t+'
replacement = ''
crash.replace_via_regex_in_df(find, replacement)

# remove leading comma + whitespace
find = r'^,\s+'
crash.replace_via_regex_in_df(find, replacement)

# deal with (0.0, 0.0)
find = r'\(0.0, 0.0\)'
crash.replace_via_regex_in_df(find, "undefined")

# can accidents happen on the same location? -> yes

zeroCoord = crash.df.apply(lambda x: True if x['location'] == 'NaN' else False , axis=1)
print(crash.df[zeroCoord])
# print(dop_crash.df.loc[dop_crash.df['latitude'],["latitude","longitude","location"]]) # row, column

# nZeroCoord = len(zeroCoord[zeroCoord == True].index)


# dop_crash.get_overview_nan_count_and_unique_values(just_print=True)
# fill latitude & longitude if present in location
# deal with NaN
# deal with "(0.0, 0.0)"
# check date format
# ints that should be floats & vice versa
"""
Nice-to-have features:
- more data = better, pay attention that the more data you have, the longer each operation needs to execute.
- add new features computed using the features present that you think are going to be useful
- apply the preprocessing steps needed so that a future machine learning model can make the best use out of it
- (feature selection, feature engineering, feature normalization, and resampling)
"""
print("anchor for debugging")