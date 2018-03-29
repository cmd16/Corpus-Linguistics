"""
Abstract Nouns
Written by Catherine DeJager

Get the abstract nouns in a corpus by searching for various suffixes as found in the website below.
    https://learningenglishgrammar.wordpress.com/suffixes/suffixes-and-how-they-form-abstract-nouns/
Dependencies: openpyxl (if you want to output results to spreadsheet)
"""

# imports
import openpyxl
import os

# global variables
test = True
suffix_list = ['ance', 'ances', 'cy', 'cies', 'dom', 'doms', 'ence', 'ences', 'ness',
               'nesses', 'esses', 'hood', 'hoods', 'ice', 'ices', 'ion', 'ions', 'ism',
               'isms', 'ity', 'itys', 'ment', 'ments', 'ty', 'ties', 'tude', 'tudes', 'ure', 'ures']


# function definitions
def get_abstract_nouns_from_wordlist(infile):
    """
    Returns a dictionary of abstract nouns, with a separate entry for each suffix.
    :param infile: a .txt file containing a word list created from AntConc
    :return: a dictionary of abstract nouns, with a separate entry for each suffix.
    """
    abstract_noun_dict = {suffix: [] for suffix in suffix_list}  # each suffix has a blank array (for word and frequency)
    linenum = 0
    for line in infile:
        if linenum < 3:  # first 3 lines contain metadata
            linenum += 1
            continue
        data = str(line).split()
        word = data[2]
        frequency = int(data[1])
        for idx in range(len(suffix_list)):
            suffix = suffix_list[idx]
            if word.endswith(suffix):
                abstract_noun_dict[suffix].append((word, frequency))
                break
        linenum += 1
    infile.close()
    return abstract_noun_dict


def get_abstract_nouns_from_txt(infile):
    """
    Returns a dictionary of abstract nouns, with a separate entry for each suffix.
    Note: this seems to work but doesn't pass my current tests, so use at your own risk.
    :param infile: a .txt file with words in it.
    :return: a dictionary of abstract nouns, with a separate entry for each suffix.
    """
    """Returns a dictionary of abstract nouns, with a separate entry for each suffix.
    Preconditions: infile refers to a .txt file with words in it."""
    # TODO: CHANGE THIS LATER TO USE MULTIDIMENSIONAL ARRAY FOR WORDS

    abstract_noun_dict = {suffix: {} for suffix in suffix_list}  # each suffix has a blank dictionary (for word and frequency)
    for line in infile:
        words = str(line).split()
        for word in words:
            for suffix in suffix_list:
                if word.endswith(suffix):
                    if word in abstract_noun_dict[suffix]:
                        abstract_noun_dict[suffix][word] += 1
                    else:
                        abstract_noun_dict[suffix][word] = 1
                    break
    infile.close()
    return abstract_noun_dict


def print_abstract_nouns(aDict):
    """
    Prints out the abstract nouns in a dictionary, formatted nicely.
    :param aDict: a dictionary created by running get_abstract_nouns
    :return:
    """
    for suffix in aDict:
        print(suffix, "words:")
        for word in aDict[suffix]:
            print(word, aDict[suffix][word])  # print word and frequency
        print()  # new line for spacing


