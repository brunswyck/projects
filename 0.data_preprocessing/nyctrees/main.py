from dfops import DfOps as Dops
from pathlib import PurePath

file_location = PurePath("data", "data_100000.csv")
df_trees = Dops.import_data_from_csv(file_path=file_location, low_memory=False)

dop_trees = Dops(df_trees, 40, 1080)
print(dop_trees.df.shape)  # (100000, 42)
dop_trees.sort_index()

# parse the dates in "created_at" column
date_format = "%m/%d/%Y"  # eg 04/30/2015
dop_trees.parse_date_column("created_at", date_format)

# parse geometric POINT data
# dop_trees.print_columns_has_nan_check()

# df had 35190 nan values
# https://data.cityofnewyork.us/City-Government/State-Assembly-Districts/pf5b-73bw
# "MULTIPOLYGON (((-73.9128…17 40.65878291292874)))"

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

# change no, yes to false
dop_trees.change_x_y_to_false_true(no_yes_to_false_true, "No", "Yes")
# change NoDamage, Damage to false, true
dop_trees.change_x_y_to_false_true("sidewalk_dmg", "NoDamage", "Damage")

# convert following columns to boolean
"""
convert_bool_columns = ["branch_light", "branch_other", "branch_shoe",
                           "root_grate", "root_other", "root_stone",
                           "sidewalk_dmg",
                           "trnk_light", "trnk_other", "trnk_wire"
                           ]
"""
# have df convert dtypes it can
dop_trees.convert_dtypes()

boolean_columns = ["branch_light", "branch_other", "branch_shoe"]

dop_trees.drop_duplicate_rows()

# todo: recognize point data with geopandas

# strip leading trailing whitesapce
dop_trees.strip_leading_trailing_whitespace()

# deal with nans in these columns
cleanup_nans = ["guards", "health", "steward"]
dop_trees.apply_fillna_to_columns(cleanup_nans, "undefined")

# give meaning to "None" strings in these columns
dop_trees.replace_string_in_column("guards", "None", "NoGuard")
dop_trees.replace_string_in_column("steward", "None", "NoSteward")
dop_trees.replace_string_in_column("health", "None", "undefined")

# convert datatype to strings w max length of largest string in column
columns_to_string = ["name_latin", "name_latin", "name_common", "address"]
dop_trees.convert_columns_to_datatype_and_do_fillna(columns_to_string, "undefined", "str")

