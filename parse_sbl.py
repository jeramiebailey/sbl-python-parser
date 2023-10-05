"""
This script extracts data from a text file
containing textual variants and witness abbreviations,
and outputs the data to an Excel file.
The script parses the input text file, extracts the data,
and assigns group, variant, and occurrence numbers to each entry in the data.
The output Excel file contains one row for each textual variant,
with columns for book name, chapter number, verse number,
textual variant, witness abbreviation, group number, variant number, and occurrence number.

For more information on how to use this script,
please refer to the README.md file in the project directory.
"""

# -- coding: utf-8 --

# =============================================================================
# STEP 1:
#    Initialize script
# =============================================================================


# Step 1a: Import necessary libraries

import re
import pandas as pd
from collections import defaultdict
import numpy as np

# Step 1b: Define global variables
header_pattern = re.compile(
    r'^(?P<book_name>[\w\d\s]+)\s+(?P<chapter_num>\d+):(?P<verse_num>\d+)')
group_pattern = re.compile(
    r'^\s*•\s*')
variant_pattern = re.compile(
    r'(?P<text_var>[\w\-\[\]\s\+\–]+)(?P<witness_abbr>\b(?:WH|NA28|Treg|RP)+\b)')

# =============================================================================
# STEP 2:
#    Extract textual variants
# =============================================================================

# Step 2a: Define "extract_textual_variants()" function


def extract_textual_variants(input_text):  # BREAKPOINT
    """
    Extracts textual variants and witness abbreviations from the input text.

    Args:
        input_text (str): The input text containing textual variants and witness abbreviations.

    Returns:
        list: A list of tuples, where each tuple contains a textual variant
        and its associated witness abbreviation.
    """

    # Step 2b: Define a regular expression pattern to match textual variants (with ellipses)
    # and their associated witness abbreviations.
    # The pattern consists of three parts:
    # 1. Textual variant: (?:\S+\s*)…(?:\s*\S+)
    # 2. Witness abbreviation: (.*?)
    # 3. Lookahead assertion to ensure the correct end of the match: (?=•|\d+:\d+|$)
    pattern = r"((?:\S+\s*)…(?:\s*\S+))\s*(.*?)\s*(?=•|\d+:\d+|$)"

    # Step 2c: Use 're.findall' to find all matches of the pattern in the input text.
    # 're.MULTILINE' flag is used to handle multiline input text.
    matches = re.findall(pattern, input_text)

    # Step 2d: Initialize an empty list to store the extracted data.
    extracted_data = []

    # Step 2e: Iterate through all matches found.
    for match in matches:
        # Each 'match' is a tuple containing the textual variant
        # and its associated witness abbreviation.
        textual_variant, witness_abbreviation = match

        # Append the current match (tuple) to the 'extracted_data' list.
        extracted_data.append((textual_variant, witness_abbreviation))

    # Step 2f: Create 'input_text' column and assign input_text to every row
    input_text_list = [input_text] * len(extracted_data)
    for i, input_text in enumerate(input_text_list):
        extracted_data[i] += (input_text,)

    # Step 2g: Return the list of extracted textual variants and witness abbreviations.
    return extracted_data

# =============================================================================
# STEP 3:
#    Assign identifier numbers to "groups", "textual variants" and "occurrences"
# =============================================================================

# Step 3a: Define "assign_identifier_numbers() function,
# which assigns unique identifier numbers to each row of the DataFrame
# based on its group, variant, and occurrence."


