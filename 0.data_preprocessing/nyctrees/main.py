from dfops import DfOps as Dops
from pathlib import PurePath

file_location = PurePath("data", "data_100000.csv")
df_trees = Dops.import_data_from_csv(file_location, low_memory=False, parse_dates=True)

dop_trees = Dops(df_trees, 40, 1080)
dop_trees.sort_index()

# parse the dates in "created_at" column
date_format = "%m/%d/%Y"  # eg 04/30/2015
dop_trees.parse_date_column("created_at", format=date_format)

# parse geometric POINT data
dop_trees.print_datatypes()
dop_trees.print_columns_has_nan_check()

# unfortunately not all values in zip_city column are in nta_name column
# unfortunately not all values in cncldist column are in st_assem column
# print(dop_trees.check_values_column_x_are_in_column_y("cncldist", "st_assem"))

# print(dop_trees.get_nan_count_column("spc_common"))
# print(dop_trees.get_nan_count_dataframe())

# nan values per column
# dop_trees.get_overview_nan_count(just_print=True)
# dop_trees.get_overview_unique_count(just_print=True)


# print(dop_trees.get_nan_count_row(10))
# print(df_trees.head(20))
# print(df_trees.iloc[5])

"""
you can keep categorical strings
check their uniqueness
remove capitalization
throw away useless data

# df has 35190 nan values


created_at = Date trees were mapped
the_geom = POINT (Longitude, latitude) -> checked out geopandas to work with this data
curb_loc = ['OnCurb' 'OffsetFromCurb']
status = ['Alive' 'Dead' 'Stump']
health = ['Fair' 'Good' 'Poor' nan]
spc_latin = 126 unique values, 5027 nan's
spc_common = 0 NaN "red maple"
steward = 5027 NaN's, ['None', '1or2', '3or4', nan, '4orMore'], dtype=object
guards = 5027 NaN's ['None', 'Helpful', 'Harmful', 'Unsure', nan], dtype=object
sidewalk = 5027 NaN's ['NoDamage', 'Damage', nan], dtype=object


"""
# https://data.cityofnewyork.us/City-Government/State-Assembly-Districts/pf5b-73bw
# "MULTIPOLYGON (((-73.9128…17 40.65878291292874)))"

# keep zip code, geo points, latitude & longitude drop other geobased column
# everything is "state" = 'New York' so just drop it
drop_columns = ["problems", "borocode", "state"]
rename_columns = {
    "brnch_ligh": "branch_light",
    "brnch_othe": "branch_other",
    "brnch_shoe": "branch_shoe",
    "cncldist": "council_dist",
    "nta": "nbhood_code",
    "nta_name": "nbhood_name",
    "spc_common": "name_common",
    "spc_latin": "name_latin",
    "the_geom": "geo_points",
    "tree_dbh": "tree_diam",
    "x_sp": "x_coord",
    "y_sp": "y_coord",
    "st_assem": "st8_assembly",
    "st_senate": "st8_senate",
    "sidewalk": "sidewalk_dmg"
}
dop_trees.rename_columns_dict(rename_columns)
dop_trees.drop_columns(columns=drop_columns)
no_yes_to_false_true = ["branch_light", "branch_other", "branch_shoe",
                        "root_grate", "root_other", "root_stone",
                        "trnk_light", "trnk_other", "trnk_wire"
                        ]
# renamed sidewalk to sidewalk_dmg
nodmg_dmg_to_false_true = ["sidewalk_dmg"]
dop_trees.change_x_y_to_false_true(no_yes_to_false_true, "No", "Yes")
dop_trees.change_x_y_to_false_true(nodmg_dmg_to_false_true, "NoDamage", "Damage")



# convert following columns to boolean
convert_bool_columns = ["branch_light", "branch_other", "branch_shoe",
                           "root_grate", "root_other", "root_stone",
                           "sidewalk_dmg",
                           "trnk_light", "trnk_other", "trnk_wire"
                           ]
# convert np.array columns to list column
dop_trees.convert_column_with_arrays_to_lists(convert_bool_columns)

dop_trees.convert_cols_to_datatype(convert_bool_columns, "bool")
dop_trees.get_overview_nan_count_and_unique_values(just_print=True)

boolean_columns = ["branch_light", "branch_other", "branch_shoe", ""]

categoricals = {
    "boroname": ['Queens', 'Brooklyn', 'Manhattan', 'Staten Island', 'Bronx'],
    "": []
}

# arr.tolist
