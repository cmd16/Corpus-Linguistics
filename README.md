# Corpus-Linguistics
A repository to store the scripts I write to make corpus linguistics (analyzing bodies of texts) work easier.

POS Spreadsheet
This allows you to:
    Create a dictionary that maps each part of speech (POS) to a dictionary containing words with that POS with their frequency,
        with a separate entry for each POS.
    Sort that dictionary by frequency or by words in alphabetical order
    Store that dictionary in a spreadsheet
Dependencies:
    openpyxl
    you need to have tagged txt files to use

abstract_nouns
This allows you to:
    Get the abstract nouns in a corpus by searching for various suffixes as found in the following website:
        https://learningenglishgrammar.wordpress.com/suffixes/suffixes-and-how-they-form-abstract-nouns/
    Sort that dictionary by frequency or by words in alphabetical order
    Store that dictionary in a spreadsheet
Dependencies:
    openpyxl
    you need wordlist files created using AntConc (http://www.laurenceanthony.net/software/antconc/)
Note:
    I have done nothing to correct for false positives. 
    If you find false positives, please let me know on the issues page, and I'll make a list of false positives.

remove_html_tags
This allows you to:
    Remove all html tags from a file (e.g., <p>paragraph</p> becomes paragraph)
