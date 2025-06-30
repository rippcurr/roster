# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 22:34:39 2025

@author: david
"""
import re

routes = ['199', '185', '182', '191', '192', '155', 'B1', '156', '190X', '181X']

def find_base_runs(main_string: str, search_list: list[str]) -> list[str]:
    """
    Searches a main string for the presence of each string in a given list.

    Args:
        main_string: The string to search within.
        search_list: A list of strings to search for.

    Returns:
        A list of booleans, where each boolean corresponds to a string in the
        search_list. True indicates that the string was found as a substring
        in the main_string, and False indicates it was not found.
    """
    results = []
    for search_term in search_list:
        # The 'in' operator checks if a substring is present within a string.
        is_found = search_term in main_string
        if (is_found):
            results.append(search_term)
            
#TODO

    return results
       

def extract_text_blocks_from_file(file_path):
  """
  Searches a text file for blocks of text delimited by "Depot: MONA VALE BUS DEPOT".
  Each block starts with this string and includes all content until the next occurrence
  of the delimiter or the end of the file.

  Args:
    file_path (str): The path to the .txt file to search.

  Returns:
    list: A list of strings, where each string is a block of text found.
          Returns an empty list if the file is not found or no blocks are found.
  """
  blocks = []
  delimiter = "Depot:  MONA VALE BUS DEPOT"
  current_block = []
  in_block = False

  try:
    with open(file_path, 'r') as f:
      for line in f:
        # Check if the current line starts a new block
        if line.strip().startswith(delimiter):
          # If we were already collecting a block, save it
          if in_block:
            blocks.append("".join(current_block).strip())
            current_block = [] # Reset for the new block
          in_block = True
          current_block.append(line) # Add the delimiter line to the new block
        elif in_block:
          # If inside a block, append the line
          current_block.append(line)

      # After the loop, if we were still collecting a block, add the last one
      if in_block and current_block:
        blocks.append("".join(current_block).strip())

  except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
  except Exception as e:
    print(f"An unexpected error occurred while reading the file: {e}")

  return blocks

def find_school_runs(main_string: str) -> list[str]:
    """
    Searches a string for patterns consisting of exactly three digits followed by the character 'n'.

    Args:
        main_string: The string to search within.

    Returns:
        A list of strings, where each string is a found match of the pattern.
        Returns an empty list if no matches are found.
    """
    # The regular expression pattern:
    # \d{3} : Matches exactly three digit characters (0-9).
    # n     : Matches the literal character 'n'.
    pattern = r'\d{3}n'
    # re.findall() returns a list of all non-overlapping matches of the pattern in the string.
    matches = re.findall(pattern, main_string)
    return matches


def create_routes_list(filename):
    print(f"--- Extracting blocks from '{filename}' ---")
    mona_vale_blocks_1 = extract_text_blocks_from_file(filename)    
    r = []
    for block in mona_vale_blocks_1:
        res = find_base_runs(block, routes)
        sch = find_school_runs(block)
        r.append(res + sch)
    return r

if __name__ == '__main__':

    file_name = '00_mon_thu_journals.txt'
    r = create_routes_list(file_name)
    print(r)
    
    
    
        