def assign_identifier_numbers(data_frame):
    """
    Assigns group numbers, variant numbers, and occurrence numbers
    to each column in each row of the DataFrame.

    Args:
        data_frame (pd.DataFrame): A pandas DataFrame with columns:
        'record_number', 'book_name', 'chapter_number', 'verse_number',
        'textual_variant', 'witness_abbreviation', 'group_number', and 'occurrence_number'

    Returns:
        None: This function modifies the input DataFrame in-place, adding 'group_number'
        and 'occurrence_number' columns to assign unique identifier numbers to each row of
        the DataFrame based on its group and occurrence (NOT 'variant_number' column).

    """

    # Step 3b NEW: Check to make sure the necessary columns are present in the DataFrame
    if not all(col in data_frame.columns for col in [
        'record_number', 'book_name', 'chapter_number',
        'verse_number', 'textual_variant', 'witness_abbreviation']):
        raise ValueError('One or more required columns not found in DataFrame')

    # Step 3c: Sort data frame by textual variant,
    # then by group number
    if 'group_number' in data_frame.columns:
        data_frame = data_frame.sort_values(
            by=['textual_variant', 'group_number'],
            ignore_index=True
        )
    else:
        raise ValueError('group_number column not found in DataFrame')

    # Step 3d: check to make sure the 'book_name' column is present in the DataFrame
    if 'book_name' not in data_frame.columns:
        raise ValueError('book_name column not found in DataFrame')

    # Step 3e: Group data frame by textual variant and group number
    grouped_data = data_frame.groupby(['textual_variant', 'group_number'])

    # Step 3f: Iterate through each group in the grouped DataFrame.
    last_variant = ""
    last_input_text = ""
    for group_name, group_data in grouped_data:

        # Step 3f1: Assign a unique identifier number to each group of data
        # based on its textual variant and group number
        group_data['group_identifier'] = f"{group_name[0]}_{group_name[1]}"
        group_data['group_identifier'] = group_data['group_identifier'].astype('category').cat.codes

    # Step 3g: Create a new 'group_number' column
    # based on the unique combination of 'textual_variant', 'group_number', and 'book_name'
    data_frame['group_number'] = data_frame.apply(
        lambda row: f"{row['textual_variant']}_{row['group_number']}_{row['book_name']}", axis=1)

    # Step 3h: Assign unique identifier numbers to each group based on their 'group_number'
    data_frame['input_text'] = data_frame.groupby('group_number').ngroup()

    # Step 3i: Drop the 'group_number' column since we no longer need it
    data_frame.drop(columns=['group_number'], inplace=True)

    # Step 3j: Initialize new columns in the DataFrame
    # for group numbers, variant numbers, and occurrence numbers
    data_frame['group_number'] = pd.Series(np.zeros(len(data_frame), dtype=int))
    data_frame['variant_number'] = pd.Series(np.zeros(len(data_frame), dtype=int))
    data_frame['occurrence_number'] = pd.Series(np.zeros(len(data_frame), dtype=int))


    # Step 3k: Initialize variables for tracking the following identifiers:
    # group numbers, variant numbers, and occurrence numbers. These variables will be used
    # to assign unique identifier numbers to each row of the DataFrame.
    group_number = 1
    variant_number = 1 # Added variant_number initialization
    occurrence_number = 1
    last_group = ""
    last_record = ""

    # Step 3l: Group the data frame by textual variant and record number
    grouped_data = data_frame.groupby(['textual_variant', 'group_number'])

    # Step 3m: Iterate through each group in the grouped DataFrame.
    last_variant = ""
    last_input_text = ""
    for group_name, group_data in grouped_data:
        # Check if the current textual variant and record number is different from the last one.
        if last_variant != group_name[0] or last_record != group_name[1]:
            # If the textual variant and record number is different,
            # reset group_number and occurrence_number.
            group_number = 1
            variant_number = 1 # Added variant_number reset
            # REMOVED:
            # variant_number += 1
            occurrence_number = 1

        # Step 3m1: Iterate through each row in the current group.
        # ***change the second iteration variable name
        # ***to something other than group_data
        # ***to avoid name conflicts with the grouped data in Step 3h.
        for (textual_variant, input_text), row_data in grouped_data:  # BREAKPOINT

            # Step 3m2: Check if the current textual variant
            # and input_text is different from the last one.
            if last_variant != textual_variant or last_input_text != input_text:
                # If the textual variant and group number is different,
                # reset variant_number and occurrence_number.
                variant_number += 1
                occurrence_number = 1
                # Update last_group variable for the next iteration
                last_group = group_number

            # Step 3m3: Iterate through each row in the current group.
            for occurrence_number, index in enumerate(row_data.index):

                # Step 3m4: Update the last_variant and last_input_text variables for the next iteration.
                last_variant = textual_variant
                last_input_text = input_text

                # Step 3m5: Update the current row with the following calculated identifiers:
                # group_number, variant_number, and occurrence_number.
                # These numbers are based on the group, variant, and occurrence of the current row within the DataFrame.
                data_frame.at[index, "group_number"] = group_number
                data_frame.at[index, "variant_number"] = variant_number
                data_frame.at[index, "occurrence_number"] = occurrence_number
                # BREAKPOINT

                # Step 3m6: Increment the occurrence_number for the next iteration.
                if occurrence_number != 0:
                    # Increment the occurrence_number for the next iteration.
                    occurrence_number += 1

            # Step 3m7: Increment the variant_number for the next iteration.
            if occurrence_number == 1:
                variant_number += 1

            # Step 3m8: Reset the occurrence_number for the next iteration.
            if occurrence_number != 0:
                occurrence_number = 1

