import pandas as pd
import numpy as np
from pprint import pprint as pp
# conda install -c conda-forge geopandas
import geopandas as gpd
from pathlib import PurePath
# conda install multipledispatch
# from multipledispatch import dispatch
from shapely.geometry import Point

class DfOps:

    def __init__(self, dataframe, max_cols, cons_width=640):
        self.df = dataframe
        self.df.sort_index()
        self.initiate_pandas(max_cols, cons_width)
        self.initiate_numpy(cons_width)

    @staticmethod
    def initiate_pandas(max_cols, cons_width):
        pd.set_option('display.max_columns', max_cols)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', cons_width)  # make output in console wider

    @staticmethod
    def initiate_numpy(console_width=640):
        # https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
        np.set_printoptions(linewidth=console_width)

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    @staticmethod
    def import_data_from_csv(file_path: PurePath, sep: str = ",", low_memory: bool = True, verbose: bool = True, parse_dates: bool = False):
        df = pd.read_csv(file_path, sep=sep, low_memory=low_memory, verbose=verbose)
        if isinstance(df, pd.DataFrame):
            return df
        else:
            raise Exception(f"No dataframe was created when trying pd.read_csv({file_path})")

    def rename_columns_dict(self, new_names: dict):
        self.df.rename(columns=new_names, inplace=True)

    def replace_value_in_column(self, column, old_value, new_value):
        self.df[column] = self.df[column].replace(to_replace=old_value, value=new_value)

    def change_zero_ones_to_true_false(self, columns_list: list):
        for column in columns_list:
            self.replace_value_in_column(column, 0, False)
            self.replace_value_in_column(column, 1, True)

    def change_x_y_to_false_true(self, columns_list, x: str = "no", y: str = "yes"):
        for column in columns_list:
            self.replace_nan_in_column(column, x)
            self.replace_value_in_column(column, x, False)
            self.replace_value_in_column(column, y, True)


    def count_nans_in_column(self, column: str) -> int:
        return self.df[column].isna().sum()

    # convert to datatype only
    def convert_cols_to_datatype(self, columns, set_datatype_to: str):
        for col in columns:
            self.df[col] = self.df[col].astype(set_datatype_to)

    # fillna and convert to datatype
    def convert_cols_to_datatype_and_do_fillna(self, columns, fill_na_value, set_datatype_to=None):
        # do fillna AND convert to datatype
        if fill_na_value and set_datatype_to:
            for index, column in enumerate(columns):
                self.df[column] = self.df[column].fillna(fill_na_value).astype(set_datatype_to)

    # do fillna only
    def apply_fillna_to_column(self, column, replace_nan_value):
        self.df[column] = self.df[column].fillna(replace_nan_value)

    def replace_nan_in_column(self, columns, replace_nan_value):
        if not isinstance(columns, list):
            list(columns)
        self.apply_fillna_to_column(columns, replace_nan_value)

    # https://hashtaggeeks.com/posts/pandas-categorical-data.html
    @staticmethod
    def create_category(category_list):
        try:
            return pd.CategoricalDtype(categories=category_list)
        except Exception as err:
            print(f"something went wrong when creating categorical: {err}")

    def apply_mean_to_column(self, column):
        self.apply_fillna_to_column(column, self.df[column].mean())

    def write_to_csv(self, file_path):
        self.df.to_csv(file_path)

    def count_nans_in_df(self):
        return self.df.isna().sum()

    def print_datatypes(self):
        print("------------checking column datatypes------------>")
        print(self.df.dtypes)
        print("----------checking column datatypes END---------->")

    def print_columns_has_nan_check(self):
        print("----- columns with missing values = True -------->")
        print(self.df.isnull().any())
        print("----------- missing values check END ------------>")

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_index.html
    def sort_index(self, ascending: bool = True):
        self.df.sort_index

    # https://stackoverflow.com/questions/23797491/parse-dates-in-pandas
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
    def parse_date_column(self, column: str, format='%d/%m/%Y'):
        self.df[column] = pd.to_datetime(self.df[column], format=format)

    def get_unique_values_of_column(self, column) -> np.ndarray:
        if isinstance(self.df[column], pd.Series):
            return pd.unique(self.df[column])

    def get_index_start_stop_step(self):
        print(self.df.index)  # <class 'pandas.core.indexes.range.RangeIndex'>

    def get_column_index(self, column: str) -> int:
        return self.df.columns.get_loc(column)

    def get_nan_count_column(self, column: str) -> int:
        return self.df[column].isna().sum()

    def get_nan_count_dataframe(self) -> int:
        return self.df.isna().sum().sum()

    def get_nan_count_row(self, row_index: int, row_name: str = None) -> int:
        if row_name:
            return self.df[row_name].isna().sum().sum()
        elif row_index:
            return self.df.loc[row_index].isna().sum().sum()

    def get_overview_nan_count(self, just_print=False):
        column_with_nan_count_dictionary = dict()
        for column in self.df:
            column_with_nan_count_dictionary[column] = self.get_nan_count_column(column)
        if just_print:
            pp(column_with_nan_count_dictionary)
        else:
            return column_with_nan_count_dictionary

    def get_overview_unique_count(self, just_print=False):
        column_with_unique_count_dictionary = dict()
        for column in self.df:
            column_with_unique_count_dictionary[column] = self.get_unique_values_of_column(column)
        if just_print:
            pp(column_with_unique_count_dictionary)
        else:
            return column_with_unique_count_dictionary

    def get_overview_nan_count_and_unique_values(self, just_print=False):
        overview_dict = dict()
        for column in self.df:
            overview_dict[column] = (self.get_nan_count_column(column), self.get_unique_values_of_column(column))
        if just_print:
            pp(overview_dict)
        else:
            return overview_dict

    def check_values_column_x_are_in_column_y(self, column_x: str, column_y: str) -> bool:
        # for every row in column x
        unique_vals_col_x = self.get_unique_values_of_column(column_x)
        unique_vals_col_y = self.get_unique_values_of_column(column_y)
        return set(unique_vals_col_x).issubset(unique_vals_col_y)

    def drop_columns(self, columns: [str]):
        self.df = self.df.drop(columns=columns)

    def convert_column_with_arrays_to_lists(self, list_of_columns: list):
        for column in list_of_columns:
            self.df[column].values.tolist()

    # just a test
    def parse_point_data(self, row):
        geoblocks = row.split()  # split Point (Long, Lat) up into Point () + Longitude + Latitude
        long = float(geoblocks[1].lstrip('('))  # longitude
        lat = float(geoblocks[2].rstrip(')'))   # latitude
        point = Point(long, lat)
        return point