def store_spreadsheet(aDict, filename="Abstract Nouns Spreadsheet"):
    """
    Stores the abstract nouns and their frequencies in a spreadsheet.
    :param aDict: a dictionary created by running get_abstract_nouns
    :param filename: the name of the spreadsheet to store the results in
    :return:
    """
    wb = openpyxl.Workbook()
    ws = wb.active  # get a handle to the sheet in the workbook

    ws['A1'] = "Abstract Nouns Spreadsheet"
    for col in range(1, len(suffix_list) * 2 + 1, 2):  # go up by two because the suffixes need to be separated. add one because indexing starts at 1 in openpyxl
        suffix = suffix_list[(col - 1) // 2]
        current_suffix_entry = aDict[suffix]
        ws.cell(row=2, column=col).value = "-" + suffix
        for row in range(3, len(current_suffix_entry) + 3):  # this number is equal to the number of unique words with that suffix
            idx = row - 3
            word = current_suffix_entry[idx][0]
            ws.cell(row=row, column=col).value = word
            ws.cell(row=row, column=col+1).value = current_suffix_entry[idx][1]  # store the frequency
    if not filename.endswith(".xlsx"):
        wb.save(filename + ".xlsx")  # add the type extension if not included
    else:
        wb.save(filename)


def sort_abstract_nouns(aDict, sort_key='frequencyhi'):
    """
    Sort (in place) a dictionary that was constructed using get_abstract_nouns
    :param aDict: a dictionary constructed using get_abstract_nouns
    :param sort_key: a string representing which way to sort the words/frequencies
    :return:
    """
    if sort_key == "frequencyhi":
        for suffix in suffix_list:
           aDict[suffix].sort(key=lambda x: x[1], reverse=True)
    elif sort_key == "frequencylo":
        for suffix in suffix_list:
            aDict[suffix].sort(key=lambda x: x[1])
    elif sort_key == "alphalo":
        for suffix in suffix_list:
           aDict[suffix].sort()
    elif sort_key == "alphahi":
        for suffix in suffix_list:
           aDict[suffix].sort(reverse=True)
    elif sort_key == "alphawordendlo":
        raise NotImplementedError
    elif sort_key == "alphawordendhi":
        raise NotImplementedError
    else:
        print('Sorting type invalid. Try again with "frequencyhi" (high to low), "frequencylo" (low to high), "alphahi", "alphalo", '
              '"alphawordendlo", or "alphawordendhi"')


def abstract_nouns_store_count(aDict, outfilename, num=10):
    total_types = 0
    total_tokens = 0
    count_dict = {suffix: [] for suffix in suffix_list}  # suffix: [types, tokens, [top_num]]
    for suffix in suffix_list:
        entry = aDict[suffix]
        types = len(entry)
        total_types += types
        count_dict[suffix].append(types)
        tokens = 0
        for freq_tup in entry:
            tokens += freq_tup[1]
        total_tokens += tokens
        count_dict[suffix].append(tokens)
        count_dict[suffix].append(entry[0:num+1])
    f_out = open(outfilename, "w")
    f_out.write("# Word types: %d\n" % total_types)
    f_out.write("# Word tokens: %d\n" % total_tokens)
    for suffix in suffix_list:
        count_entry = count_dict[suffix]
        f_out.write("# %s types: %d\n" % (suffix, count_entry[0]))
        f_out.write("# %s tokens: %d\n" % (suffix, count_entry[1]))
        for freq_tup in count_entry[2]:
            f_out.write("%s:\t%d\n" %(freq_tup[0], freq_tup[1]))
    f_out.close()


def walk_dir_abstract_nouns_spreadsheet(path, sort_key="frequencyhi", keyword="_antconc"):
    """
    Walks through a directory and makes a spreadsheet of abstract nouns for each file in the directory.
    Preconditions: _antconc is in the filename of each wordlist file
    :param path: the path to a directory containing- AntConc wordlists and/or folders containing AntConc wordlists
    :return:
    """
    for item in os.walk(path):
        print(item)
        os.chdir(item[0])  # change to the directory you are looking at. useful for reading and writing files
        for filename in item[2]:
            if filename.endswith(".txt") and keyword in filename:
                this_dict = get_abstract_nouns_from_wordlist(open(filename))
                sort_abstract_nouns(this_dict, sort_key)
                store_spreadsheet(this_dict, filename[:filename.index(".txt")] + "_abstract_nouns")


def walk_dir_count_abstract_nouns(path, out_dir, sort_key="frequencyhi", keyword="_python"):
    for item in os.walk(path):
        os.chdir(item[0])  # change to the directory you are looking at. useful for reading and writing files
        for filename in item[2]:
            if filename.endswith(".txt"):
                print(filename)
                this_dict = get_abstract_nouns_from_wordlist(open(filename))
                sort_abstract_nouns(this_dict, sort_key)
                abstract_nouns_store_count(this_dict, os.path.join(out_dir, filename[:filename.index(keyword)] + "_abstract nouns_python.txt"))


def main():
    this_dict = get_abstract_nouns_from_wordlist(open(input("Name of the file containing the wordlist: ")))
    sort_type = input('Sort words by "frequencyhi" (high to low), "frequencylo" (low to high), "alpha", "reversealpha", '
        '"alphawordend", or "reversealphawordend": ')
    sort_abstract_nouns(this_dict, sort_type)
    store_spreadsheet(this_dict, input("Name of spreadsheet to store results in: "))

# test code
if test:
    proj_dir = "/Volumes/2TB/Final_Project"
    wordlist_dir = os.path.join(proj_dir, "wordlists")
    walk_dir_count_abstract_nouns(wordlist_dir, os.path.join(proj_dir, "Abstract Nouns"))
    # test_dict = get_abstract_nouns_from_wordlist(open("hist152_final_wordend.txt"))
    # sort_abstract_nouns(test_dict, "frequencyhi")
    # store_spreadsheet(test_dict, "test_spreadsheet.xlsx")
    # test_dict2 = get_abstract_nouns_from_txt(open("HIST152_academicessay_Dec1616_Final.txt"))
    # assert test_dict == test_dict2
    # store_spreadsheet(test_dict2, "test_spreadsheet2.xlsx")


# main code
# main()
