# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 21:45:33 2025

@author: david
"""

import pandas as pd
from loguru import logger
import platform
import sys
import os
import argparse
import openpyxl
import math
from datetime import datetime, timedelta


__version__ = '0.1'

def clean_roster_list(input_list: list) -> list:
    """
    Removes NaN (Not a Number) values from a given list.

    This function handles both standard float('nan') and pandas/numpy np.nan.

    Args:
        input_list: The list from which to remove NaN values.

    Returns:
        A new list with all NaN values removed.
    """
    cleaned_list = []
    for item in input_list:
        # Check if the item is a float and if it's NaN
        # math.isnan() works for float('nan') and np.nan
        if isinstance(item, (float, int)) and math.isnan(item):
            continue # Skip NaN values
        else:
            cleaned_list.append(item)
            
    #now check for elements that start with 'H' or 'D' and check they are correct length
    for i in range(len(cleaned_list)):
        if isinstance(cleaned_list[i], str):
            s = cleaned_list[i]
            first_char = s[0]
            if first_char == 'D' or first_char == 'H':
                if len(cleaned_list[i]) > 4:
                    cleaned_list[i] = s[:4]

    return cleaned_list

def get_row_as_list(df: pd.DataFrame, row_index: int) -> list:
    """
    Extracts a specific row from a Pandas DataFrame and returns it as a list.

    Args:
        df: The input Pandas DataFrame.
        row_index: The integer index of the row to extract.

    Returns:
        A list representing the data in the specified row.
        Returns an empty list if the row_index is out of bounds or df is not a DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        print("Error: The first argument must be a Pandas DataFrame.")
        return []

    if row_index < 0 or row_index >= len(df):
        print(f"Error: Row index {row_index} is out of bounds for DataFrame with {len(df)} rows.")
        return []

    try:
        # Select the row by its integer index and convert it to a list
        row_list = df.iloc[row_index].tolist()
        return row_list
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def get_day_of_week(date_strings: list[str]) -> list[str]:
    """
    Converts a list of date strings (dd-mm-yyyy) into a list of corresponding
    days of the week.

    Args:
        date_strings: A list of date strings in 'dd-mm-yyyy' format.

    Returns:
        A list containing the full names of the days of the week (e.g., 'Monday', 'Tuesday').
        Returns an empty list if an invalid date format is encountered for any date.
    """
    days_of_week = []
    for date_str in date_strings:
        try:
            # Parse the date string into a datetime object
            date_object = datetime.strptime(date_str, "%d-%m-%Y")
            # Get the full weekday name
            day_name = date_object.strftime("%A")
            
            days_of_week.append(day_name)
        except ValueError:
            print(f"Error: Invalid date format for '{date_str}'. Expected 'dd-mm-yyyy'.")
            # You might want to handle this differently, e.g., append None or raise an error.
            # For this example, we'll return an empty list if any date is invalid
            # to indicate a failure in processing the whole list.
            return []
    return days_of_week

def generate_sequential_dates(start_date_str: str, n_days: int) -> list[str]:
    """
    Generates a list of sequential string dates starting from a given date.

    Args:
        start_date_str (str): The starting date in "dd-mm-yyyy" format.
        n_days (int): The number of sequential days to generate (including the start date).

    Returns:
        list[str]: A list of sequential dates in "dd-mm-yyyy" string format.
                   Returns an empty list if n_days is less than or equal to 0.

    Raises:
        ValueError: If the start_date_str is not in the "dd-mm-yyyy" format.
    """
    if n_days <= 0:
        return []

    try:
        # Convert the start_date_str to a datetime object
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Invalid start_date_str format. Expected 'dd-mm-yyyy'.")

    date_list = []
    for i in range(n_days):
        # Calculate the next date
        current_date = start_date + timedelta(days=i)
        # Format the datetime object back to "dd-mm-yyyy" string
        date_list.append(current_date.strftime("%d-%m-%Y"))

    return date_list

