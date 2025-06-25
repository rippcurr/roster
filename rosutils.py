# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 13:18:26 2025

@author: david
"""

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