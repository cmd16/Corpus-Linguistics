"""
Abstract Nouns
Written by Catherine DeJager

Get the abstract nouns in a corpus by searching for various suffixes as found in the website below.
Dependencies: openpyxl (if you want to output results to spreadsheet
    https://learningenglishgrammar.wordpress.com/suffixes/suffixes-and-how-they-form-abstract-nouns/
"""

# imports
import openpyxl

# global variables
test = False
suffix_list = ['age', 'ages', 'ance', 'ances', 'ce', 'ces', 'cy', 'cies', 'dom', 'doms', 'ence', 'ences', 'ess', 'esses',
               'esse', 'esses', 'head', 'heads', 'hood', 'hoods', 'ice', 'ices', 'ion', 'ions', 'ise', 'ises', 'ism',
               'isms', 'ity', 'itys', 'ment', 'ments', 'ry', 'ries', 'ty', 'ties', 'tude', 'tudes', 'ure', 'ures']


# function definitions
def get_abstract_nouns_from_wordlist(infile):
    """Returns a dictionary of abstract nouns, with a separate entry for each suffix.
    Preconditions: infile refers to a .txt file containing a word list created from AntConc"""
    abstract_noun_dict = {suffix: [] for suffix in suffix_list} # each suffix has a blank array (for word and frequency)
    linenum = 0
    for line in infile:
        if linenum < 3:  # first 3 lines contain metadata
            linenum += 1
            continue
        data = str(line).split()
        word = data[2]
        frequency = data[1]
        for idx in range(len(suffix_list)):
            suffix = suffix_list[idx]
            if word.endswith(suffix):
                print(data)
                abstract_noun_dict[suffix].append([word, data[1]])
                break
        linenum += 1
    infile.close()
    return abstract_noun_dict


def get_abstract_nouns_from_txt(infile):
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
    """Prints out the abstract nouns in a dictionary, formatted nicely.
    Preconditions: aDict is a dictionary created by running get_abstract_nouns"""
    for suffix in aDict:
        print(suffix, "words:")
        for word in aDict[suffix]:
            print(word, aDict[suffix][word])  # print word and frequency
        print()  # new line for spacing


def store_spreadsheet(aDict, filename="Abstract Nouns Spreadsheet"):
    """Stores the abstract nouns and their frequencies in a spreadsheet.
    Preconditions: aDict is a dictionary created by running get_abstract_nouns."""
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


def sort_abstract_nouns(aDict, type='frequency'):
    if type == "frequency":
        for suffix in suffix_list:
           aDict[suffix].sort(key=lambda x: x[1])
    elif type == "reversefrequency":
        for suffix in suffix_list:
           aDict[suffix].sort(key=lambda x: x[1], reverse=True)
    elif type == "alpha":
        for suffix in suffix_list:
           aDict[suffix].sort()
    elif type == "reversealpha":
        for suffix in suffix_list:
           aDict[suffix].sort(reverse=True)
    elif type == "alphawordend":
        pass  # the list is sorted this way by default
    elif type == "reversealphawordend":
        for suffix in suffix_list:
           aDict[suffix].reverse()



# test code
if test:
    test_dict = get_abstract_nouns_from_wordlist(open("hist152_final_wordend.txt"))
    store_spreadsheet(test_dict, "test_spreadsheet.xlsx")
    test_dict2 = get_abstract_nouns_from_txt(open("HIST152_academicessay_Dec1616_Final.txt"))
    # assert test_dict == test_dict2
    store_spreadsheet(test_dict2, "test_spreadsheet2.xlsx")

# main code
this_dict = get_abstract_nouns_from_wordlist(open(input("Name of the file containing the wordlist: ")))
store_spreadsheet(this_dict, input("Name of spreadsheet to store results in: "))
