"""
Abstract Nouns
Written by Catherine DeJager

Get the abstract nouns in a corpus by searching for various suffixes as found in the website below.
    https://learningenglishgrammar.wordpress.com/suffixes/suffixes-and-how-they-form-abstract-nouns/
"""

"""
infilename = input("Infilename: ")
infile = open(infilename,'r')
"""

# function definitions

def get_abstract_nouns(infile=open(input("Infilename: "))):
    """Returns a dictionary of abstract nouns, with a separate entry for each suffix.
    Preconditions: infile refers to a .txt file containing a word list created from AntConc"""
    abstract_noun_list = ["ion", "ions", "ity", "itys", "ness", "nesses", "dom", "doms", "ment", "ments", "age", "ance",
                          "ence", "ce", "cy", "ess", "esse", "head", "hood", "ice", "ise", "ism", "ry", "tude", "ty", "ure"]
    abstract_noun_dict = {suffix: {} for suffix in abstract_noun_list} # each suffix has a blank dictionary (for word and frequency)
    linenum = 0
    for line in infile:
        if linenum < 3:  # first 3 lines contain metadata
            linenum += 1
            continue
        data = str(line).split()
        word = data[2]
        frequency = data[1]
        for suffix in abstract_noun_list:
            if word.endswith(suffix):
                if word in abstract_noun_dict[suffix]:  # if an entry exists for this word
                    abstract_noun_dict[suffix][word] += 1  # increase the count
                else:
                    abstract_noun_dict[suffix][word] = 1  # create an entry
        linenum += 1
    infile.close()
    return abstract_noun_dict

