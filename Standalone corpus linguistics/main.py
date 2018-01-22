import nltk
import pprint   # For proper print of sequences.
import treetaggerwrapper
import operator
import csv
import openpyxl
import os
import math
import re

#1) build a TreeTagger wrapper:
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
tree_taglist = ["CC", "CD", "DT", "EX", "FW", 'IN', 'IN/that', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NP', 'NPS', 'PDT', 'POS',
            'PP', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SENT', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP',
            'VH', 'VHD', 'VHG', 'VHN', 'VHZ', 'VHP', 'VV', 'VVD', 'VVG', 'VVN',
            'VVP', 'VVZ', 'WDT', 'WP', 'WP$', 'WRB', ':', '$', ',', '(', ')', "''", "NONE"]  # removed VD tags and "``"
tree_tagdefs = {"CC": "coordinating conjuction", "CD": "cardinal number", "DT": "determiner", "EX": "existential there",
                   "FW":"foreign word", 'IN':"preposition/subord. conj", 'IN/that':"complementizer", 'JJ':"adjective",
                   'JJR': "adjective, comparative", 'JJS': "adjective, superlative", 'LS': "list marker", 'MD': "modal",
                   'NN': "noun, singular or mass", 'NNS': "noun, plural", 'NP': "proper noun, singular", 'NPS': "proper noun, plural",
                'PDT':"predeterminer", 'POS':"possessive ending", 'PP':"personal pronoun", 'PP$':"possesive pronoun",
                'RB': "adverb", 'RBR':"adverb, comparative", 'RBS':"adverb, superlative", 'RP':"particle", 'SENT':"end punctuation",
                'SYM': "symbol", 'TO': "to", 'UH':"interjection", 'VB':"be", 'VBD':"was/were", 'VBG':"being", 'VBN':"been",
                'VBZ':"is", 'VBP':"am/are", 'VH':"have, base form", 'VHD':"had", 'VHG':"having", 'VHN':"had", 'VHZ':"has",
                'VHP':"have, present non-3rd person", # removed VD tags
                'VV':"verb, base form", 'VVD':"verb, past tense", 'VVG': "verb, gerund/participle", 'VVN': "verb, past participle",
                'VVP': "verb, present non-3rd person", 'VVZ': "verb, present 3rd person singular", 'WDT': "wh-determiner",
                'WP': "wh-pronoun", 'WP$': "possessive wh-pronoun", 'WRB': "wh-adverb", ':' : "general joiner",
                '$': "currency symbol", ',':",", '(':"(", ')':")", "''":"quotation marks", "NONE": "miscellaneous"}

# TODO: MODIFY THE CALL TO TAGFILE
def tag_directory(in_dir, out_dir, walk=False, restart="", end=""):
    """
    Tag the files in a directory specified by in_dir and store them in a directory specified by out_dir
    :param in_dir: the directory to read files from
    :param out_dir: the directory to write files to
    :param walk: if True, walk through the subdirectories
    :param restart: the first file to tag (skips all others)
    :return:
    """
    original_dir = os.getcwd()
    try:
        os.chdir(in_dir)
    except FileNotFoundError:
        os.mkdir(in_dir)
        os.chdir(in_dir)
    current = os.getcwd()
    namelist = []
    if restart:
        found = False
    else:
        found = True
    for name in os.listdir(current)[1:]:
        if name == restart:
            found = True
        if found:
            namelist.append(name)
    for filename in namelist:
        if filename == end:
            print(filename, end)
            break
        print("tag_directory processing", filename)
        try:
            tagger.tag_file_to(filename, os.path.join(out_dir, filename[:len(filename)-4] + "_tagged.txt"))
        except FileNotFoundError:
            os.mkdir(out_dir)
            tagger.tag_file_to(filename, os.path.join(out_dir, filename[:len(filename) - 4] + "_tagged.txt"))
        except treetaggerwrapper.TreeTaggerError:  # most common error seems to be html tags
            print("removing html tags in", filename, "due to TreeTaggerError")
            with open(filename) as file:
                with open("temp.txt", 'w') as tempfile:
                    line1 = next(file)
                    if "@page" not in line1:
                        tempfile.write(line1)
                    body = file.read()
                    body = re.sub("<.*?>", "", body)
                    tempfile.write(body)
            os.replace("temp.txt", filename)
            tagger.tag_file_to(filename, os.path.join(out_dir, filename[:len(filename)-4] + "_tagged.txt"))
            print("tagged file after removing html")
    os.chdir(original_dir)  # change back in case later methods need to be in this directory


