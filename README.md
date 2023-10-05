This Python module parses an input text file (merged_sbl.txt),
which is a 'textual apparatus' of the New Testament from the Society of Biblical Literature.

The textual apparatus consists of footnotes to Bible verses that present the following data:
1. "textual variants" (alternate readings of verses)
2. "witnesses" (abbreviations for Bible versions that feature each "textual variant")

The script should break down the data from the textual apparatus
into multiple lines in the output file,
including "occurrences" (individual records of the output file) of each "textual variant"
with its associated "witness" abbreviation,
organized by the location in the Bible (book, chapter, verse).

A "textual variant" is an alternative reading within each verse.

For example, one version (a "witness") of the New Testament might say this:
"And Jesus walked..." (in Greek)

While another, conflicting "witness" might something else:
"Jesus ran..." (in Greek).

A Textual Apparatus could break up these "textual variants" into 2 "groups":
Group 1.
    Textual variant 1.
        "+ and" (the addition of the word "and")
    Textual variant 2.
        "–" (the omission of the word "and")
Group 2.
    Textual variant 1.
        "walk"
    Textual variant 2.
        "ran"

Alternatively, a textual apparatus could treat this as a single "group" of "textual variants":
Group 1.
    Textual variant 1.
        "And Jesus walked"
    Textual variant 2.
        "Jesus ran"


=============================================================================

Here is a sample of what the output should look like
for these first 2 verses:

| record_number | book_name | chapter_number | verse_number | variant_text  | witness_abbreviation | group_number | variant_number | occurrence_number |
|---------------|-----------|----------------|--------------|---------------|----------------------|--------------|----------------|-------------------|
| 1             | Matthew   | 1              | 5            | Βόες … Βόες   | WH                   | 1            | 1              | 1                 |
| 2             | Matthew   | 1              | 5            | Βόες … Βόες   | NA28                 | 1            | 1              | 2                 |
| 3             | Matthew   | 1              | 5            | Βοὸς … Βοὸς   | Treg                 | 1            | 2              | 3                 |
| 4             | Matthew   | 1              | 5            | Βοὸζ … Βοὸζ   | RP                   | 1            | 3              | 4                 |
| 5             | Matthew   | 1              | 5            | Ἰωβὴδ … Ἰωβὴδ | WH                   | 2            | 4              | 5                 |
| 6             | Matthew   | 1              | 5            | Ἰωβὴδ … Ἰωβὴδ | Treg                 | 2            | 4              | 6                 |
| 7             | Matthew   | 1              | 5            | Ἰωβὴδ … Ἰωβὴδ | NA28                 | 2            | 4              | 7                 |
| 8             | Matthew   | 1              | 5            | Ὠβὴδ … Ὠβὴδ   | RP                   | 2            | 5              | 8                 |
| 9             | Matthew   | 1              | 6            | δὲ            | WH                   | 1            | 1              | 1                 |
| 10            | Matthew   | 1              | 6            | δὲ            | Treg                 | 1            | 1              | 2                 |
| 11            | Matthew   | 1              | 6            | δὲ            | NA28                 | 1            | 1              | 3                 |
| 12            | Matthew   | 1              | 6            | + ὁ βασιλεὺς  | RP                   | 1            | 2              | 4                 |


=============================================================================