# =============================================================================
# STEP 4:
#    Create a DataFrame with extracted data.
# =============================================================================

# Step 4a: Define "create_dataframe()" variable


def create_dataframe(header, extracted_data):
    """
    Creates a DataFrame using the extracted header and data.

    Args:
        header (str): The header string containing book name, chapter number, and verse number.
        extracted_data (list): A list of tuples
        containing the extracted textual variants and witness abbreviations.

    Returns:
        pd.DataFrame: A DataFrame containing the header and extracted data.
    """

    # Step 4b: Extract the book name, chapter number, and verse number from the header.
    book_name, chapter_number, verse_number = parse_header(header)

    # Step 4c: Create a new DataFrame with the required columns.
    data_frame = pd.DataFrame(columns=[
        "record_number", "book_name", "chapter_number", "verse_number",
        "textual_variant", "witness_abbreviation",
        "group_number", "variant_number", "occurrence_number"])

    # Step 4d: Loop through the extracted data and append each entry to the new DataFrame.
    rows = []
    record_number = 1
    for row_tuple in extracted_data:
        row_dict = {
            "record_number": record_number,
            "book_name": book_name,
            "chapter_number": chapter_number,
            "verse_number": verse_number,
            "textual_variant": row_tuple[0],
            "witness_abbreviation": row_tuple[1],
            "group_number": 0,
            "variant_number": 0,
            "occurrence_number": record_number
        }
        rows.append(row_dict)
        record_number += 1  # increment record_number after each iteration

    # Step 4e: Append the rows to the data_frame.
    data_frame = pd.concat(
        [data_frame, pd.DataFrame(rows)], ignore_index=True
        )

    # REMOVE???
    # Step 4e Append a new row to the data_frame with the following values:
    # - book_name, chapter_number, and verse_number from the header
    # - textual_variant, witness_abbreviation, and occurrence_number from the current row in the extracted_data
    # - group_number and variant_number will be assigned later in the assign_identifier_numbers() function
    # data_frame = pd.DataFrame(rows, columns=[
    #    "record_number", "book_name", "chapter_number", "verse_number",
    #    "textual_variant", "witness_abbreviation", "occurrence_number"
    #])

    # Step 4f: Assign group_number, variant_number, and occurrence_number to the DataFrame.
    assign_identifier_numbers(data_frame)

    # Step 4g: Reorder the columns in the DataFrame to match the desired order.
    data_frame = data_frame[["record_number", "book_name", "chapter_number", "verse_number",
                             "textual_variant", "witness_abbreviation",
                             "group_number", "variant_number", "occurrence_number"]]

    # Step 4h: Check if the book_name column is present in the DataFrame
    if 'book_name' not in data_frame.columns:
        print("book_name column is missing from the DataFrame")

    # Step 4i: Return the Dataframe
    return data_frame

