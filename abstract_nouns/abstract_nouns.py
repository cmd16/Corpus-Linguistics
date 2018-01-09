"""
Abstract Nouns
Written by Catherine DeJager

Get the abstract nouns in a corpus by searching for various word endings as found in the website below.
    https://learningenglishgrammar.wordpress.com/suffixes/suffixes-and-how-they-form-abstract-nouns/
Preconditions: infilename refers to a .txt file containing a word list created from AntConc
"""

infilename = input("Infilename: ")
infile = open(infilename,'r')

abstract_noun_list = ["ion", "ions", "ity", "itys", "ness", "nesses", "dom", "doms", "ment", "ments"
                      "age", "ance", "ence", "ce", "cy", "ess", "esse", "head", "hood", "ice", "ise", "ism",
                      "ry", "tude", "ty", "ure"]

linenum = 0
for line in infile:
    if linenum < 3:  # first 3 lines contain metadata
        continue
    data = str(line).split()

    linenum += 1