def tag_lemma_from_tree(in_name, case_sensitive=False):
    """
    Returns a dictionary that maps each part of speech (POS) to a dictionary containing words with that POS with their frequency,
    with a separate entry for each POS.
    :param in_name: the name of a .txt file created using or a list of filenames of txt files that contain tagged words
    :param case_sensitive: if true, "The" is a different word from "the"
    :return: a tuple containing 0) a dictionary that maps each part of speech (POS) to a dictionary containing words with that POS with their frequency,
    with a separate entry for each POS 1) a dictionary that maps each lemma to its frequency
    """
    if type(in_name) == list:
        iterator = iter(in_name)
    else:
        iterator = iter([in_name])
    tag_dict = {tag: {} for tag in tree_taglist}
    lemma_dict = {}
    for infilename in iterator:
        infile = open(infilename)
        print("tag_lemma_from_tree processing " + infilename, end="... ")
        for line in infile:
            data = line.split()  # get a list containing word, tag, lemma
            word = data[0]
            if not case_sensitive:
                word = word.lower()
            try:
                pos = data[1]
                if pos == "``":
                    pos = "''"
                if case_sensitive:
                    lemma = data[2]
                else:
                    lemma = data[2].lower()
            except IndexError:
                if word.startswith("<"):
                    continue  # e.g., <repdns text="nosuey.Beta" />
                else:
                    print(line, data, sep=" : ")
                    word = input("enter word: ")
                    pos = input("enter pos: ")
                    lemma = input("enter lemma: ")
            try:
                entry = tag_dict[pos]
            except KeyError:
                if word == "#":
                    pos = "SYM"
                elif word.startswith("<rep"):  # skip replaced dns
                    continue
                else:
                    # pos = input("{" + word + "} " + line + " not in dictionary. Please enter a valid tag: ")
                    pos = "NONE"
                entry = tag_dict[pos]
            if word in entry:
                entry[word] += 1
            else:
                entry[word] = 1
            if lemma in lemma_dict:
                lemma_dict[lemma] += 1
            else:
                lemma_dict[lemma] = 1
        print("done")
    print("dictionaries complete")
    return tag_dict, lemma_dict


def tag_lemma_from_tree_directory(path, end="_tagged.txt", case_sensitive=False, walk=False):
    """
    Make a dictionary that maps each part of speech (POS) to a dictionary containing words with that POS with their frequency,
    with a separate entry for each POS.
    :param path: the path to the directory you want to look at. Note: this will aggregate data across all the files. If you want individual
    dictionaries for each file, call tag_lemma_from_tree on each file.
    :param end: the filename ending that signifies a tagged file.
    :param case_sensitive: if true, "The" is a different word from "the"
    :param walk: if True, the function "walks" the directory - it goes into subfolders
    :return: a tuple containing 0) a dictionary that maps each part of speech (POS) to a dictionary containing words with that POS with their frequency,
    with a separate entry for each POS 1) a dictionary that maps each lemma to its frequency
    """
    currentdir = os.getcwd()
    filename_list = []
    if walk:
        for item in os.walk(path):
            print(item)
            currentpath = item[0]
            os.chdir(currentpath)  # change to the directory you are looking at. useful for reading and writing files
            for filename in item[2]:
                if filename.endswith(end):
                    filename_list.append(os.path.join(currentpath, filename))
    else:
        for filename in os.listdir(path):
            if filename.endswith("_tagged.txt"):
                filename_list.append(os.path.join(path, filename))
    os.chdir(currentdir)
    return tag_lemma_from_tree(filename_list, case_sensitive=case_sensitive)


