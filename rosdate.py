# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 21:56:38 2025

@author: david
"""
from datetime import datetime, timedelta, date

def is_date_after(seq_date: date, given_date: date) -> bool:
    """
    Checks if a given date falls after a date provided as a string.

    Args:
        date_string: The reference date in 'dd-mm-yyyy' format.
        given_date: The date to check against the reference date.

    Returns:
        True if the given_date is after the date_string, False otherwise.
        Returns False if the date_string is in an invalid format.
    """
    try:
        # Convert the date string to a datetime.date object
        # reference_date = datetime.strptime(date_string, '%d-%m-%Y').date()
        
        # Compare the two date objects
        return given_date > seq_date
        
    except ValueError:
        # Handle the case where the date string is not in the correct format
        print(f"Error: The date string '{date_string}' is not in 'dd-mm-yyyy' format.")
        return False

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
            return []
    return days_of_week

def generate_sequential_dates(start_date_str: str, n_days: int, is_vac=False) -> list[str]:
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
        date_str = current_date.strftime("%d-%m-%Y")
        # if (is_vac):
        #     if (is_date_after(current_date, date(2025,7,6))):
        #         date_str += 'v'
                
        date_list.append(date_str)

    return date_list
