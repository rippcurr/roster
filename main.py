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
import math
import rosutils as ru
import rosdate as rd

daysoff = ['OFF', 'ADO', 'xxxOFF', 'uwsOFF', 'xxxADO', 'uwsADO', 'xxxOFF9', 'oAsg', 'A/L', 'PFL']
db_files = ['10_mon_thu-db.txt', '11_fri-db.txt', '12_sat-db.txt', '13_sun-db.txt', '14_mon_fri_vac-db.txt' ]
__version__ = '0.1'

def check_for_day_off(code):
  for s in daysoff:
    # It's good practice to ensure elements in the list are also strings
    # if you expect direct string comparison. If not, handle type mismatch.
    if not isinstance(s, str):
      print(f"Warning: Non-string element '{s}' found in list_of_strings. Skipping comparison.")
      continue
    if code == s:
        return True
  return False
    
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
                if len(s) > 4:
                    s = s[:4]
            s = ru.remove_newlines(s)
            cleaned_list[i] = s

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

def match_shifts(days, shifts, vac=False):
    
    times = []
  
    for el in zip(days, shifts):
        if el[0] == 'Friday' and vac==False:
            if (check_for_day_off(el[1])):
                res = el[1]
            else:
                res = ru.find_row_with_string(db_files[1], el[1])
           # print(f'{el[0]}: {res}')
            times.append(res)
        elif el[0] == 'Saturday':
            if (check_for_day_off(el[1])):
                res = el[1]
            else:
                res = ru.find_row_with_string(db_files[2], el[1])
          #  print(f'{el[0]}: {res}')
            times.append(res)
        elif el[0] == 'Sunday':
            if (check_for_day_off(el[1])):
                res = el[1]
            else:
                res = ru.find_row_with_string(db_files[3], el[1])
          #  print(f'{el[0]}: {res}')
            times.append(res)
        elif vac==True:
            if (check_for_day_off(el[1])):
                res = el[1]
            else:
                res = ru.find_row_with_string(db_files[4], el[1])
                times.append(res)
        else:
            if (check_for_day_off(el[1])):
                res = el[1]
            else:
                res = ru.find_row_with_string(db_files[0], el[1])
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
    vac_start = "06-07-2025"


    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.add("roster.log")
    logger.info(f'Starting {os.path.basename(__file__)} Version: {__version__}...')
    logger.info(f'platform: {platform.system()}')

    logger.info(f'filename:         {file}')

    df = pd.read_excel(file)
    get_index = find_row_index_by_search_term(df, "ESS")
    shifts = get_row_as_list(df, get_index[0])
    dates = rd.generate_sequential_dates(start_date, 28, True)
    days = rd.get_day_of_week(dates)
    clean_shifts = clean_roster_list(shifts)
    
    driver_name = clean_shifts[0]
    clean_shifts = clean_shifts[n:]
    
    times = match_shifts(days, clean_shifts, vac=False)
   
    pretty_print(driver_name,dates, days, times)
  