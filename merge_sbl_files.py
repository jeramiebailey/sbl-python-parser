"""
This script copies the text from the folder /sbl_parser/SBLGNT-master/data/sblgntapp/text/
and pastes it into a single file in /sbl_parser/merged_sbl.txt
"""

# -- coding: utf-8 --

# =============================================================================
# STEP 1:
#    Initialize script
# =============================================================================


# Step 1a: Import necessary libraries

import os

# =============================================================================
# STEP 2:
#    Establish file paths
# =============================================================================

# Step 2a: Prompt the user to enter the input directory and output file paths

input_directory = input("Enter path for input directory: ").strip()
output_file = input("Enter path for output file: ").strip()


# =============================================================================
# STEP 3:
#    Name files
# =============================================================================

# Step 2a: List file names in canonical order

file_names = [
    "Matt.txt",
    "Mark.txt",
    "Luke.txt",
    "John.txt",
    "Acts.txt",
    "Rom.txt",
    "1Cor.txt",
    "2Cor.txt",
    "Gal.txt",
    "Eph.txt",
    "Phil.txt",
    "Col.txt",
    "1Thess.txt",
    "2Thess.txt",
    "1Tim.txt",
    "2Tim.txt",
    "Titus.txt",
    "Phlm.txt",
    "Heb.txt",
    "Jas.txt",
    "1Pet.txt",
    "2Pet.txt",
    "1John.txt",
    "2John.txt",
    "3John.txt",
    "Jude.txt",
    "Rev.txt",
]

# =============================================================================
# STEP 3:
#    Merge files
# =============================================================================

# Step 3a: Define 'merge_sbl_files()' function

def merge_sbl_files(input_directory, output_file):

    # Step 3b: Create output file

    output_file = "merged_sbl.txt"

    # Step 3c: Copy & paste

    with open(output_file, "w", encoding="utf-8") as output:
        for index, file_name in enumerate(file_names):
            file_path = os.path.join(input_directory, file_name)
            with open(file_path, "r", encoding="utf-8") as input_file:

                # Skip the first line (Greek book title)
                input_file.readline()

                # Read the next line and remove leading/trailing whitespaces
                next_line = input_file.readline().strip()

                # Write the next line without adding a newline character
                output.write(next_line)
                content = input_file.read()

                # Check if it's the last file
                if index == len(file_names) - 1:

                    # Remove trailing spaces from the last line of the last file
                    content = content.rstrip()

                output.write(content)

                # Add a single newline character at the end of each book
                output.write("\n")

# Step 3d: Call the 'merge_sbl_files() function

if __name__ == "__main__":
    merge_sbl_files(input_directory, output_file)