def store_taglemma_results(tag_lemma, filename="Parts of Speech Spreadsheet", sort="frequencyhi"):
    """
    Store the various parts of speech and their frequencies, as well as lemmas and their frequencies, in a spreadsheet
    :param tag_lemma: a tuple containing 0) a dictionary that maps each part of speech (POS) to a dictionary containing words with that POS with their frequency,
    with a separate entry for each POS 1) a dictionary that maps each lemma to its frequency [the return value of tag_lemma_from_tree]
    :param filename: the name of the spreadsheet to store the results in
    :param sort: indicates order the entries should be sorted in
    :return:
    """
    tag_dict = tag_lemma[0]
    lemma_dict = tag_lemma[1]
    wb = openpyxl.Workbook()
    ws = wb.active  # get a handle to the sheet in the workbook
    ws['A1'] = "POS and Lemma Spreadsheet"
    endcol = len(tree_taglist) * 2 + 1
    for col in range(1, endcol, 2):  # go up by two because the POSs need to be separated. add one because indexing starts at 1 in openpyxl
        pos = tree_taglist[(col - 1) // 2]
        print("processing", pos, "words")
        if pos == "``":
            pos = "''"  # `` is equivalent to ''
        entry = tag_dict[pos]
        ws.cell(row=2, column=col).value = tree_tagdefs[pos]
        # sort the dictionary
        if sort == "frequencyhi":
            entry_list = sorted(entry.items(), key=operator.itemgetter(1), reverse=True)
        elif sort == "alpha":
            entry_list = sorted(entry.items(), key=operator.itemgetter(0))
        elif sort == "reversealpha":
            entry_list = sorted(entry.items(), key=operator.itemgetter(0), reverse=True)
        elif sort == "frequencylo":
            entry_list = sorted(entry.items(), key=operator.itemgetter(1))
        for row in range(3, len(entry_list) + 3):  # this number is equal to the number of unique words with that suffix
            idx = row - 3
            word = entry_list[idx][0]
            try:
                ws.cell(row=row, column=col).value = word
            except openpyxl.utils.exceptions.IllegalCharacterError:
                # word = input(word + " invalid. New value: ")
                ws.cell(row=row, column=col).value = "IllegalCharacterError"
            ws.cell(row=row, column=col+1).value = entry_list[idx][1]  # frequency
        if not filename.endswith(".xlsx"):  # save the spreadsheet after each POS (in case of crash)
            wb.save(filename + ".xlsx")  # add the type extension if not included
        else:
            wb.save(filename)
    print("processing lemmas")
    ws.cell(row=2, column=endcol).value = "Lemmas"
    if sort == "frequencyhi":
        lemma_list = sorted(lemma_dict.items(), key=operator.itemgetter(1), reverse=True)
    elif sort == "alpha":
        lemma_list = sorted(lemma_dict.items(), key=operator.itemgetter(0))
    elif sort == "reversealpha":
        lemma_list = sorted(lemma_dict.items(), key=operator.itemgetter(0), reverse=True)
    elif sort == "frequencylo":
        lemma_list = sorted(lemma_dict.items(), key=operator.itemgetter(1))
    for row in range(3, len(lemma_list) + 3):
        idx = row - 3
        lemma = lemma_list[idx][0]
        try:
            ws.cell(row=row, column=endcol).value = lemma
        except openpyxl.utils.exceptions.IllegalCharacterError:
            # lemma = input(lemma + " invalid. New value: ")
            ws.cell(row=row, column=endcol).value = "IllegalCharacterError"
        ws.cell(row=row, column=endcol + 1).value = lemma_list[idx][1]  # frequency
    if not filename.endswith(".xlsx"):  # save the spreadsheet
        wb.save(filename + ".xlsx")  # add the type extension if not included
    else:
        wb.save(filename)


def freq_from_str(text, case_sensitive=False):
    """
    Get the frequencies of words from a string
    :param text:
    :param case_sensitive:
    :return:
    """
    if case_sensitive:
        words = [word for word in nltk.word_tokenize(text) if
                 word.isalpha() or word.replace("'", "").isalpha()]
    else:
        words = [word for word in nltk.word_tokenize(text.lower()) if
                 word.isalpha() or word.replace("'", "").isalpha()]
    freqdist = nltk.FreqDist(words)
    return freqdist


def freq_from_csv(csv_in, case_sensitive=False):
    """
    Get the frequencies of words from a csv created using ao3_get_fanfics.py
    :param csv_in: the name of a csv file to read in
    :return: a FreqDist object with the unique words and their frequencies
    """
    f_in = open(csv_in, 'r+')
    reader = csv.reader(f_in)
    header = next(reader)
    freqdist = nltk.FreqDist()
    for row in reader:
        this_freqdist = freq_from_str(row[-1], case_sensitive)
        freqdist.update(this_freqdist)
    return freqdist


def freq_from_txt(infilename, case_senstive=False):
    """
    Get the frequencies of words from a txt file
    :param infilename: the name of a txt file
    :return: a FreqDist object with the unique words and their frequencies
    """
    f_in = open(infilename)
    freqdist = freq_from_str(f_in.read(), case_senstive)
    f_in.close()
    return freqdist


def freq_from_dir(path, case_sensitive=False, end=".txt", walk=False):
    """
    Get the frequencies of words from a directory. Data is aggreggated across all files
    :param path: path to the directory to read
    :param case_sensitive: if True, "The" is different from "the"
    :param walk: if True, go into subdirectories
    :return: a FreqDist object with the unique words and their frequencies
    """
    currentdir = os.getcwd()
    filename_list = []
    if walk:
        for item in os.walk(path):
            # print(item)
            currentpath = item[0]  # might need to join with path
            os.chdir(currentpath)  # change to the directory you are looking at. useful for reading and writing files
            for filename in item[2]:
                if filename.endswith(end):
                    filename_list.append(os.path.join(currentpath, filename))
    else:
        for filename in os.listdir(path):
            if filename.endswith(end):
                filename_list.append(os.path.join(path, filename))
    os.chdir(currentdir)
    freqdist = nltk.FreqDist()
    for filename in filename_list:
        print("freq_from_dir getting freq from", filename)
        this_freqdist = freq_from_txt(filename, case_sensitive)
        freqdist.update(this_freqdist)
    return freqdist


def freqdist_to_wordlistfile(freqdist, filename):
    """
    Store the results of a frequency distribution in a txt file in a format identical to the one generated by AntConc
    :param freqdist: the FreqDist object
    :param filename: the txt file to store the results in
    :return:
    """
    tokens = freqdist.N()
    types = len(freqdist)
    print(filename, tokens, types)
    with open(filename, 'w') as f_out:
        f_out.write("#Word types: " + str(types) + "\n")  # unique words
        f_out.write("#Word tokens: " + str(tokens) + "\n")  # total words
        f_out.write("#Search results: 0" + '\n')
        rank = 1
        for tup in freqdist.most_common():
            word = tup[0]
            freq = str(tup[1])
            f_out.write(str(rank) + "\t" + freq + "\t" + word + "\t\n")
            rank += 1


def keywordanalysis(corpus1name, corpus2name):
    """
    :param corpus1name: name of the first txt wordlist file in the format generated by AntConc
    :param corpus2name: name of the second txt wordlist file in the format generated by AntConc
    :return: a dictionary containing the words and their frequencies, keynesses, and effects
    """
    print("keyword analysis")
    corpus2 = open(corpus2name)
    types2 = int(next(corpus2)[13:])
    tokens2 = int(next(corpus2)[14:])
    next(corpus2)
    # load corpus2 into a FreqDist
    freqdist2 = nltk.FreqDist()
    for line in corpus2:
        line = line.split()
        freqdist2[line[2]] = line[1]  # store the word and its frequency
    corpus2.close()
    keyword_dict = {}  # {word: (frequency, keyness)}  # TODO: implement effect
    # start reading corpus1
    corpus1 = open(corpus1name)
    types1 = int(next(corpus1)[13:])
    tokens1 = int(next(corpus1)[14:])
    next(corpus1)
    for line in corpus1:
        line = line.split()
        freq1 = int(line[1])
        word = line[2]
        freq2 = int(freqdist2[word])
        num = (freq1 + freq2) / (tokens1 + tokens2)
        E1 = tokens1 * num
        E2 = tokens2 * num
        try:
            keyness = 2 * (freq1 * math.log(freq1/E1) + (freq2 * math.log(freq2/E2)))  # TODO: try except
        except ValueError:
            keyness = 2 * (freq1 * math.log(freq1/E1))  # the second part equals 0
        keyword_dict[word] = (freq1, keyness)
    corpus1.close()
    return keyword_dict


def store_keyword(keyword_dict, filename="Keyword Spreasheet.xlsx", sort="keynesshi"):
    """
    Store a keyword dict to a spreadsheet
    :param keyword_dict: a keyword dict { word: (frequency, keyness)
    :param filename: the name of the spreadsheet
    :return:
    """
    print("storing keyword analysis")
    wb = openpyxl.Workbook()
    ws = wb.active  # get a handle to the sheet in the workbook
    ws['A1'] = "Keyword Spreadsheet"
    ws.cell(row=2, column=1).value = "Word"
    ws.cell(row=2, column=2).value = "Frequency"
    ws.cell(row=2, column=3).value = "Keyness"
    entry_list = []
    for item in keyword_dict.items():
        word = item[0]
        entry_list.append((word, keyword_dict[word][0], keyword_dict[word][1]))  # frequency, keyness
    if sort == "keynesshi":
        entry_list.sort(key=operator.itemgetter(2), reverse=True)
    else:  # TODO implement other sorting later
        entry_list.sort(key=operator.itemgetter(2), reverse=True)
    for row in range(3, len(entry_list) + 3):
        idx = row - 3
        word = entry_list[idx][0]
        try:
            ws.cell(row=row, column=1).value = word
        except openpyxl.utils.exceptions.IllegalCharacterError:
            word = input(word + " invalid. New value: ")
            ws.cell(row=row, column=1).value = word
        ws.cell(row=row, column=2).value = int(entry_list[idx][1])  # store frequency
        ws.cell(row=row, column=3).value = int(entry_list[idx][2])  # store keyness
    if not filename.endswith(".xlsx"):
        wb.save(filename + ".xlsx")  # add the type extension if not included
    else:
        wb.save(filename)

project_dir = "/Volumes/CDJ_disk/Final_Project"


def sherlock_tag():
    """tag_directory(os.path.join(project_dir, "Fanfiction/Sherlock/Sherlock works En"), os.path.join(project_dir,  # removed 5825911 it's a tutorial
            "Tagged Sherlock"), restart="695066.txt")  # skip 2208000, skip 3538460"""
    tag_lemma = tag_lemma_from_tree_directory(os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Sherlock"))
    store_taglemma_results(tag_lemma, filename="Sherlock POS Lemma")


def undertale_tag():
    """
    tag_directory(os.path.join(project_dir, "Fanfiction/Undertale/Undertale works"), os.path.join(project_dir,
            "Tag/Tag Fanfic/Tagged Undertale"), restart="6275878.txt")  # skip 11073834, 4981594, 6174664, 6275314
    """
    tag_lemma = tag_lemma_from_tree_directory(os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Undertale"))
    store_taglemma_results(tag_lemma, filename="Undertale POS Lemma")


def doctor_who_tag():
    # tag_directory(os.path.join(project_dir, "Fanfiction/Doctor Who/Doctor Who works"), os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Doctor Who"), restart="4776638.txt")  # error 108673, do 108674
    tag_lemma = tag_lemma_from_tree_directory(os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Doctor Who"))
    store_taglemma_results(tag_lemma, filename="Doctor who POS Lemma")


def lotr_tag():
    # tag_directory(os.path.join(project_dir, "Fanfiction/Lotr/Lotr works"), os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Tolkien"), restart="3403703.txt")  # skipped 2208000, 3403682
    tag_lemma = tag_lemma_from_tree_directory(os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Tolkien"))
    store_taglemma_results(tag_lemma, filename=os.path.join(project_dir, "Antconc results/Tag results/Tag Fanfic/Tolkien POS Lemma.xlsx"))


def hamilton_tag():
    # tag_directory(os.path.join(project_dir, "Fanfiction/Hamilton/Hamilton works"), os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Hamilton"), restart="8015692.txt")  # skip 8014951
    tag_lemma = tag_lemma_from_tree_directory(os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Hamilton"))
    store_taglemma_results(tag_lemma, filename=os.path.join(project_dir, "Antconc results/Tag results/Tag Fanfic/Hamilton POS Lemma.xlsx"))

def les_mis_tag():
    tag_lemma = tag_lemma_from_tree_directory(os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Les Mis"))
    store_taglemma_results(tag_lemma, filename=os.path.join(project_dir, "Antconc results/Tag results/Tag Fanfic/Les Mis POS Lemma.xlsx"))

def undertale_freq():
    freqdist = freq_from_txt("Undertale Text (not arranged).txt")
    pprint.pprint(freqdist.most_common())
    freqdist_to_wordlistfile(freqdist, "Undertale wordlist.txt")

def fanfic_tag():
    sherlock_tag()
    doctor_who_tag()
    undertale_tag()
    lotr_tag()
    hamilton_tag()
    les_mis_tag()

def original_canon_freq():
    originaldir = os.getcwd()
    os.chdir(os.path.join(project_dir, "Original Canon"))
    current = os.getcwd()
    for dir_name in os.listdir(current)[1:]:
        freqdist = freq_from_dir(os.path.join(current, dir_name), walk=True)
        freqdist_to_wordlistfile(freqdist, os.path.join(project_dir, dir_name + " wordlist"))
    os.chdir(originaldir)


def dw_wordlists_keyword():
    resultdir = "/Volumes/CDJ_disk/Final_Project/Antconc results/AntConc/Ant Original Canon/Ant Doctor Who"
    keyword_dict = keywordanalysis(os.path.join(resultdir, "Doctor Who Related wordlist.txt"), os.path.join(resultdir, "DW_related_antconc_results.txt"))
    store_keyword(keyword_dict, os.path.join(project_dir, "Antconc results/Keyword analysis/Doctor Who wordlist vs AntConc.xlsx"))


# TODO: allow walk directory
def original_canon_tag():
    originaldir = os.getcwd()
    os.chdir(os.path.join(project_dir, "Original Canon"))
    current = os.getcwd()
    tagdir = os.path.join(project_dir, "Tag/Tag Original Canon")
    skipdir = True  # flag (skip first directory)
    for item in os.walk(current):
        if skipdir:
            skipdir = False
            continue
        dir_name = item[0]
        this_tag_dir = os.path.join(tagdir, dir_name[dir_name.index("Canon") + 6:])
        if not os.path.isdir(this_tag_dir):
            os.mkdir(this_tag_dir)
        files = item[2]
        if len(files) > 0:
            print("original_canon_tag", dir_name)
            tag_directory(dir_name, this_tag_dir)
    os.chdir(originaldir)


def original_canon_poslemma():
    originaldir = os.getcwd()
    tagdir = os.path.join(project_dir, "Tag/Tag Original Canon")
    os.chdir(tagdir)
    current = os.getcwd()
    for dirname in os.listdir(current):
        if dirname.startswith("Tagged"):
            tag_lemma = tag_lemma_from_tree_directory(os.path.join(current, dirname), walk=True)
            store_taglemma_results(tag_lemma, filename=os.path.join(project_dir,
                                                                    "Antconc results/Tag results/Tag Original Canon/") + dirname.replace("Tagged", "Tag") + " POS Lemma.xlsx")
    os.chdir(originaldir)


def clean_tagged(name_to_clean, originalfilename, logtxt):
    with open(name_to_clean) as file:
        body = file.read()
        if "replaced-" in body:
            print("replacing", name_to_clean)
            logtxt.write(name_to_clean + "\n")
            tagger.tag_file_to(originalfilename, name_to_clean, notagurl=True, notagemail=True, notagip=True, notagdns=True)

tagsdir = os.path.join(project_dir, "Tag")


def clean_fanfic():
    for item in os.walk(tagsdir):
        path = item[0]
        filenames = item[2]
        if "Tag Fanfic/Tagged" in path:  #  and len(filenames) > 0
            print("path is", path)
            fandom = path[path.index("Tagged")+7:]
            fanfic_path = os.path.join(project_dir, "Fanfiction/" + fandom + "/" + fandom + " works")
            logfile = open(fandom + "_logfile.txt", "w")  # + "_logfile.txt" after I hit run
            for filename in filenames:
                clean_tagged(os.path.join(path, filename), os.path.join(fanfic_path, filename.replace("_tagged","")), logfile)
            logfile.close()

# tag_directory(os.path.join(project_dir, "Fanfiction/Doctor Who/Doctor Who works"), os.path.join(project_dir, "Tag/Tag Fanfic/Tagged Doctor Who"), end="10544770.txt")  # error 108673, do 108674