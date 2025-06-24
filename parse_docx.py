# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 21:08:03 2025

@author: david
"""

import os

def find_first_and_last_colon_word(text_string):
    """
    Finds the first and last words in a string that contain a colon (':').

    Args:
        text_string (str): The input string to search.

    Returns:
        tuple: A tuple containing two elements:
               - The first word found that contains a colon (str), or None if not found.
               - The last word found that contains a colon (str), or None if not found.
    """
    words = text_string.split()  # Split the string into words by whitespace
    first_colon_word = None
    last_colon_word = None

    # Find the first word containing a colon
    for word in words:
        if ':' in word:
            first_colon_word = word
            break # Stop after finding the first one

    # Find the last word containing a colon (iterate in reverse)
    for word in reversed(words):
        if ':' in word:
            last_colon_word = word
            break # Stop after finding the first one from the end

    return first_colon_word, last_colon_word


def extract_text_between_words(file_path, start_word, end_word, duty):
    """
    Searches a text file for occurrences of a start word and an end word,
    and extracts all text found between them, concatenating it into a single string.
    The search for start and end words is case-insensitive.

    Args:
        file_path (str): The path to the text file.
        start_word (str): The word that marks the beginning of the text to extract.
        end_word (str): The word that marks the end of the text to extract.

    Returns:
        str: A single string containing all concatenated text segments found
             between the start and end words. Returns an empty string if the
             file is not found, or if the words/patterns are not present.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return ""

    try:
        with open(file_path, 'r') as file:
            full_text = file.read()

        extracted_segments = []
        duty_index = 0
        # Convert search words to lowercase for case-insensitive matching
        start_word_lower = start_word.lower()
        end_word_lower = end_word.lower()

        # We need to search through the text, keeping track of our position
        current_position = 0
        while True:
            # Find the start word, case-insensitive
            start_index = full_text.lower().find(start_word_lower, current_position)

            if start_index == -1:
                # No more start words found
                break

            # Adjust start_index to point to the end of the actual (case-sensitive) start_word
            # This ensures we get the text *after* the start_word
            actual_start_word_end_index = start_index + len(start_word)

            # Find the end word, starting from after the start word
            end_index = full_text.lower().find(end_word_lower, actual_start_word_end_index)

            if end_index == -1:
                # Start word found, but no corresponding end word after it in the rest of the text
                print(f"Warning: Found '{start_word}' but no matching '{end_word}' afterwards.")
                break # Exit loop as we can't find further complete segments

            # Extract the text between the end of the start word and the beginning of the end word
            segment = full_text[actual_start_word_end_index:end_index]
            #extracted_segments.append("-----------------------------------\n")
            extracted_segments.append(duty[duty_index] + " ")
            first_colon_word, last_colon_word = find_first_and_last_colon_word(segment)
            extracted_segments.append("  "+ first_colon_word + "  " + last_colon_word + '\n')
            duty_index += 1
            

            # Update current_position to search for the next pair after the current end word
            current_position = end_index + len(end_word)

        return "".join(extracted_segments)

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return ""
    

def search_word_in_file(file_path, search_word):
    """
    Searches a text file for occurrences of a specific word (case-insensitive)
    and returns a list of lines containing that word.

    Args:
        file_path (str): The path to the text file.
        search_word (str): The word to search for.

    Returns:
        list: A list of strings, where each string is a line from the file
              that contains the search word. Returns an empty list if the
              file is not found or the word is not present.
    """
    found_lines = []
    # Convert the search word to lowercase for case-insensitive matching
    search_word_lower = search_word.lower()

    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return []

    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Check if the lowercase version of the line contains the lowercase search word
                if search_word_lower in line.lower():
                    found_lines.append(line.strip()) # .strip() removes leading/trailing whitespace and newlines
        return found_lines
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []


filename = 'friday-journal.txt'
duty = search_word_in_file(filename, 'Duty')
times = extract_text_between_words(filename, 'Spread', 'Route', duty)


f = open('Friday_duty_times.txt', 'w')
f.write(times)
f.close()



