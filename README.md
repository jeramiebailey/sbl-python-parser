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

The first verse in the input file is listed as follows:

"Matthew 1:5
1:5 Βόες … Βόες WH NA28 ] Βοὸς … Βοὸς Treg; Βοὸζ … Βοὸζ RP
• Ἰωβὴδ … Ἰωβὴδ WH Treg NA28 ] Ὠβὴδ … Ὠβὴδ RP"

Here is an example of how the script should break down this data:

Group 1. (the first line marked by "1:5")
    Textual variant 1.
        "Βόες … Βόες"
            Occurrences of the textual variant in each witness:
                1. WH
                2. NA28
    DELIMITER: " ] "
    Textual variant 2.
        "Βοὸς … Βοὸς"
            Occurrences of the textual variant in each witness:
                3. Treg
    DELIMITER: "; "
    Textual variant 3.
        Βοὸζ … Βοὸζ
            Occurrences of the textual variant in each witness:
                4. RP
Group 2. (the second line marked by "•")
    Textual variant 4.
        Ἰωβὴδ … Ἰωβὴδ
            Occurrences of the textual variant in each witness:
                5. WH
                6. Treg
                7. NA28
    DELIMITER: " ] "
    Textual variant 5.
        Ὠβὴδ … Ὠβὴδ
            Occurrences of the textual variant in each witness:
                8. RP

=============================================================================

The module converts this list of Bible verses and their "textual variants"
into an excel spreadsheet with the following columns:

A. 'record_number': an integer reflecting the total number of rows in the output file
(not counting the column headings).
This counts the number of database records generated by the script
and serves as a perpetual counter that doesn't reset at any point in the procedure.

B. 'book_name': the name of the book of the Bible being parsed.
Here is a list of all 27 book names used in the input file:

1.    Matthew
2.    Mark
3.    Luke
4.    John
5.    Acts
6.    Romans
7.    1 Corinthians
8.    2 Corinthians
9.    Galatians
10.    Ephesians
11.    Philippians
12.    Colossians
13.    1 Thessalonians
14.    2 Thessalonians
15.    1 Timothy
16.    2 Timothy
17.    Titus
18.    Philemon
19.    Hebrews
20.    James
21.    1 Peter
22.    2 Peter
23.    1 John
24.    2 John
25.    3 John
26.    Jude
27.    Revelation

C. 'chapter_number': an integer representing the chapter number of the verse being parsed.

D. 'verse_number': an integer representing the verse number of the verse being parsed.

E. textual_variants: the Greek text of the verse being parsed and its textual variants,
with each textual variant separated by a semicolon and a space (with some exceptions).

F. witness_abbreviations | the abbreviation for each Bible version
that serves as a "witness" to specific "textual variants" listed in the textual apparatus.
There are only 5 "witnesses" abbreviated in the SBL textual apparatus:
“WH”, “NA28”, “RP”, “Treg”, "NIV"

These abbreviations stand for 4 different Bible versions,
most of which are critical editions of the Greek New Testament:
1. “WH” (Westcott and Hort)
2. “NA28” (Nestle-Aland 28)
3. “RP” (Robinson-Pierpont)
4. “Treg” (Tregelles)
5. "NIV" (New International Version)

G. group_number: an integer representing the group number of each textual variant in a given verse.
Each line under a Bible verse heading (i.e. "Matthew 1:5") has one or more "groups,"
which are "groups" of mutually exclusive "textual variants".
Since these "groups" of "textual variants" can occur in multiple locations,
the "groups" of "textual variants" for each verse
are listed in separate lines/"groups" of the input file.

H. variant_number: an integer representing the number of each textual variant in a given verse.
This column keeps track of the total number of "textual variants" in each verse.
The script incriments this variable for each "textual variant"
until it moves on to the next verse, where the variable resets to 1

I. occurrence_number: an integer representing the number of times a "textual variant" OCCURS
in each "witness", according to the textual apparatus.
Since each "textual variant" can "occur" in up to 4 of the witnesses ("WH", "NA28", "RP", "Treg"),
each combination of a "textual variant" and a "witness" abbreviation is an "occurrence".

