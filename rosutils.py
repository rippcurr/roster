# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 13:18:26 2025

@author: david
"""

import os

def remove_newlines(text_string):
  """
  Removes all newline characters ('\\n') from a given string.

  Args:
    text_string: The input string that may contain newline characters.

  Returns:
    A new string with all newline characters removed.
  """
  # Check if the input is actually a string to prevent errors
  if not isinstance(text_string, str):
    # You can choose to raise an error, convert to string, or return as-is
    # For this function, we'll raise a TypeError if it's not a string.
    raise TypeError("Input must be a string.")

  # The replace() method is used to find all occurrences of '\n'
  # and replace them with an empty string, effectively removing them.
  return text_string.replace('\n', '')

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