# after string cleaning has concluded turn following into categoricals
# guard, steward and health columns have been adjusted for their "None" replacement
categoricals = {
    "boroname": ['Queens', 'Brooklyn', 'Manhattan', 'Staten Island', 'Bronx'],
    "zip_city": ['Forest Hills', 'Whitestone', 'Brooklyn', 'New York', 'Staten Island', 'Astoria', 'Elmhurst',
                 'Kew Gardens', 'Ridgewood', 'Bronx', 'Fresh Meadows', 'East Elmhurst', 'Jackson Heights', 'Flushing',
                 'Rego Park', 'Far Rockaway', 'Corona', 'Springfield Gardens', 'Queens Village', 'Woodhaven',
                 'Rockaway Park', 'Long Island City', 'Saint Albans', 'Bayside', 'Oakland Gardens', 'Jamaica',
                 'College Point', 'Little Neck', 'Howard Beach', 'Arverne', 'Richmond Hill', 'Woodside', 'Bellerose',
                 'Ozone Park', 'Sunnyside', 'South Ozone Park', 'Cambria Heights', 'Rosedale', 'Glen Oaks',
                 'Central Park', 'Breezy Point', 'Middle Village', 'Hollis', 'New Hyde Park', 'Maspeth', 'Floral Park',
                 'South Richmond Hill'], "user_type": ['TreesCount Staff', 'Volunteer', 'NYC Parks Staff'],
    "curb_loc": ['OnCurb', 'OffsetFromCurb'], "guards": ['NoGuard', 'Helpful', 'Harmful', 'Unsure', "undefined"],
    "health": ['Fair', 'Good', 'Poor', "undefined"],
    "nbhood_code": ['QN17', 'QN49', 'BK90', 'BK37', 'MN14', 'MN15', 'SI14', 'BK26', 'QN72', 'SI54', 'BK69', 'BK81',
                    'BK29', 'BK42', 'QN25', 'BK68', 'MN40', 'MN12', 'SI25', 'QN60', 'BK46', 'MN27', 'QN20', 'BX17',
                    'SI36', 'SI45', 'BK17', 'MN50', 'MN24', 'SI24', 'BK44', 'QN62', 'SI01', 'BX06', 'BX41', 'SI48',
                    'QN28', 'MN20', 'MN23', 'BK33', 'MN09', 'BX43', 'BX36', 'BK19', 'BK31', 'BK43', 'QN51', 'BK96',
                    'QN22', 'QN15', 'BK77', 'QN12', 'BX40', 'QN03', 'QN18', 'QN34', 'BK64', 'BK28', 'BK95', 'BX62',
                    'QN27', 'MN31', 'QN70', 'MN21', 'QN53', 'QN10', 'BK41', 'QN41', 'QN48', 'BK76', 'SI05', 'BX28',
                    'BK58', 'BK25', 'MN17', 'QN19', 'MN25', 'MN11', 'QN31', 'BK88', 'QN08', 'QN66', 'QN46', 'QN42',
                    'QN06', 'QN23', 'BX01', 'MN19', 'BX26', 'QN45', 'BK61', 'BK73', 'BX49', 'QN71', 'QN57', 'BK82',
                    'BK78', 'BK79', 'BK60', 'MN28', 'MN13', 'BK34', 'BK75', 'BX08', 'QN54', 'SI07', 'BX52', 'BK45',
                    'MN32', 'BK32', 'BX03', 'QN50', 'BK35', 'BX30', 'BK40', 'BX37', 'BX34', 'QN43', 'BK85', 'BK27',
                    'BK21', 'SI32', 'MN22', 'BK83', 'BK50', 'MN36', 'SI11', 'QN37', 'BX10', 'BK72', 'MN33', 'QN63',
                    'SI35', 'BX75', 'BK30', 'QN29', 'SI12', 'QN44', 'BK63', 'MN04', 'QN55', 'MN06', 'QN47', 'BX33',
                    'QN33', 'SI37', 'BK91', 'BK23', 'BX39', 'BX09', 'BK38', 'BX63', 'BX05', 'QN05', 'BX29', 'QN56',
                    'MN01', 'BX27', 'SI22', 'MN34', 'QN35', 'QN68', 'BX44', 'MN35', 'QN52', 'QN38', 'BX14', 'BX22',
                    'BK09', 'SI28', 'SI08', 'QN26', 'BX35', 'BX55', 'BX31', 'QN61', 'BX46', 'MN03', 'BX13', 'QN21',
                    'QN07', 'QN76', 'QN30', 'QN01', 'BX59', 'QN02', 'BK93', 'BX07'],
    "nbhood_name": ['Forest Hills', 'Whitestone', 'East Williamsburg', 'Park Slope-Gowanus', 'Lincoln Square',
                    'Clinton', 'Grasmere-Arrochar-Ft. Wadsworth', 'Gravesend', 'Steinway', 'Great Kills',
                    'Clinton Hill', 'Brownsville', 'Bensonhurst East', 'Flatbush', 'Corona', 'Fort Greene',
                    'Upper East Side-Carnegie Hill', 'Upper West Side', 'Oakwood-Oakwood Beach', 'Kew Gardens',
                    'Ocean Parkway South', 'Chinatown', 'Ridgewood', 'East Tremont',
                    'Old Town-Dongan Hills-South Beach', 'New Dorp-Midland Beach',
                    'Sheepshead Bay-Gerritsen Beach-Manhattan Beach', 'Stuyvesant Town-Cooper Village',
                    'SoHo-TriBeCa-Civic Center-Little Italy', 'Todt Hill-Emerson Hill-Heartland Village-Lighthous',
                    'Madison', 'Queensboro Hill', "Annadale-Huguenot-Prince's Bay-Eltingville", 'Belmont', 'Mount Hope',
                    'Arden Heights', 'Jackson Heights', 'Murray Hill-Kips Bay', 'West Village',
                    'Carroll Gardens-Columbia Street-Red Hook', 'Morningside Heights', 'Norwood',
                    'University Heights-Morris Heights', 'Brighton Beach', 'Bay Ridge', 'Midwood', 'Murray Hill',
                    'Rugby-Remsen Village', 'Flushing',
                    'Far Rockaway-Bayswater', 'Bushwick North', 'Hammels-Arverne-Edgemere', 'Fordham South',
                    'Springfield Gardens South-Brookville', 'Rego Park', 'Queens Village', 'Prospect Heights',
                    'Bensonhurst West', 'Erasmus', 'Woodlawn-Wakefield', 'East Elmhurst', 'Lenox Hill-Roosevelt Island',
                    'Astoria', 'Gramercy', 'Woodhaven', 'Breezy Point-Belle Harbor-Rockaway Park-Broad Chan',
                    'Kensington-Ocean Parkway', 'Fresh Meadows-Utopia', 'Auburndale', 'Greenpoint',
                    'New Springville-Bloomfield-Travis', 'Van Cortlandt Village', 'Flatlands', 'Homecrest',
                    'Midtown-Midtown South', 'Glendale', 'Battery Park City-Lower Manhattan', 'Central Harlem South',
                    'Hunters Point-Sunnyside-West Maspeth', 'Borough Park', 'St. Albans', 'Laurelton',
                    'Bayside-Bayside Hills', 'Oakland Gardens', 'Jamaica Estates-Holliswood', 'College Point',
                    'Claremont-Bathgate', 'Turtle Bay-East Midtown', 'Highbridge',
                    'Douglas Manor-Douglaston-Little Neck', 'Crown Heights North', 'North Side-South Side',
                    'Pelham Parkway', 'Old Astoria', 'Lindenwood-Howard Beach', 'East New York', 'Bushwick South',
                    'Ocean Hill',
                    'Prospect Lefferts Gardens-Wingate', 'Lower East Side',
                    'Hudson Yards-Chelsea-Flatiron-Union Square', 'Sunset Park East', 'Bedford',
                    'West Farms-Bronx River', 'Richmond Hill', 'Westerleigh',
                    'Schuylerville-Throgs Neck-Edgewater Park', 'Georgetown-Marine Park-Bergen Beach-Mill Basin',
                    'Yorkville', 'Sunset Park West', 'Eastchester-Edenwald-Baychester', 'Elmhurst-Maspeth',
                    'Stuyvesant Heights', 'Kingsbridge Heights', 'Windsor Terrace',
                    'Van Nest-Morris Park-Westchester Square', 'Melrose South-Mott Haven North', 'Bellerose',
                    'East New York (Pennsylvania Ave)', 'Bath Beach', 'Seagate-Coney Island', 'Rossville-Woodrow',
                    'East Village', 'Cypress Hills-City Line', 'Canarsie', 'Washington Heights South',
                    'Charleston-Richmond Valley-Tottenville', 'Kew Gardens Hills',
                    'Pelham Bay-Country Club-City Island', 'Williamsburg', 'East Harlem South', 'Woodside',
                    'New Brighton-Silver Lake', 'Crotona Park East', 'Dyker Heights', 'Elmhurst',
                    "Mariner's Harbor-Arlington-Port Ivory-Graniteville", 'Glen Oaks-Floral Park-New Hyde Park',
                    'Crown Heights South', 'Hamilton Heights',
                    'South Ozone Park', 'Manhattanville', 'Ft. Totten-Bay Terrace-Clearview', 'Longwood',
                    'Cambria Heights', 'Stapleton-Rosebank', 'East Flatbush-Farragut', 'West Brighton',
                    'Mott Haven-Port Morris', 'Soundview-Castle Hill-Clason Point-Harding Park',
                    'DUMBO-Vinegar Hill-Downtown Brooklyn-Boerum Hill', 'West Concourse', 'Bedford Park-Fordham North',
                    'Rosedale', 'Spuyten Duyvil-Kingsbridge', 'Ozone Park', 'Marble Hill-Inwood', 'Hunts Point',
                    'West New Brighton-New Brighton-St. George', 'East Harlem North', 'Briarwood-Jamaica Hills',
                    'Queensbridge-Ravenswood-Long Island City', 'Williamsbridge-Olinville', 'Washington Heights North',
                    'East Flushing', 'Pomonok-Flushing Heights-Hillcrest', 'East Concourse-Concourse Village',
                    'North Riverdale-Fieldston-Riverdale', 'Brooklyn Heights-Cobble Hill', 'Port Richmond',
                    'Grymes Hill-Clifton-Fox Hills', 'North Corona', 'Morrisania-Melrose', 'Soundview-Bruckner',
                    'Allerton-Pelham Gardens', 'Jamaica', 'Parkchester', 'Central Harlem North-Polo Grounds',
                    'Co-op City', 'Middle Village', 'Hollis', 'Baisley Park', 'Maspeth',
                    'South Jamaica', 'Westchester-Unionport', 'Springfield Gardens North', 'Starrett City',
                    'Bronxdale'],
    "status": ['Alive', 'Dead', 'Stump'],
    "steward": ['NoSteward', '1or2', '3or4', '4orMore', 'undefined']
}

dop_trees.create_categories_from_dict(categoricals)

# UNCOMMENT TO VIEW ALL DATA
# dop_trees.get_overview_nan_count_and_unique_values(just_print=True)

print(dop_trees.get_nan_count_dataframe())
dop_trees.print_datatypes()

# nan values per column
dop_trees.get_overview_nan_count(just_print=True)

# dop_trees.get_overview_unique_count(just_print=True)