# =============================================================================
# STEP 5:
#    Parse the header information.
# =============================================================================

# Step 5a: Define 'parse_header()' function to extract values from the input text
# such as book_name, chapter_number, and verse_number.


def parse_header(input_text):
    """
    Parses the header to extract book name, chapter number, and verse number.

    Args:
        input_text (str): The input text containing the header information.

    Returns:
        tuple: A tuple containing the book name, chapter number, and verse number.
    """

    # Define a regex pattern to match the book name, chapter number, and verse number.
    pattern = r"(\w+)\s+(\d+):(\d+)"

    # Search for the pattern in the input text.
    match = re.search(pattern, input_text)
# BREAKPOINT

    # Step 5b: Extract the book name, chapter number, and verse number from the header text

    if match:
        # If a match is found, extract the book name, chapter number, and verse number.
        book_name = match.group(1)
        chapter_number = int(match.group(2))
        verse_number = int(match.group(3))

        # Return the extracted information as a tuple.
        return book_name, chapter_number, verse_number
    else:
        # If no match is found, raise a ValueError.
        raise ValueError("Invalid header format")

# Step 5c: Initialize the input_text variable
# with a sample input text containing the header information.
# Main processing code
input_text = """
Matthew 1:5
1:5 Βόες … Βόες WH NA28 ] Βοὸς … Βοὸς Treg; Βοὸζ … Βοὸζ RP
• Ἰωβὴδ … Ἰωβὴδ WH Treg NA28 ] Ὠβὴδ … Ὠβὴδ RP
"""


# Step 5d: Extract the textual variants and witness abbreviations from the input text.

extracted_data = extract_textual_variants(input_text)
# BREAKPOINT

# Step 5e: Create a Pandas DataFrame with the required columns

data_frame = create_dataframe(input_text, extracted_data)
# BREAKPOINT

# =============================================================================
# STEP 6: Defines the parse_variants() function,
#         which takes an input line
#         containing one or more textual variants and their witnesses
#         and returns a list of tuples
#         containing each textual variant and its witnesses.
# =============================================================================

# Step 6a: Define 'parse_variants()' function
# to extract each textual variant and its witnesses from an input line.


def parse_variants(input_line):
    """
    Parses an input line containing textual variants and returns a list of tuples
    containing each textual variant and its witness abbreviation(s).

    Args:
        input_line (str): An input line containing a section
        with one or more textual variants and their witnesses.

    Returns:
        list: A list of tuples containing
        the variant number, textual variant, and witness abbreviation(s).
"""

    # Step 6a1: Prepare a list to store the results
    results = []

    # Step 6a2: Check if the ' ] ' separator exists in the input line
    if ' ] ' in input_line:

        # If the separator exists,
        # split the input_line at ' ] '
        # to separate the first textual variant and the second textual variant
        # Example: 'Βόες … Βόες WH NA28 ] Βοὸς … Βοὸς Treg'
        first_variant_section, subsequent_variant_section = input_line.split(' ] ')

        # Remove any whitespace at the beginning and end of the sections
        first_variant_section = first_variant_section.strip()
        subsequent_variant_section = subsequent_variant_section.strip()
# BREAKPOINT

    else:
        # If the separator does not exist,
        # consider the entire input line as the first textual variant section
        first_variant_section = input_line.strip()

        # If the separator does not exist,
        # set an empty string for subsequent textual variant
        subsequent_variant_section = ""

        # Remove any whitespace at the beginning of the first variant section
        first_variant_section = first_variant_section.strip()