Each "occurrence" needs to be listed on its own line/row of the output file in excel,
since each "occurrence" will make up a single record in the database.
This "occurrence_number" variable will effectively count the total number
of "witness" abbreviations associated with each textual variant within a verse.
The variable should only reset when the script moves on to the next verse.

=============================================================================

If there are two or more “textual variants” listed in a single line (“group”),
the first “textual variant” and its “witness” abbreviation(s) are preceded
by a square bracket with spaces on either side (“ ] “)
and the subsequent “textual variants” and their “witness” abbreviation(s) are separated
by semicolons with no space on the left and a single space on the right (“; “).

There are two standard delimiters:

(1) (“ ] ”) - with a space on either side
(2) (“; ”) - with a space on the right only

These delimiters are always preceded by at least one witness abbreviation,
so the symbol by itself never stands alone as a delimiter without additional context.

Here are all the possible combinations of "witness" abbreviation + delimiter:

- “WH ] ”
- "WH; “
- “NA28 ] "
- “NA28; ”
- “RP ] ”
- “RP; ”
- “RP ] “
- “RP; “
- “Treg ] ”
- “Treg; “
- “NIV ] ”
- “NIV; “

=============================================================================

The script must account for that fact that the semicolon with a space to the right (“; ”)
is also the Greek question mark (?).
In those instances, where “; ” is a Greek question mark embedded in the textual variant,
the semicolons are NOT preceded by "witness" abbreviations.

For example:

“Matthew 11:9
9 ; προφήτην ἰδεῖν WH ] ἰδεῖν; προφήτην Treg NA28 RP”

The first semicolon after Matthew 11:9 is a question mark
that indicates that the first textual variant (in WH) omits the term “ἰδεῖν”,
which is obvious because the semicolon is not preceded by any “witness” abbreviation,
neither in the first “textual variant” nor in the second.

=============================================================================

Note that some “textual variants” are preceded by a plus sign (“+ “) with a trailing space
to indicate that the variant is included in the “witness(es)” cited,
implying that the variant is omitted from other “witnesses”.
For the purpose of the script, the plus sign ("+ ") should be included
as part of the “textual variant” within the cell.

Note that, in contrast to the use of the plus sign with a space ("+ "),
some “textual variants” are listed merely as an en dash (“– “) with spaces on either side
to indicate that the variant is omitted from the “witness(es)” cited,
implying that the variant is added to the other “witnesses”.
For the purpose of the script, the en dash ("– ") should be included
as the “textual variant” within the cell.

For example, observe the second “textual variant” listed for Mathew 1:18 -

Matthew 1:18
18 Ἰησοῦ WH NA28 RP ] – Treg
• γένεσις WH Treg NA28 ] γέννησις RP
• μνηστευθείσης WH Treg NA28 ] + γὰρ RP

Here, in group 1, the script should recognize “ RP ] ” followed by the en dash with a space ("– "),
which represents the omission of the textual variant to the left of the delimiter ("Ἰησοῦ")

Conversely, in group 3, the script should recognize “ NA28 ] ”
followed by the plus sign with a space ("+ "),
which is included as part of the beginning of the textual variant, i.e. “+ ὁ βασιλεὺς”.

=============================================================================

For subsequent verses within the same chapter,
the first “group” (first row) of “textual variants” under each verse heading
is preceded by the verse number along, without the chapter number (i.e., “6” under Matthew 1:6).
So, whenever the script comes across a new verse
with multiple “groups” of “textual variants” (multiple lines under the verse heading),
it should be able to account for this predictable convention based on where it is within a chapter.

For example, when it starts with “Matthew 1:5”,
it should expect the first “group” of “textual variants” to be listed right after “1:5”.
And when it comes across the next verse, Matthew 1:6,
it should expect the first variant to be listed right after the number “6”.

Subsequent lines (“groups”) under the same verse heading are all preceded by a dot (•),
rather than repeating the chapter:verse (for the initial verse in a chapter)
or the verse number (for subsequent verses).

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