# import matplotlib.pyplot as plt
# import seaborn as sns
# import pathlib
#
#
# class ChartMaker:
#     default_path = pathlib.PurePath("files", "charts")
#
#     def __init__(self, data, title, cm="Blues_d", palette="Blues_d", style="whitegrid"):
#         self.data = data
#         self.chart_style = style
#         self.palette = palette
#         self.cm = sns.color_palette(cm)
#         self.title = title
#         self.plot = plt
#         self.figure = plt.figure()
#
#     def get_correlation_matrix(self):
#         if isinstance(self.data, pd.DataFrame):
#             return self.data.corr().abs()
#
#     def set_sns_theme_style(self):
#         sns.set_theme(style=self.chart_style)
#
#     # https://seaborn.pydata.org/generated/seaborn.heatmap.html?highlight=heatmap#seaborn.heatmap
#     def create_sns_heatmap(self, matrix):
#         sns.heatmap(matrix, cmap=self.cm)
#
#     # https://seaborn.pydata.org/generated/seaborn.barplot.html?highlight=barplot#seaborn.barplot
#     def create_sns_barplot(self, y_title: str):
#         sns.barplot(x=self.data.index, y=y_title, data=self.data, palette=self.palette)
#
#     def set_figure_title(self, title: str, fontsize=9):
#         self.figure.suptitle(title)
#
#     def set_plot_title(self, title: str):
#         self.plot.title(title)
#
#     def save_plot_figure(self, filename: str):
#         save_final = pathlib.PurePath(self.default_path, filename)
#         self.plot.savefig(save_final)
#
#     def set_plot_figure_fize(self, x: int, y: int):
#         self.figure.figsize(x, y)
#
#     def plot_show_figures(self):
#         self.plot.show()
#
#     def set_plot_ylim(self, y_range_start: int, y_range_stop: int):
#         # range allowed on y-axis
#         self.plot.ylim(y_range_start, y_range_stop)
#
#     def set_plot_ylabel(self, y_label: str):
#         self.plot.ylabel(y_label)
#
#     def set_yticks(self, start: int, stop: int, step: float):
#         self.plot.yticks(np.arange(start, stop, step=step))