# BREAKPOINT

    # Step 6b: Use a regular expression pattern
    # to find all witness-text pairs in the first_variant_section.
    # The pattern matches a group of characters that starts with one or more word characters,
    # followed by one or more spaces, followed by one or more non-semicolon characters.
    # Each match should be in the format: witness abbreviation followed by textual variant.
    # Example: 'WH Βόες … Βόες', 'NA28 Βόες … Βόες'
    first_variant_matches = re.findall(r'(\w+\s+[^;]+)', first_variant_section)

    # Step 6c: Iterate through the matches to process each witness-text pair
    for match in first_variant_matches:
        # Split the match by the first space to get the witness and the text
        # Example: 'WH', 'Βόες … Βόες'
        witness, text = match.split(' ', 1)
        # Add the (text, witness) tuple to the results list
        results.append((f"v{len(results)+1}", text.strip(), witness.strip()))
# BREAKPOINT

    # Step 6d: If subsequent_variant_section is not empty,
    if subsequent_variant_section:
        # split it by '; ' to separate each subsequent variant.
        # Example: 'Βοὸς … Βοὸς Treg; Βοὸζ … Βοὸζ RP …'
        subsequent_variants_list = subsequent_variant_section.split('; ')

        # Remove any whitespace at the beginning of each subsequent variant
        subsequent_variants_list = [
            variant.strip()
            for variant in subsequent_variants_list
        ]

    # Step 6e: Iterate through the subsequent_variants_list to process each variant
    for variant in subsequent_variants_list:
        # Split the variant by the first space to get the witness and the text.
        # Each variant should be in the format: textual variant followed by witness abbreviation.
        # Example: 'Βοὸς … Βοὸς Treg', 'Βοὸζ … Βοὸζ RP'
        witness, text = variant.split(' ', 1)
        # Add the (text, witness) tuple to the results list
        results.append((f"v{len(results)+1}", text.strip(), witness.strip()))
# BREAKPOINT

    # Step 6g: ADD DESCRIPTION
    return results

# =============================================================================
# STEP 7: Define the get_files() function to prompt the user
#         to input the path for the input file and the output file.
# =============================================================================

# Step 7a: Define 'def get_files()' function
# to prompts the user to enter the paths for the input and output files.


def get_files():
    """
    Prompts the user to enter the paths for the input and output files.

    Returns:
        tuple: A tuple containing the input file path and the output file path.
    """
    input_file = input("Enter path for input file: ")
    output_file = input("Enter path for output file: ")
    return input_file, output_file

# =============================================================================
# STEP 8: Read in and clean up input file contents
# =============================================================================

# Step 8a: Define the 'clean_file_contents' function.


