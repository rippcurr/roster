# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 13:29:16 2025

@author: david
"""

def remove_columns_with_nan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes columns from a pandas DataFrame that contain any NaN (Not a Number) values.

    Args:
        df (pd.DataFrame): The input pandas DataFrame.

    Returns:
        pd.DataFrame: A new DataFrame with columns containing NaN values removed.
                      Returns an empty DataFrame if all columns contain NaN.
    """
    # Identify columns that do NOT contain any NaN values
    # df.isnull() returns a boolean DataFrame of the same shape as df, indicating True for NaN.
    # .any() applied to df.isnull() along axis=0 (columns) returns a Series where True means
    # that column contains at least one NaN.
    # The '~' (tilde) negates this boolean Series, so True means "does NOT contain any NaN".
    columns_to_keep = df.columns[~df.isnull().any()]

    # Select only the columns that do not contain NaN values
    df_cleaned = df[columns_to_keep]

    return df_cleaned


def get_row_containing(df: pd.DataFrame, column_name: str, to_find: str) -> pd.DataFrame:
    """
    Returns rows in a pandas DataFrame where the specified column contains the word.

    Args:
        df (pd.DataFrame): The input pandas DataFrame.
        column_name (str): The name of the column to search within.

    Returns:
        pd.DataFrame: A DataFrame containing the rows where to_find occurs.
                      Returns an empty DataFrame if no such rows are found.
    """
    # Ensure the column exists and is of string type to use .str.contains()
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")
    if not pd.api.types.is_string_dtype(df[column_name]):
        df[column_name] = df[column_name].astype(str)

    # Use .str.contains() to find rows where the column contains 'MONAGHAN'
    # case=False makes the search case-insensitive
    # na=False treats NaN values as False, so they won't be returned
    return df[df[column_name].str.contains(to_find, case=True, na=False)]