def find_row_index_by_search_term(df: pd.DataFrame, search_term: str) -> list[int]:
    """
    Finds the index/indices of rows in a Pandas DataFrame that contain a specific search term.
    This function searches across all columns of the DataFrame.

    Args:
        df: The input Pandas DataFrame.
        search_term: The string term to search for within the DataFrame.

    Returns:
        A list of integer indices where the search term was found.
        Returns an empty list if the search term is not found or if the input is invalid.
    """
    if not isinstance(df, pd.DataFrame):
        print("Error: The first argument must be a Pandas DataFrame.")
        return []

    if not isinstance(search_term, str):
        print("Error: The search term must be a string.")
        return []

    found_indices = []
    # Iterate through each row of the DataFrame
    for index, row in df.iterrows():
        # Check if the search_term exists in any of the row's values (converted to string)
        if any(search_term in str(value) for value in row.values):
            found_indices.append(index)
    return found_indices

def find_row_with_string(file_path, search_string):
    """
    Searches a text file for the first occurrence of a given string (case-insensitive)
    and returns the entire row of text that contains it.

    Args:
        file_path (str): The path to the text file.
        search_string (str): The string to search for within the file's lines.

    Returns:
        str or None: The first line (row) from the file that contains the
                     search_string, or None if the file is not found,
                     an error occurs, or the string is not found in any row.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None

    # Convert the search string to lowercase for case-insensitive matching
    search_string_lower = search_string.lower()

    try:
        with open(file_path, 'r' ) as file:
            for line_num, line in enumerate(file, 1):
                # Check if the lowercase version of the line contains the lowercase search string
                if search_string_lower in line.lower():
                    return line.strip() # Return the line and remove leading/trailing whitespace and newlines
        
        # If the loop finishes, the string was not found
        #print(f"The string '{search_string}' was not found in the file '{file_path}'.")
        return f"*** {search_string} Shift not found ***"

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def match_shifts(days, shifts):
    
    times = []
  
    for el in zip(days, shifts):
        if el[0] == 'Friday':
            if (el[1] == 'OFF'or el[1] == 'ADO'):
                res = el[1]
            else:
                res = find_row_with_string('Friday_duty_times.txt', el[1])
           # print(f'{el[0]}: {res}')
            times.append(res)
        elif el[0] == 'Saturday':
            if (el[1] == 'OFF'or el[1] == 'ADO'):
                res = el[1]
            else:
                res = find_row_with_string('Saturday_duty_times.txt', el[1])
          #  print(f'{el[0]}: {res}')
            times.append(res)
        elif el[0] == 'Sunday':
            if (el[1] == 'OFF'or el[1] == 'ADO'):
                res = el[1]
            else:
                res = find_row_with_string('Sunday_duty_times.txt', el[1])
          #  print(f'{el[0]}: {res}')
            times.append(res)
        else:
            if (el[1] == 'OFF'or el[1] == 'ADO'):
                res = el[1]
            else:
                res = find_row_with_string('Mon-Thur_duty_times.txt', el[1])
          #  print(f'{el[0]}: {res}')
            times.append(res)
    return times            
        
        

def pretty_print(driver, dates, days, times):
    print(f'Driver:  {driver}:')
    for item in zip(dates,days, times):
        print(f'| {item[0]} | {item[1]:<9} | {item[2]:<32} |')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parse schedule',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('f_roster', metavar='ROSTER', nargs='+',
                        help='Name of roster file')

    args = parser.parse_args()
    
    file = args.f_roster[0]
    
    n = 3
    start_date = "22-06-2025"


    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.add("roster.log")
    logger.info(f'Starting {os.path.basename(__file__)} Version: {__version__}...')
    logger.info(f'platform: {platform.system()}')

    logger.info(f'filename:         {file}')

    df = pd.read_excel(file)
    get_index = find_row_index_by_search_term(df, "MONAGHAN")
    shifts = get_row_as_list(df, get_index[0])
    dates = generate_sequential_dates(start_date, 28)
    days = get_day_of_week(dates)
    clean_shifts = clean_roster_list(shifts)
    print(clean_shifts)
    
    driver_name = clean_shifts[0]
    clean_shifts = clean_shifts[n:]
    
    times = match_shifts(days, clean_shifts)
   
    pretty_print(driver_name,dates, days, times)
  