def clean_file_contents(file_path):
    """
        Call the read_input_file function
        to read in the input file
        at the specified file path as a list of strings.
        If the file is not found, raises a FileNotFoundError exception.
        Then, remove any newline characters from each line of the file
        to ensure that they do not interfere
        with our regular expression pattern matching when extracting data.

            Args:
                file_path (str): The path to the input file.
            Returns:
                list[str]: A list of strings
                where each string represents
                a line in the input file
                without new line characters.
            Raises:
                FileNotFoundError: If the input file cannot be located.
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as file_handle:
            file_contents = file_handle.readlines()
        cleaned_file_contents = [line.strip() for line in file_contents]
        return cleaned_file_contents
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "Unable to locate input file. "
            "Please check the file path and try again."
        ) from exc

# =============================================================================
# STEP 9: Extract data from the input file
# =============================================================================

# Step 9a: Define 'extract_data()' function.


def extract_data(input_text):
    """
    Processes the input text to separate clusters of textual variants
    and their witnesses into individual lines, and extracts relevant data
    from each line using regular expressions.

    Args:
        input_text (str): A string containing the input file text.

    Returns:
        pd.DataFrame: A pandas DataFrame
        where each row represents a variation unit observed in the witnesses.
        The relevant fields for each row are
        'record_number', 'book_name', 'chapter_number', 'verse_number',
        'textual_variant', 'witness_abbreviation',
        'group_number', 'variant_number', and 'occurrence_number'.
    """

    # Step 9b: Split the input text into lines.
    lines = input_text.split("\n")

    # Step 9c: Loop through each line and concatenate it with the previous line
    # if it does not start with a book/chapter/verse header or a group marker.
    line_groups = []
    current_line_group = []
    for line in lines:
        header_pattern = re.compile(r'^\w+\s+\d+:\d+')
        group_pattern = re.compile(r'^\s*•\s*')
        if header_pattern.match(line) or group_pattern.match(line):
            if current_line_group:
                line_groups.append(' '.join(current_line_group))
                current_line_group = []
        current_line_group.append(line.strip())
    if current_line_group:
        line_groups.append(' '.join(current_line_group))

    # Step 9d: Define regular expression patterns
    # for matching book/chapter/verse headers and textual variants.
    #This should account for alphanumeric book names like "1 Corinthians"
    header_pattern = re.compile(
        r'^(?P<book_name>[\w\d\s]+)\s+(?P<chapter_num>\d+):(?P<verse_num>\d+)')
    group_pattern = re.compile(r'^\s*•\s*')
    variant_pattern = re.compile(
        r'(?P<text_var>[\+–]?[\w\-\[\]\s]+)(?P<witness_abbr>\b(?:WH|NA28|Treg|RP)+\b)')

    # Step 9e: Loop through each line group and extract relevant data
    # using the defined regular expression patterns.
    # Create an empty list to store extracted data.
    data_list = []

    # Step 9f: Initialize variables to keep track of the current book, chapter, and verse.
    record_number = 1
    current_book = None
    current_chapter = None
    current_verse = None
    group_number = 1
    variant_number = 1
    occurrence_counts = defaultdict(int)

    # Step 9g: Loop through each line and extract relevant data
    # using the defined regular expression patterns.
    for line_group in line_groups:

        # Step 9g1: Check for a book/chapter/verse header.
        header_match = None  # Initialize header_match to None
        for line in line_group.split('\n'):
            header_match = header_pattern.match(line)
            if header_match:
                break  # Break the loop if a match is found

        # Step 9g2: If a header is found, update the current book, chapter, and verse.
        if header_match:
            # Extract the book name.
            current_book = header_match.group('book_name')
            # Extract the chapter number.
            current_chapter = int(header_match.group('chapter_num'))
            # Extract the verse number.
            current_verse = int(header_match.group('verse_num'))
            group_number = 1
            variant_number = 1
            occurrence_counts = defaultdict(int)
            record_number += 1
            print(f"Header found: {current_book} {current_chapter}:{current_verse}")
        else:
            # Check for a group marker.
            group_match = group_pattern.match(line)
            # If a group marker is found,
            # update the group number, variant number, and occurrence number.
            if group_match:
                record_number += 1
                group_number += 1  # BREAKPOINT
                variant_number = 1
                occurrence_counts = defaultdict(int)
                # Remove the group marker from the line.
                line = line.lstrip("•").strip()

        # 9h: Check for textual variants and witness abbreviations.
        variant_matches = list(variant_pattern.finditer(line))

        # 9i: If there are no textual variants, skip to the next line.
        if not variant_matches:
            continue

        # Loop through the variant matches.
        for i, match in enumerate(variant_matches):

            # Extract the variant text.
            variant_text = match.group('text_var').strip()
            # Extract the witness abbreviation.
            witness_abbr = match.group('witness_abbr')
            # Add the extracted data to the data_list.
            data_list.append({
                    'record_number': record_number,
                    'book_name': current_book,
                    'chapter_number': current_chapter,
                    'verse_number': current_verse,
                    'textual_variant': variant_text,
                    'witness_abbreviation': witness_abbr,
                    'group_number': group_number,
                    'variant_number': variant_number,
                    'occurrence_number': occurrence_counts[variant_text] + 1
            })
# BREAKPOINT

            # Increment the occurrence number for this variant.
            occurrence_counts[variant_text] += 1  # BREAKPOINT

            # Increment the variant number
            variant_number += 1  # BREAKPOINT

    # Step 9j: Convert extracted data list into a pandas DataFrame.
    extracted_data_df = pd.DataFrame(data_list)

    # Step 9k: Return the extracted data DataFrame.
    return extracted_data_df

# =============================================================================
# STEP 10: Write output to file
# =============================================================================

# Step 10a: Define 'write_output_file()' function.


def write_output_file(data_frame, output_file_path):  # BREAKPOINT
    """
    Writes the extracted data to an output file in Excel format.

    Args:
        data_frame (pd.DataFrame): A pandas DataFrame containing the extracted data.
        output_file_path (str): The path where the output file should be written.
    """
# BREAKPOINT

    # Step 10b: Create a context in which the pd.ExcelWriter object is used.
    # When the context is exited, the object is automatically closed,
    # and the output file is saved.
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:

        # Write the data to the output file using a tab delimiter
        data_frame.to_excel(writer, sheet_name='Sheet1', index=False)

    print(f"Data has been successfully extracted and saved to {output_file_path}")

# =============================================================================
# STEP 11: Read input file and return its contents as a string
# =============================================================================

# Step 11a: Define 'read_input_file' function.


def read_input_file(file_path):
    """
    Reads the input file and returns its contents as a string.

    Args:
        file_path (str): The path to the input file.

    Returns:
        str: The contents of the input file as a string.
    """

    # Step 11b: Read the input file and store its contents as a list of lines
    with open(file_path, "r") as file:
        input_lines = file.readlines()

    # Step 11c: Join the lines together to form a single string
    input_text = "".join(input_lines)

    # Step 11d: Return the input file contents as a string
    return input_text
# BREAKPOINT

# =============================================================================
# STEP 12: Extract data from input file and return pandas DataFrame.
# =============================================================================

# Step 12a: Define the 'process_input_file()' function.


def process_input_file(input_file):
    """
    Reads in an input file, extracts relevant data,
    assigns group, variant, and occurrence numbers,
    and returns a pandas DataFrame with the resulting data.

    Args:
        input_file (str): The path to the input file.

    Returns:
        pd.DataFrame: A pandas DataFrame where each row represents a variation unit
        observed in the witnesses.
        The relevant fields for each row are 'book_name', 'chapter_number', 'verse_number',
        'textual_variant', 'witness_abbreviation',
        'group_number', 'variant_number','occurrence_number'.
    """

    # Step 12a1: Read in the input file.
    file_contents = read_input_file(input_file)

    # Step 12a2: Check if the input file is empty or could not be read.
    if not file_contents:
        print("The input file is empty or could not be read.")
        return None

    # Steph 12a3: Extract data from the input file.
    extracted_data_df = extract_data(file_contents)

    # Step 12b: Return the resulting DataFrame.
    return extracted_data_df

# =============================================================================
# STEP 13: Identify and assign group, variant, and occurrence numbers
#          to each row of the DataFrame
# =============================================================================

# Step 13a: Define 'identify_and_assign()' function


def identify_and_assign(data_frame):
    """
    Identifies and assigns group, variant, and occurrence numbers to each row of the DataFrame.

    Args:
        data_frame (pd.DataFrame): A pandas DataFrame where each row represents a variation unit
        observed in the witnesses.
    Returns:
        pd.DataFrame: A pandas DataFrame where each row represents a variation unit observed
        in the witnesses. The 'group_number', 'variant_number', and 'occurrence_number'
        fields for each row have been populated based on the corresponding variation units.
    """

    # Step 13b: Group the DataFrame by book_name, chapter_number, and verse_number.
    grouped_data = data_frame.groupby(['group_number', 'textual_variant', 'witness_abbreviation'])

    # Step 13c: Create an empty DataFrame with the same columns as the input DataFrame.
    output_data_frame = pd.DataFrame(columns=data_frame.columns)

    # Step 13d: Define a function to assign group, variant, and occurrence numbers
    # within each verse group
    def assign_numbers(group_data_frame):
        """
        Assigns group, variant, and occurrence numbers to each row in the group DataFrame.

        Args:
            group_data_frame (pd.DataFrame): A pandas DataFrame representing a single group
            of variation units.

        Returns:
            pd.DataFrame: A pandas DataFrame with assigned group, variant, and occurrence
            numbers for each row in the input DataFrame.
        """

        # Make a copy of the input DataFrame to avoid modifying the original
        group_data_frame = group_data_frame.copy()

        # Group by textual variant and witness abbreviation
        grouped = group_data_frame.groupby(['textual_variant', 'witness_abbreviation'])

        # Assign group_number as the group index + 1
        group_data_frame['group_number'] = grouped.ngroup() + 1

        # Assign variant_number as the cumulative count of each group + 1
        group_data_frame['variant_number'] = grouped.cumcount() + 1

        # Assign occurrence_number as the cumulative sum of non-null witness abbreviations
        # within each group
        group_data_frame['occurrence_number'] = grouped['witness_abbreviation'].transform(
            lambda x: x.notnull().cumsum())

        # Return the modified DataFrame
        return group_data_frame

    # Step 13e: Loop through each group of the grouped data.
    for group_key, group_value in grouped_data:
        # Call the 'assign_numbers' function for each group and concatenate the result
        # with the output_data_frame.
        output_data_frame = pd.concat([output_data_frame, assign_numbers(group_value)])
    # BREAKPOINT

    # Step 13f: Reorder the columns in the DataFrame to match the desired order.
    output_data_frame = output_data_frame[[
        "record_number", "book_name", "chapter_number", "verse_number",
        "textual_variant", "witness_abbreviation",
        "group_number", "variant_number", "occurrence_number"]]

    # Step 13g: Return the output_data_frame with assigned group, variant, and occurrence numbers.
    return output_data_frame

# =============================================================================
# STEP 14: Extract the header values from input text
# =============================================================================

# Step 14a: Define 'extract_header()' function


def extract_header(input_text):
    """
    Extracts the header
    containing book name, chapter number, and verse number
    from the input text.

    Args:
        input_text (str): The input text containing the header information.

    Returns:
        str: The header string containing the book name, chapter number, and verse number.
    """

    # Step 14b: Define a regex pattern to match the header.
    pattern = r"(\w+\s+\d+:\d+)"

    # Step 14c: Search for the pattern in the input text.
    match = re.search(pattern, input_text)

    # Step 14d: Check if a match is found in the input text using the defined regex pattern.
    if match:
        # If a match is found,
        # return the header string without leading/trailing whitespace and line breaks.
        header = match.group(1).strip()
# BREAKPOINT

        # If a match is found, return the header string.
        return header
    else:
        # If no match is found, raise a ValueError.
        raise ValueError("Invalid header format")

# =============================================================================
# STEP 15: Read and process the input file and save the output to Excel
# =============================================================================

# Step 15a: Define 'main()' function


def main():
    """
    Main function that reads the input file,
    processes it, and saves the output to an Excel file.
    """

    # Step 15b: Prompt the user to enter the input and output file paths
    input_file = input("Enter path for input file: ").strip()
    output_file = input("Enter path for output file: ").strip()

    # Step 15c: Read the input text file.
    input_text = read_input_file(input_file)

    # Step 15d: Extract the textual variants and witness abbreviations.
    extracted_data = process_input_file(input_file)

    # Step 15e: Create a DataFrame using the header and extracted data.
    data_frame = identify_and_assign(extracted_data)

    # Step 15g: Write the output DataFrame to a CSV file.
    write_output_file(data_frame, output_file)

    # Step 15h:
    print(f"Data has been successfully extracted and saved to {output_file}")

# Step 15i:


if __name__ == '__main__':
    main()


# =============================================================================
# END OF CODE
# =============================================================================
