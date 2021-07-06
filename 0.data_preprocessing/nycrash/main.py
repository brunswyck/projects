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
print(crash.df.head(10))
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
find = r'\r+|\n+|\t+|�'
replacement = ''
crash.replace_via_regex_in_df(find, replacement)

# remove leading comma + whitespace
find = r'^,\s+'
crash.replace_via_regex_in_df(find, replacement)

# deal with (0.0, 0.0)
find = r'\(0.0, 0.0\)'
crash.replace_via_regex_in_df(find, "undefined")

# can accidents happen on the same location? -> yes

# drop rows if location_cols are all nan
# my model will have no use for streetnames and numbers when there are no coordinates
location_cols = ["latitude", "longitude", "location"]

# drop rows if there are no coordinates to suck up
crash.drop_rows_when_these_columns_are_nan(location_cols)
# won't be using street data, just coordinates
crash.drop_columns(["on_street_name", "off_street_name", "cross_street_name"])

lat_no_zero = (crash.df.latitude != 0)
long_no_zero = (crash.df.longitude != 0)
location_no_zero_zero = (crash.df.location != (0.0))
location_no_undefined = (crash.df.location != "undefined")
# print(crash.df[lat_no_zero & long_no_zero & location_no_zero_zero & location_no_undefined])

# print(crash.df.loc[0:200, location_cols]) # drop

## one hot encoding with get_dummies
# to get actual dummy encoding instead of OHE you need drop_first=True
# todo: decide on columns to OHE
# todo: unique em
categorical_to_ohe = ['contributing_factor_vehicle_1', 'contributing_factor_vehicle_2', 'contributing_factor_vehicle_3',
                      'contributing_factor_vehicle_4', 'contributing_factor_vehicle_5']
"""
for cat in categorical_to_ohe:
    print(crash.get_unique_values_of_column(cat))
# unique data in contributing factor columns
['Unspecified', 'Passing or Lane Usage Improper', 'Following Too Closely', 'Driver Inexperience',
 'Failure to Yield Right-of-Way', 'Driver Inattention/Distraction', 'Brakes Defective', 'Passing Too Closely',
 'Turning Improperly', 'Unsafe Speed', 'Backing Unsafely', 'View Obstructed/Limited', 'Steering Failure',
 'Traffic Control Disregarded', 'Drugs (illegal)', 'Other Vehicular', 'Reaction to Uninvolved Vehicle',
 'Aggressive Driving/Road Rage', 'Fell Asleep', 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion',
 'Alcohol Involvement', 'Unsafe Lane Changing', 'Pavement Slippery', 'Pavement Defective', 'Other Lighting Defects',
 'Oversized Vehicle', 'Animals Action', 'Outside Car Distraction', 'Illnes', 'Driverless/Runaway Vehicle',
 'Passenger Distraction', 'Tire Failure/Inadequate', 'nan', 'Lost Consciousness', 'Accelerator Defective',
 'Obstruction/Debris', 'Glare', 'Eating or Drinking', 'Cell Phone (hands-free)', 'Lane Marking Improper/Inadequate',
 'Failure to Keep Right', 'Using On Board Navigation Device', 'Fatigued/Drowsy', 'Tow Hitch Defective',
 'Physical Disability', 'Cell Phone (hand-Held)',
 'Headlights Defective', 'Tinted Windows', 'Vehicle Vandalism', 'Other Electronic Device', 'Prescription Medication',
 'Listening/Using Headphones', 'Traffic Control Device Improper/Non-Working', 'Texting', 'Shoulders Defective/Improper',
 'Windshield Inadequate']
['nan', 'Unspecified', 'Unsafe Speed', 'Driver Inattention/Distraction', 'Driver Inexperience',
 'Failure to Yield Right-of-Way', 'Following Too Closely', 'Turning Improperly', 'Passing or Lane Usage Improper',
 'Other Vehicular', 'View Obstructed/Limited', 'Oversized Vehicle', 'Passing Too Closely', 'Unsafe Lane Changing',
 'Traffic Control Disregarded', 'Reaction to Uninvolved Vehicle', 'Fell Asleep', 'Aggressive Driving/Road Rage',
 'Backing Unsafely', 'Alcohol Involvement', 'Outside Car Distraction',
 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion', 'Obstruction/Debris', 'Glare', 'Vehicle Vandalism',
 'Pavement Slippery', 'Passenger Distraction', 'Steering Failure', 'Driverless/Runaway Vehicle', 'Drugs (illegal)',
 'Failure to Keep Right', 'Fatigued/Drowsy', 'Headlights Defective', 'Lane Marking Improper/Inadequate',
 'Tire Failure/Inadequate', 'Traffic Control Device Improper/Non-Working', 'Other Lighting Defects', 'Brakes Defective',
 'Cell Phone (hands-free)', 'Pavement Defective', 'Tinted Windows', 'Cell Phone (hand-Held)', 'Accelerator Defective',
 'Listening/Using Headphones', 'Illnes',
 'Using On Board Navigation Device' 'Animals Action']
['nan', 'Unspecified', 'Passing or Lane Usage Improper', 'Following Too Closely', 'Other Vehicular',
 'Unsafe Lane Changing', 'View Obstructed/Limited', 'Outside Car Distraction',
 'Driver Inattention/Distraction' 'Failure to Yield Right-of-Way' 'Oversized Vehicle' 'Pavement Slippery' 'Driver Inexperience' 'Unsafe Speed' 'Obstruction/Debris' 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion' 'Reaction to Uninvolved Vehicle' 'Alcohol Involvement' 'Passing Too Closely' 'Traffic Control Device Improper/Non-Working' 'Pavement Defective' 'Tire Failure/Inadequate' 'Backing Unsafely' 'Fell Asleep' 'Traffic Control Disregarded' 'Turning Improperly' 'Aggressive Driving/Road Rage' 'Failure to Keep Right' 'Cell Phone (hands-free)' 'Driverless/Runaway Vehicle']
['nan',
 'Unspecified' 'Reaction to Uninvolved Vehicle' 'Other Vehicular' 'Following Too Closely' 'Driver Inattention/Distraction' 'Alcohol Involvement' 'Outside Car Distraction' 'Driver Inexperience' 'Pavement Slippery' 'Passing or Lane Usage Improper' 'Obstruction/Debris' 'Passing Too Closely' 'Unsafe Speed' 'Backing Unsafely']
['nan', 'Unspecified', 'Following Too Closely', 'Driver Inattention/Distraction', 'Other Vehicular',
 'Passing Too Closely', 'Outside Car Distraction', 'Driver Inexperience', 'Pavement Slippery', 'Obstruction/Debris',
 'Unsafe Speed']
# fix typo Illnes -> illness
"""
fix_typo_column = 'contributing_factor_vehicle_2'
crash.replace_string_in_column(fix_typo_column, 'Illnes', 'Illness')
# pd.get_dummies(df.Sex, prefix='Sex')
columns_to_dumb = ['contributing_factor_vehicle_5']
crash.dummify_columns(columns_to_dumb, "5")


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
print(crash.df.head(100))
print("anchor for debugging")
