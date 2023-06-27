import pandas as pd
from functools import reduce


class Utils:
    @staticmethod
    def merge_dataframes(dataframes, on_columns):
        if len(dataframes) < 2:
            raise ValueError("At least two DataFrames are required for merging.")

        return reduce(
            lambda left, right: pd.merge(left, right, on=on_columns, how="inner"),
            dataframes,
        )
