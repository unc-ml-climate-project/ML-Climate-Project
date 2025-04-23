"""Data cleaning module."""

import pandas as pd


class DataCleaner:
    def __init__(self, file_path):
        """
        Initializes the DataCleaner with the file path.
        :param file_path: Path to the CSV file.
        """
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)

    def remove_text(self, column, text, regex=False):
        """
        Removes unwanted text from a specified column.
        :param column: The column name to clean.
        :param text: The text to remove from the column.
        :param regex: Check if text is a regex pattern (bool)
        """
        if self.df[column].dtypes != "object":
            raise Exception("Cannot remove text on a non-string column")
        self.df[column] = self.df[column].str.replace(text, "", regex=regex)

    def strip_spaces(self, column):
        """
        Strips leading and trailing spaces from a specified column.
        :param column: The column name to strip spaces from.
        """
        if self.df[column].dtypes != "object":
            raise TypeError("Cannot strip spaces on a non-string column")
        self.df[column] = self.df[column].str.strip()

    def handle_missing(self, column, strategy="mean"):
        """
        Handles missing values in a specified column.
        :param column: The column name with missing values.
        :param strategy: The strategy to handle missing values ('mean', 'zero',
        etc.).
        """
        if strategy == "mean":
            mean_value = self.df[column].mean()
            self.df[column] = self.df[column].fillna(mean_value)
        elif strategy == "zero":
            self.df[column] = self.df[column].fillna(0)
        elif strategy == "drop":
            self.df = self.df.dropna(subset=[column])

    def drop(self, columns):
        """
        Drops unwanted columns from the dataset.
        :param columns: List of column names to drop.
        """
        self.df = self.df.drop(columns=columns)

    def save_data(self, output_path):
        """
        Saves the cleaned data to a new CSV file.
        :param output_path: Path where the cleaned data should be saved.
        """
        try:
            self.df.to_csv(output_path, index=False)
            print(f"Data successfully saved to {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def preview(self, n=5):
        """
        Previews the first few rows of the cleaned data.
        :param n: Number of rows to print.
        """
        return self.df.head(n)

    def to_float(self, column):
        """
        Convert specfied column to float data type.
        :param column: Name of column.
        """
        self.df[column] = self.df[column].astype(float)

    def round(self, column, decimals):
        """
        Round specfied column to specified decimal amount.
        :param column: Name of column.
        :param decimals: Number of decimals to round by.
        """
        self.df[column] = self.df[column].round(decimals)

    def new_column(self, column, items):
        """
        Add new column in dataframe.
        :param column: Name of column.
        :param items: List of items to be added to column.
        """
        self.df[column] = items

    def sort_column(self, column, ascending=True):
        """
        Sorts the dataframe based on the column in ascending or descending
        order.
        :param column: Name of the column to sort by.
        :param ascending: Boolean indicating whether or not to sort by
        ascending order.
        """
        self.df = self.df.sort_values(by=column, ascending=ascending)
        self.df = self.df.reset_index(drop=True)

    def count_missing_values(self):
        return self.df.isnull().sum()

    def aggregate_data(self, columns, aggregate_method='mean'):
        """
        Groups the dataframe by the specified columns and performs the
        specified aggregation method.
        :param columns: List of columns to be grouped.
        :param aggregate_method: Aggregation method to apply.
        """
        df_grouped = self.df.groupby(columns)

        if aggregate_method.lower() == 'mean':
            self.df = df_grouped.mean()
            self.df = self.df.reset_index(drop=False)

        elif aggregate_method.lower() == 'min':
            self.df = df_grouped.min()
            self.df = self.df.reset_index(drop=False)

        elif aggregate_method.lower() == 'max':
            self.df = df_grouped.max()
            self.df = self.df.reset_index(drop=False)

        elif aggregate_method.lower() == 'sum':
            self.df = df_grouped.sum()
            self.df = self.df.reset_index(drop=False)

        elif aggregate_method.lower() == 'count':
            self.df = df_grouped.count()
            self.df = self.df.reset_index(drop=False)

        elif aggregate_method.lower() == 'median':
            self.df = df_grouped.median()
            self.df = self.df.reset_index(drop=False)

        else:
            self.df = df_grouped.mean()
            self.df = self.df.reset_index(drop=False)

    def filter_by_column(self, column, value):
        """
        Filters the data frame by a specific column and value.
        :param column: The column to be filtered.
        :param value: The value to be filtered by.
        """
        self.df = self.df[self.df[column] == value]
