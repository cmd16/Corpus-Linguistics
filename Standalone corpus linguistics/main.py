import nltk
import pprint   # For proper print of sequences.
import treetaggerwrapper
import operator
import csv
import openpyxl
import os
import math
import re
import time

# TODO: HAVE PAST VS PAST PARTICIPLE
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


def freq_from_txt(infilename, case_senstive=False):
    """
    Get the frequencies of words from a txt file
    Limitations: I've noticed not all the contractions split correctly; e.g., "n't" and "shan't" appear in the same wordlist
    :param infilename: the name of a txt file
    :return: a FreqDist object with the unique words and their frequencies
    """
    try:
        f_in = open(infilename)
        # assert f_in.is_open()
        freqdist = freq_from_str(f_in.read(), case_senstive)
        f_in.close()
        return freqdist
    except FileNotFoundError:
        # print(infilename, end=", ")
        print(infilename[infilename.index("all")+4:infilename.index(".txt")])
        return False


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
        if this_freqdist:  # if a freqdist was successfully created
            freqdist.update(this_freqdist)
    print()
    return freqdist


def freqdist_from_idfile (filename, path, case_sensitive=False, end=".txt"):
    infile = open(filename, 'r')
    freqdist = nltk.FreqDist()
    for line in infile:
        name = os.path.join(path, line.strip() + end)
        this_freqdist = freq_from_txt(name, case_sensitive)
        if this_freqdist:  # will be false if the file couldn't open
            freqdist.update(this_freqdist)
        else:
            pass
            # print(line.strip(), this_freqdist)
    infile.close()
    return freqdist


def freqdist_to_wordlistfile(freqdist, filename):
    """
    Store the results of a frequency distribution in a txt file in a format similar to the one generated by AntConc

    :param freqdist: the FreqDist object
    :param filename: the txt file to store the results in
    :return:
    """
    tokens = freqdist.N()
    types = len(freqdist)
    # print(filename, tokens, types)
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


def wordlist_to_freqdist(wordlist_file):
    """
    Given a wordlist return a frequency distribution as well as the number of types and tokens
    :param wordlist_file: a .txt file generated from AntConc or freqdist_to_wordlistfile. Line 1 has the number of types,
    line 2 the number of tokens, and lines 4-end are in the format "rank\tword\tfrequency"
    :return: a frequency distribution (word frequencies), the number of types, and the number of tokens
    """
    corpus = open(wordlist_file)
    types = int(next(corpus)[13:])
    tokens = int(next(corpus)[14:])
    next(corpus)
    # load corpus into a FreqDist
    freqdist1 = nltk.FreqDist()
    for line in corpus:
        line = line.split()
        freqdist1[line[2]] = int(line[1])  # store the word and its frequency
    corpus.close()
    return freqdist1, types, tokens


def combine_wordlists_to_freqdist(wordlists):
    """
    Return a freqdist that is the combination of several wordlists
    :param wordlists: a list of wordlist filenames
    :return: Return a freqdist that is the combination of several wordlists
    """
    print("combining wordlists")
    freqdist = nltk.FreqDist()
    for wordlist in wordlists:
        this_freqdist = wordlist_to_freqdist(wordlist)[0]
        freqdist.update(this_freqdist)
    return freqdist


def freqdist_to_excel(freqdist, filename):
    """
    Store the results of a frequency distribution in an excel spreadsheet
    :param freqdist: a frequency distribution with word frequencies, generated using
    :param filename: an excel filename to store the results in
    :return:
    """
    tokens = freqdist.N()
    types = len(freqdist)
    wb = openpyxl.Workbook()
    ws = wb.active  # get a handle to the sheet in the workbook
    ws['A1'] = "Freqdist Spreadsheet"
    ws['B1'] = "Total words (tokens)"
    ws['B2'] = tokens
    ws['B3'] = "Unique words (types)"
    ws['B4'] = types
    ws['C1'] = "word"
    ws['C2'] = "frequency"
    # ws['C3'] = "frequency per million"
    entries = freqdist.most_common()
    for rownum in range(3, len(entries) + 3):
        tup = entries[rownum - 3]  # a tuple with word, frequency, percentage (/10000 to get per million)
        ws.cell(row=rownum, col=1).value = tup[0]
        ws.cell(row=rownum, col=2).value = tup[1]
    wb.save(filename)
        # ws.cell(row=rownum, col=3).value = freqdist.freq[tup[0]] / 10000 # uncomment this for more data but it will go slower


def normalize_count_permillion(frequency, size):
    """
    Normalize a frequency given the frequency and the size
    :param frequency: frequency
    :param size: the size of the data (e.g., number of words in the corpus)
    :return: frequency per million
    """
    return frequency * 1000000 / size


def keyword_tuple_from_wordlists(corpus1name, corpus2name, p=0.01):
    """
    Keyword analysis.
    Limitations: the numbers are a little bit different here (about 10 lower or higher in the few examples I looked at)
    from the loglikelihood calculator at http://ucrel.lancs.ac.uk/cgi-bin/llsimple.pl?f1=3852&f2=2179&t1=3802120&t2=3569518
    even though I used the same formula
    Note: values are only stored if keyness is statistically significant as determined by the p value and
    normalized frequency 1 > normalized frequency 2
    :param corpus1name: name of the first txt wordlist file in the format generated by AntConc
    :param corpus2name: name of the second txt wordlist file in the format generated by AntConc
    :return: a dictionary containing the words and their frequencies, keynesses, and effects. Now it is a tuple containing that dictionary and the types and tokens
    """
    print("keyword analysis from", corpus1name, "to", corpus2name)
    if p == 0.5:
        crit = 3.84
    elif p == 0.01:
        crit = 6.63
    elif p == 0.001:
        crit = 10.83
    elif p == 0.0001:
        crit = 15.13
    elif p == 0:
        crit = 0
    else:
        crit = 6.63  # changed the default to 1% error margin
    freqdist2, types2, tokens2 = wordlist_to_freqdist(corpus2name)
    if types2 == 0 or tokens2 == 0:
        print(corpus2name, "is empty")
        return False # the wordlist is empty or something else went wrong
    keyword_dict = {}  # {word: (frequency1, normalizedfreq1, freq2, normalizedfreq2, keyness)}  # TODO: implement effect
    # start reading corpus1
    corpus1 = open(corpus1name)
    types1 = int(next(corpus1)[13:])
    tokens1 = int(next(corpus1)[14:])
    if types1 == 0 or tokens1 == 0:
        print(corpus1name, "is empty")
        return False  # the wordlist is empty or something else went wrong
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
            keyness = 2 * (freq1 * math.log(freq1/E1) + (freq2 * math.log(freq2/E2)))
        except ValueError:
            keyness = 2 * (freq1 * math.log(freq1/E1))  # the second part equals 0
        norm1 = normalize_count_permillion(freq1, tokens1)
        norm2 = normalize_count_permillion(freq2, tokens2)
        if keyness >= crit and norm1 > norm2:
            keyword_dict[word] = (freq1, norm1, freq2, norm2, keyness)
    corpus1.close()
    return keyword_dict, [corpus1name, types1, tokens1], [corpus2name, types2, tokens2]


def keyword_tuple_from_keywordtxt(filename):
    keyword_dict = {}
    try:
        f_in = open(filename)
    except FileNotFoundError:
        raise FileNotFoundError
    for line in f_in:
        line = line.strip().split("\t")
        if line[0].startswith("#"):
            if line[0] == "# Corpus 1:":
                corpus1name, types1, tokens1 = line[1:]
            elif line[0] == "# Corpus 2:":
                corpus2name, types2, tokens2 = line[1:]
            continue
        word = line[0]
        keyness = float(line[1])
        try:
            freq1 = int(line[2])
        except ValueError:
            raise ValueError
        norm1 = float(line[3])
        freq2 = int(line[4])
        norm2 = float(line[5])
        keyword_dict[word] = (keyness, freq1, norm1, freq2, norm2)
    f_in.close()
    return keyword_dict, [corpus1name, types1, tokens1], [corpus2name, types2, tokens2]


def store_keyword_txt(keyword_tuple, filename, sort_key="keynesshi"):
    """
    Store a keyword dictionary in a txt file, separated by tabs. Note: values are only stored if keyness is statistically
    significant as determined by the p value and normalized frequency 1 > normalized frequency 2
    :param keyword_tuple: [keyword_dict, corpus1stats, corpus2stats]. The keyword dict contains keyness, raw frequencies,
    and normalized frequencies
    :param filename:
    :param sort_key:
    :return:
    """
    f_out = open(filename, 'w')
    keyword_dict = keyword_tuple[0]
    corpus1name, types1, tokens1 = keyword_tuple[1]
    f_out.write("# Corpus 1:\t%s\t%d\t%d\n" % (corpus1name, types1, tokens1))
    corpus2name, types2, tokens2 = keyword_tuple[2]
    f_out.write("# Corpus 2:\t%s\t%d\t%d\n" % (corpus2name, types2, tokens2))
    f_out.write("# %s\t%s\t%s\t%s\t%s\t%s\n" % ("word", "keyness", "freq1", "norm1", "freq2", "norm2"))
    entry_list = []
    for item in keyword_dict.items():
        word = item[0]
        stats = item[1]
        freq1 = stats[0]  # all of the stats numbers shift over 1 when you move the thing
        norm1 = stats[1]
        freq2 = stats[2]
        norm2 = stats[3]
        keyness = stats[4]
        entry_list.append((word, freq1, norm1, freq2, norm2, keyness))
    if sort_key == "keynesshi":
        entry_list.sort(key=operator.itemgetter(5), reverse=True)
    else:  # TODO implement other sorting later
        entry_list.sort(key=operator.itemgetter(5), reverse=True)
    for entry in entry_list:
        word = entry[0]
        freq1 = entry[1]  # all of the stats numbers shift over 1 when you move the thing
        norm1 = entry[2]
        freq2 = entry[3]
        norm2 = entry[4]
        keyness = entry[5]
        f_out.write("%s\t%f\t%d\t%f\t%d\t%f\n" % (word, keyness, freq1, norm1, freq2, norm2))
    f_out.close()


def find_similar_keywords(keyword_files, out_csv_name, sort_key="keyness1hi"):
    """
    Given a list of files of keyword dicts, find which keywords the corpora have in common
    master_key_dict is a dictionary that maps words to a list. mastery_key_dict[word] =
    [statsforcorpus1, statsforcorpus2, etc.]
    :param keyword_files: a list of filenames containing keyword analysis
    :return:
    """
    if len(keyword_files) < 2:
        raise ValueError("Must input 2 or more files for analysis")
    try:
        key_dict, [corpus1name, types1, tokens1], [corpus2name, types2, tokens2] = keyword_tuple_from_keywordtxt(keyword_files[0])
    except FileNotFoundError:
        print("FileNotFoundError", out_csv_name, keyword_files[0])
        return
    except ValueError:
        print("ValueError", out_csv_name, keyword_files[0])
        return
    master_key_dict = {}
    for word in key_dict:
        master_key_dict[word] = [key_dict[word]]
    for filename in keyword_files[1:]:
        try:
            key_dict, [corpus1name, types1, tokens1], [corpus2name, types2, tokens2] = keyword_tuple_from_keywordtxt(filename)
        except FileNotFoundError:
            print("FileNotFoundError", out_csv_name, filename)
            return
        except ValueError:
            print("ValueError", out_csv_name, filename)
            return
        words_to_del = []
        for word in master_key_dict:
            if word in key_dict:
                master_key_dict[word].append(key_dict[word])
            else:  # this isn't a keyword that is in all corpora, so we need to remove it
                words_to_del.append(word)
        for word in words_to_del:
            del master_key_dict[word]
    f_out = open(out_csv_name, 'w')
    writer = csv.writer(f_out, delimiter="\t", quotechar='|')
    filename_fields = []
    for filename in keyword_files:
        filename_fields.append(filename)
        filename_fields.extend([""]*4)
    filename_fields.pop()  # get rid of the last empty field
    writer.writerow([""] + filename_fields)  # first two are empty for word and keyness
    rows = []  # note: this is not memory efficient, but it's the simplest way to deal with the sorting problem
    for item in master_key_dict.items():
        word, stat_lists = item
        stat_flat = [word]
        for stat_list in stat_lists:
            keyness, freq1, norm1, freq2, norm2 = stat_list
            # ["%f" % keyness, "%d" % freq1, "%f" % norm1, "%d" % freq2, "%f" % norm2]
            stat_flat.extend(stat_list)
        rows.append(stat_flat)
    if sort_key == "alphalo":
        rows.sort(key=operator.itemgetter(0))
    elif sort_key == "keyness1hi":
        rows.sort(key=operator.itemgetter(1), reverse=True)
    elif sort_key == "alphahi":
        rows.sort(key=operator.itemgetter(0), reverse=True)
    elif sort_key == "keyness1lo":
        rows.sort(key=operator.itemgetter(1))
    else:
        rows.sort(key=operator.itemgetter(1), reverse=True)  # default to sorting by keynesshi
    for row in rows:
        str_row = []
        str_row.append(row.pop(0))  # append the word
        for i in range(0, len(keyword_files)*5, 5):
            keyness, freq1, norm1, freq2, norm2 = row[i:i+5]
            str_row.extend(["%f" % keyness, "%d" % freq1, "%f" % norm1, "%d" % freq2, "%f" % norm2])
        writer.writerow(str_row)
    f_out.close()


def store_keyword(keyword_tuple, filename="Keyword Spreadsheet.xlsx", sort="keyness1hi"):
    """
    Store a keyword dict to a spreadsheet
    :param keyword_tuple: keyword dict { word: (frequency, keyness)}, [stats1], [stats2]
    :param filename: the name of the spreadsheet
    :return:
    """
    print("storing keyword analysis")
    keyword_dict = keyword_tuple[0]
    corpus1_stats = keyword_tuple[1]
    corpus2_stats = keyword_tuple[2]
    wb = openpyxl.Workbook()
    ws = wb.active  # get a handle to the sheet in the workbook
    # ws['A1'] = "Keyword Spreadsheet"
    for idx in range(3):
        ws.cell(row=1, column=idx + 1).value = corpus1_stats[idx]
        ws.cell(row=1, column= idx + 4).value = corpus2_stats[idx]
    ws.cell(row=2, column=1).value = "Word"
    ws.cell(row=2, column=2).value = "Frequency 1"
    ws.cell(row=2, column=3).value = "Normalized frequency 1"
    ws.cell(row=2, column=4).value = "Frequency 2"
    ws.cell(row=2, column=5).value = "Normalized frequency 2"
    ws.cell(row=2, column=6).value = "Keyness"  # fixed error
    entry_list = []
    for item in keyword_dict.items():
        word = item[0]
        stats = item[1]
        freq1 = stats[0]  # all of the stats numbers shift over 1 when you move the thing
        norm1 = stats[1]
        freq2 = stats[2]
        norm2 = stats[3]
        keyness = stats[4]
        entry_list.append((word, freq1, norm1, freq2, norm2, keyness))  # frequency1, keyness
    if sort == "keynesshi":
        entry_list.sort(key=operator.itemgetter(5), reverse=True)
    else:  # TODO implement other sorting later
        entry_list.sort(key=operator.itemgetter(5), reverse=True)
    for row in range(3, len(entry_list) + 3):
        idx = row - 3
        word = entry_list[idx][0]
        freq1 = entry_list[idx][1]  # all of the stats numbers shift over 1 when you move the thing
        norm1 = entry_list[idx][2]
        freq2 = entry_list[idx][3]
        norm2 = entry_list[idx][4]
        keyness = entry_list[idx][5]
        try:
            ws.cell(row=row, column=1).value = word
        except openpyxl.utils.exceptions.IllegalCharacterError:
            word = input(word + " invalid. New value: ")
            ws.cell(row=row, column=1).value = word
        ws.cell(row=row, column=2).value = freq1  # store frequency
        ws.cell(row=row, column=3).value = norm1
        ws.cell(row=row, column=4).value = freq2
        ws.cell(row=row, column=5).value = norm2
        ws.cell(row=row, column=6).value = keyness
    if not filename.endswith(".xlsx"):
        wb.save(filename + ".xlsx")  # add the type extension if not included
    else:
        wb.save(filename)


if __name__ == "__main__":
    proj_dir = "/Volumes/2TB/Final_Project"

    # category_wordlists(proj_dir)
    # au_wordlists(proj_dir)
    # tags_wordlists(proj_dir)
    # category_wordlists(proj_dir)
    # status_wordlists(proj_dir)
    # year_wordlists(proj_dir)
    # rating_wordlists(proj_dir)
    # fandom_group_wordlists(proj_dir)  # TODO: fix later
    # wordnum_wordlists(proj_dir)
    for year in range(2009, 2019):
        print("SH", year)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Sherlock %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % year))

    print("BBC SH")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/BBC Sherlock.txt"), os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/BBC_Sherlock_python.txt"))


# start = time.time()
# freqdist = freq_from_dir("/Volumes/2TB/Final_project/Fanfic_all")
# dir_time = time.time() - start
# print("Time to get wordlist:", dir_time)
# start = time.time()
# freqdist_to_wordlistfile(freqdist, "/Volumes/2TB/Final_Project/wordlists/fanfic_all_python.txt")
# word_out_time = time.time() - start
# print("Time to write out wordlist:", word_out_time)

# print("DW")
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Classic Who.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Classic_Who_python.txt"))
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/New Who.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/New_Who_python.txt"))
#
# print("H")
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Hamilton.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Hamilton_python.txt"))
#
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Les Mis.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Les_Mis_python.txt"))
#
# print("SH")
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Sherlock.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Sherlock_python.txt"))
#
# print("ST")
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Star Trek.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Star_Trek_python.txt"))
#
# print("T")
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Tolkien.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Tolkien_python.txt"))
#
# print("U")
# freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale.txt"), os.path.join(proj_dir, "Fanfic_all"))
# freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Undertale_python.txt"))

# hamilton_remove = ["9051955", "6163238", "6157525"]

"""
/anaconda/bin/python3.5 "/Users/cat/PycharmProjects/CorpusLinguisticsClass/Standalone corpus linguistics/main.py"
10500279 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
9051955 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
13346448 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13162389 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13150815 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13190844 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13042899 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13045944 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12996450 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12870165 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12564708 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12286731 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12286785 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12284460 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11977479 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11903901 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11803812 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11703900 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11625312 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11532309 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11510115 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11494026 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11412099 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11368038 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11315433 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11307960 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11295315 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11297718 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11080263 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11211402 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11188680 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11109816 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11141952 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11059938 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11059896 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11109894 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11027655 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11020227 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11020134 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11016960 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10950537 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10941576 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10925733 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10894737 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10894710 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10875825 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10875732 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10873854 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10865232 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10858599 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10857390 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11157849 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10716399 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10539135 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10452402 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10344270 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10237538 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10232798 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9694574 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11142150 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9108235 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9062875 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
7921630 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10468848 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
7344757 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
7211777 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
6424531 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
6275809 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
6091024 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5709103 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5664376 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5664343 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5608507 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5516012 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5509559 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5528387 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5352920 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5033050 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11110056 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4863320 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4795886 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4779395 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4698098 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4637157 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4564311 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4368707 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4264461 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4205280 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4037497 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3957667 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3945808 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3838843 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3646056 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3066143 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2653757 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2581445 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2420279 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2311955 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2259009 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2015838 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1985223 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1763343 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1736504 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1736474 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1579037 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1720031 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1697489 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1654649 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1651742 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1551194 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1473331 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1464757 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318867 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318858 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318843 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318810 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1110732 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1104835 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1098550 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1053890 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
990949 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
985139 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144332 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
948570 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
947275 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
912879 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
911351 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
909778 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902513 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902510 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902501 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902496 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902490 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902486 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902482 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902479 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902476 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902471 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902468 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902438 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902425 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144269 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1117861 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144248 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834223 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
833936 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
918190 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144215 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
803620 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
803629 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
762273 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834219 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834211 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
693840 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
643594 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
633903 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
625265 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
620174 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
620169 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681304 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834204 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834201 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834195 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
532601 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
524077 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
508646 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
502149 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
476447 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144029 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
431948 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681289 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
412824 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
391300 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3143849 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681279 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681275 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681271 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681265 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
253468 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681252 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
235044 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
199758 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3143819 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
489371 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10954374 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13278189 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13325424 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13172514 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12903456 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12724581 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12257427 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12215016 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12144471 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11965590 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11963226 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11963133 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11851005 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11703957 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11597337 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11594424 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11006187 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10994832 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10694073 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10861974 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10837317 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10808076 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10801716 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10701651 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10701294 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10675533 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10572321 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10540755 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10355619 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10342764 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10262447 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10225031 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10165913 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9984788 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9953198 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9949661 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9949355 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9949250 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9925046 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9857927 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9697016 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9696665 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9529388 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9498848 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9295424 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9293888 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9219842 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8939704 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8843515 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8748226 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8696662 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8599879 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8569939 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8498938 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8483692 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8412091 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8396629 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8419117 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8339359 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8337628 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8332564 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8156506 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8153468 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8039770 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8037436 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8017099 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7996621 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7892617 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8172460 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7759042 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7757248 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7614352 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7614286 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7599382 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7534021 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7524934 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7347916 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7192613 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7188119 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7186865 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6822550 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6738346 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6517051 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6503914 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6497197 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6495838 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6349330 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6349213 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6290860 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6115714 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6061195 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6049723 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6034672 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5979859 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5738446 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5717572 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5496968 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5298962 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5235146 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5139521 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4851407 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4668143 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4512213 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4402820 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4327422 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4306224 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3664431 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3645915 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3574277 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3350675 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3325001 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3253052 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3156437 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812655 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812634 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812472 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812391 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2811881 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2717381 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2717372 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2627288 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2289590 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2262681 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2244114 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2134059 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2017044 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1856389 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1807885 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1802026 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1764927 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1700891 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1662125 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1662074 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1619549 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1613240 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1579826 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1417810 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1333234 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1333153 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1333096 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1275334 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2289626 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1235470 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1220599 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1148672 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1179432 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1178571 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1175297 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1174344 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1142705 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1116672 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1104778 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1103103 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1081778 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1080831 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1075614 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1047568 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1044295 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1017768 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1005767 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
955445 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
955380 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
955436 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
950805 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
947441 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
942392 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
881543 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
881837 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
860634 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
857738 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
856327 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
856163 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
854766 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
851210 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
848335 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
844920 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
842878 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
839158 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
833563 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
825222 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
825174 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
807713 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
788882 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
918203 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
706973 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
687598 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
665505 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
592289 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
580323 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
580315 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
580312 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
579696 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
564373 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
556207 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
556203 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
540816 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
526872 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
514302 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
514298 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
514294 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
508610 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
499361 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
459775 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
388598 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
357591 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
343257 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9421379 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360705 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
265047 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
261221 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
261215 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9420917 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338774 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338693 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360712 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338618 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9420791 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338549 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360716 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360723 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360724 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360734 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
196212 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9421004 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360744 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360747 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360750 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360758 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9337631 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10902519 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5051194 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
489240 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8075698 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5738755 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
879304 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
879324 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
879360 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
842022 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
839489 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
846732 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
839495 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13357866 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13340919 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13290900 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13206963 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13137519 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13134705 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13124190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13054566 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13053270 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13051491 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13048104 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13032366 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12781986 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12756987 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12581648 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12571928 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12486216 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12461229 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12300204 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12397731 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12327207 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12294081 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12117948 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12082554 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11876682 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11875287 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11754501 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11689590 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11689521 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11630385 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11548797 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11520741 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11518569 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11482380 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11425500 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11373495 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11341530 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11292567 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11224098 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9585374 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11133681 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11062683 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10928952 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10829103 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10679217 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10637232 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10628154 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10387416 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10329893 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10313288 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10101023 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10077530 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9815480 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9753317 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9570020 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9457946 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9160954 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9062578 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8857234 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8886931 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8881417 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8828794 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8799877 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8559196 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8484241 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8300677 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8250994 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8237033 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8151250 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8148449 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8131439 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8130914 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7450816 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7286134 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7266157 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7245934 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7165832 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7024864 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6975934 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6951454 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6919345 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6779254 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6779185 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6779218 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6604852 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6574159 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6559408 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6485671 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6474076 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6359083 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6349186 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6349012 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6341734 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6334564 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6177070 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6170371 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147694 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147685 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147664 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147619 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6097132 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5996962 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5975575 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5975539 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5932311 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5902402 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5878291 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5830507 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5645590 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5524313 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5520581 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5489585 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5479157 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5300081 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5340185 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5470190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5450804 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5457578 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5395328 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5443514 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5392769 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5255795 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5290115 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5408627 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5431598 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5430740 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5424971 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5289263 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5418842 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5289203 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5410703 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5405993 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5398139 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5397368 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5393246 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5299541 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5306135 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5388104 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5288909 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5288795 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5280911 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5281124 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5275406 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5274794 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5273669 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5271131 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5300645 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5243648 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5224583 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5157110 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5131490 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5078857 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5027623 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5001040 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4970251 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4961983 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4961866 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4769162 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4739084 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4739069 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4732214 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4663620 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4571190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4547199 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4477547 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4397906 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4397852 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4397798 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4390220 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4357454 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4354847 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4310331 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4275732 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4275570 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4257072 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4256454 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4233648 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4226331 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4221216 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4220346 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4213491 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4206663 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4093030 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4076539 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4050592 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4040191 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4023082 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022245 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022230 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022194 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022167 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022155 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022107 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4014772 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4014718 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3881821 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3849253 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3976246 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3955225 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3951889 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3921025 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3909631 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3909304 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3895525 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3895483 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3891784 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3853381 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3759301 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3836458 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3816571 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3812788 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3811393 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3804157 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3778060 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3770806 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3768874 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3747385 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3696725 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3681789 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3559115 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3554540 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3547763 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3540701 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3538430 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3463502 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3439358 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3376748 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3340256 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3433448 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3289916 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3195998 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3190178 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3149402 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3113474 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3113444 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3113411 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3104099 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2885768 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2854196 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2765081 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2765054 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2756321 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2682719 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2631689 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2613560 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2613581 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2613569 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2557622 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2541809 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2533727 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2533667 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2515571 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2500907 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2459555 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2455541 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2437703 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2435501 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2420729 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2420663 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2391878 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2355743 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2321189 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2312270 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2312672 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2293106 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2290394 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2290184 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2267979 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2248605 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2204727 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2158986 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2095074 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1996833 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1974915 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1953720 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1894227 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1812262 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1799650 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1777162 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1759879 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1739399 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1725851 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1715711 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1711796 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1702442 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1614737 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1580666 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1562417 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1545023 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1535303 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1527218 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1524293 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1523843 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1524296 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1487563 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1487560 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1470121 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1468354 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1450612 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1449496 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1446028 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1446094 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1442278 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1440286 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1414384 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1414888 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1413175 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1480837 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1404214 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1403329 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1378846 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1357444 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1341667 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1339231 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1323775 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1323718 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1321276 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1321732 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1320703 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1318945 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1318936 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1318921 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1311436 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1311220 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1309483 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1309450 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1348210 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1294369 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1273585 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1273435 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1268584 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1235368 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6065662 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1182381 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1173919 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1170253 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1167121 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1161895 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1159875 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1153793 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1148640 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1133614 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1128067 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1125248 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1115773 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1104527 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1100237 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1097864 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1091059 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1090331 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1084322 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1075566 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1072950 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1072710 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1070829 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1065250 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1065189 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1017942 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1017988 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1000620 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
988462 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
971527 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
964759 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
964754 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
962349 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
950566 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
928776 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
915428 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
903891 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
900796 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
897945 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
897893 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
881764 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
876190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
875686 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
918168 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
869863 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
865547 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
860838 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
855347 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
848514 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
843473 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
785906 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
780260 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
778314 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
776018 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
834228 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
767598 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
759661 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
759144 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
757004 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
750135 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
746872 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
746196 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
834229 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
733557 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
732320 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
730010 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
729995 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
730006 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
729988 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
834234 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
723393 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
722806 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
722874 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
719932 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
699716 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
699675 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
697997 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
695649 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
670840 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
657265 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
646743 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
646682 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
646515 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
632861 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
602345 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
576426 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
527245 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
463853 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
234935 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
197139 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
197137 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
197136 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3409133 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
127265 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
254330 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13083189 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
12374919 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
11570538 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
9607820 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
9607805 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
8055367 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
8051851 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
Traceback (most recent call last):
  File "/Users/cat/PycharmProjects/CorpusLinguisticsClass/Standalone corpus linguistics/main.py", line 573, in <module>
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale.txt"), os.path.join(proj_dir, "Fanfic_all"))
  File "/Users/cat/PycharmProjects/CorpusLinguisticsClass/Standalone corpus linguistics/main.py", line 335, in freqdist_from_idfile
    this_freqdist = freq_from_txt(name, case_sensitive)
  File "/Users/cat/PycharmProjects/CorpusLinguisticsClass/Standalone corpus linguistics/main.py", line 291, in freq_from_txt
    freqdist = freq_from_str(f_in.read(), case_senstive)
  File "/Users/cat/PycharmProjects/CorpusLinguisticsClass/Standalone corpus linguistics/main.py", line 260, in freq_from_str
    words = [word for word in nltk.word_tokenize(text.lower()) if
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/__init__.py", line 106, in word_tokenize
    return [token for sent in sent_tokenize(text, language)
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/__init__.py", line 91, in sent_tokenize
    return tokenizer.tokenize(text)
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/punkt.py", line 1226, in tokenize
    return list(self.sentences_from_text(text, realign_boundaries))
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/punkt.py", line 1274, in sentences_from_text
    return [text[s:e] for s, e in self.span_tokenize(text, realign_boundaries)]
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/punkt.py", line 1265, in span_tokenize
    return [(sl.start, sl.stop) for sl in slices]
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/punkt.py", line 1265, in <listcomp>
    return [(sl.start, sl.stop) for sl in slices]
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/punkt.py", line 1304, in _realign_boundaries
    for sl1, sl2 in _pair_iter(slices):
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/punkt.py", line 311, in _pair_iter
    for el in it:
  File "/anaconda/lib/python3.5/site-packages/nltk/tokenize/punkt.py", line 1278, in _slices_from_text
    for match in self._lang_vars.period_context_re().finditer(text):
KeyboardInterrupt

Process finished with exit code 1

"""

"""
dw_remove = ["10500279", "9051955", "6163238", "6157525", "6060937", "13346448", "13162389", "13150815", "13190844", "13042899",
             "13045944", "12996450", "12870165", "12564708", "12286731", "12286785", "12284460", "11977479", "12027435", "11903901",
             "11803812", "11703900", "11625312", "11532309", "11510115", "11494026", "11412099", "11368038", "11315433", "11307960",
             "11295315", "11297718", "11080263", "11211402", "11188680", "11109816", "11141952", "11059938", "11059896", "11109894",
             "11037063", "11036334", "11027655", "11020227", "11020134", "11016960", "10950537", "10941576", "10925733", "10894737",
             "10894710", "10875825", "10875732", "10873854", "10865232", "10858599", "10857390", "11157849", "10716399", "10539135",
             "10452402", "10344270", "10237538", "10232798", "9694574", "11142150", "9108235", "9062875", "7921630", "10468848",
             "7344757", "7211777", "6424531", "6275809", "6091024", "5709103", "5664376", "5664343", "5608507", "5516012", "5509559",
             "5528387", "5352920", "5033050", "11110056", "4863320", "4795886", "4779395", "4698098", "4637157", "4564311", "4368707",
             "4264461", "4205280", "4037497", "3957667", "3945808", "3838843", "3646056", "3066143", "2653757", "2581445", "2420279",
             "2311955", "2259009", "2102448", "2102412", "2102397", "2102481", "2102373", "2102514", "2102583", "2102343", "2102379",
             "2102355", "2102466", "2102529", "2102442", "2102295", "2102577", "2102565", "2102286", "2102547", "2102268", "2097000",
             "2096982", "2097132", "2096970 ", "2097360", "2097405", "2097366", "2097246", "2097330", "2097171", "2097063", "2097294",
             "2097117", "2097270", "2097390", "2097078", "2097165", "2097420", "2097507", "2097216", "2097285", "2097588", "2097456",
             "2097072", "2097060", "2097483", "2097192", "2091216", "2091684", "2091456", "2091588", "2092233", "2091831", "2091999",
             "2091855", "2091672", "2091987", "2091747", "2091153", "2091918", "2092098", "2091552", "2092194", "2091615",
             "2092203", "2091192", "2091471", "2091111", "2091969", "2091060", "2091495", "2091483", "2091159", "2091138",
             "2092299", "2091537", "2091513", "2091537", "2092143", "2091765", "2091900", "2091075", "2092167", "2091936",
             "2091126", "2091645", "2092263", "2091018", "2091984", "2091876", "2091174", "2092266", "2091078", "2091864",
             "2092122", "2092305", "2092254", "2092089", "2092173", "2091144", "2092065", "2091093", "2092041", "2092281",
             "2091447", "2091909", "2091423", "2091531", "2091675", "2091846", "2091663", "2090994", "2091000", "2091726",
             "2091606", "2091699", "2091822", "2086161", "2086197", "2085990", "2015838", "1985223", "1763343", "1736504 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1736474 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1579037 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1720031 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1697489 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1654649 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1651742 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1551194 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1473331 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1464757 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318867 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318858 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318843 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318810 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1110732 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1104835 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1098550 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1053890 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
990949 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
985139 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144332 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
948570 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
947275 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
912879 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
911351 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
909778 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902513 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902510 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902501 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902496 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902490 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902486 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902482 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902479 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902476 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902471 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902468 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902438 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902425 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144269 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1117861 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144248 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834223 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
833936 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
918190 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144215 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
803620 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
803629 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
789844 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
762273 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9578879 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834219 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834211 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
693840 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
643594 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
633903 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
625265 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
623189 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
620174 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
620169 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681304 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834204 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834201 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834195 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
532601 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
524077 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
508646 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
502149 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
476447 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144029 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
431948 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681289 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
412824 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
391300 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1893309 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3143849 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
332368 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
332351 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
325417 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9610910 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9610769 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9662114 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681279 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9578228 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681275 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681271 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681265 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
253468 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681252 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
235044 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
199758 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9577883 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3143819 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
151936 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
151915 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
151138 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
93119 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
92525 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
91909 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
91696 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1905102 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1904502 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5098 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
489371 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10954374 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt"


10500279 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
9051955 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
6163238 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
6157525 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
6060937 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
13346448 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13162389 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13150815 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13190844 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13042899 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13045944 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12996450 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12870165 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12564708 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12286731 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12286785 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12284460 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11977479 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
12027435 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11903901 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11803812 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11703900 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11625312 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11532309 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11510115 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11494026 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11412099 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11368038 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11315433 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11307960 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11295315 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11297718 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11080263 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11211402 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11188680 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11109816 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11141952 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11059938 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11059896 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11109894 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11037063 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11036334 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11027655 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11020227 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11020134 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11016960 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10950537 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10941576 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10925733 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10894737 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10894710 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10875825 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10875732 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10873854 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10865232 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10858599 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10857390 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11157849 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10716399 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10539135 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10452402 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10344270 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10237538 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10232798 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9694574 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11142150 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9108235 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9062875 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
7921630 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10468848 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
7344757 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
7211777 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
6424531 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
6275809 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
6091024 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5709103 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5664376 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5664343 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5608507 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5516012 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5509559 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5528387 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5352920 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5033050 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
11110056 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4863320 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4795886 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4779395 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4698098 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4637157 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4564311 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4368707 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4264461 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4205280 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
4037497 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3957667 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3945808 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3838843 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3646056 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3066143 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2653757 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2581445 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2420279 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2311955 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2259009 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102448 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102412 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102397 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102481 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102373 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102514 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102583 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102343 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102379 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102355 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102466 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102529 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102442 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102295 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102577 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102565 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102286 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102547 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2102268 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097000 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2096982 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097132 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2096970 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097360 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097405 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097366 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097246 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097330 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097171 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097063 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097294 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097117 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097270 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097390 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097078 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097165 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097420 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097507 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097216 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097285 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097588 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097456 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097072 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097060 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097483 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2097192 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091216 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091684 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091456 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091588 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092233 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091831 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091999 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091855 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091672 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091987 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091747 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091153 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091918 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092098 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091552 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092194 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091615 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092203 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091192 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091471 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091111 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091969 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091060 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091495 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091483 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091159 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091138 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092299 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091537 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091513 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091537 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092143 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091765 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091900 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091075 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092167 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091936 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091126 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091645 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092263 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091018 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091984 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091876 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091174 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092266 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091078 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091864 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092122 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092305 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092254 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092089 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092173 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091144 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092065 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091093 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092041 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2092281 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091447 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091909 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091423 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091531 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091675 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091846 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091663 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2090994 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091000 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091726 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091606 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091699 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2091822 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2086161 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2086197 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2085990 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
2015838 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1985223 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1763343 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1736504 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1736474 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1579037 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1720031 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1697489 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1654649 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1651742 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1551194 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1473331 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1464757 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318867 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318858 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318843 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1318810 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1110732 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1104835 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1098550 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1053890 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
990949 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
985139 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144332 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
948570 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
947275 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
912879 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
911351 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
909778 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902513 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902510 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902501 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902496 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902490 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902486 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902482 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902479 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902476 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902471 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902468 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902438 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
902425 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144269 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1117861 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144248 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834223 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
833936 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
918190 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144215 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
803620 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
803629 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
789844 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
762273 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9578879 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834219 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834211 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
693840 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
643594 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
633903 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
625265 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
623189 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
620174 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
620169 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681304 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834204 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834201 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
834195 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
532601 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
524077 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
508646 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
502149 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
476447 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3144029 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
431948 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681289 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
412824 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
391300 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1893309 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3143849 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
332368 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
332351 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
325417 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9610910 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9610769 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9662114 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681279 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9578228 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681275 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681271 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681265 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
253468 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
681252 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
235044 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
199758 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
9577883 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
3143819 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
151936 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
151915 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
151138 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
93119 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
92525 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
91909 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
91696 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1905102 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
1904502 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
5098 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
489371 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
10954374 /Volumes/2TB/Final_Project/Fanfic lists/New Who.txt
13278189 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13325424 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13222062 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13221975 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13172514 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12903456 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12724581 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12257427 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12215016 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12144471 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11965590 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11963226 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11963133 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11851005 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11703957 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11597337 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11594424 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
11006187 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10994832 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10694073 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10861974 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10837317 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10808076 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10801716 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10701651 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10701294 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10675533 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10572321 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10540755 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10355619 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10342764 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10262447 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10225031 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10165913 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9984788 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9953198 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9949661 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9949355 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9949250 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9925046 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9857927 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9697016 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9696665 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9529388 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9498848 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9295424 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9293888 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9219842 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8939704 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8843515 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8748226 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8696662 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8599879 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8569939 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8498938 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8483692 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8412091 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8396629 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8419117 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8339359 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8337628 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8332564 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8156506 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8153468 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8039770 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8037436 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8017099 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7996621 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7892617 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8172460 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7759042 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7757248 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7614352 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7614286 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7599382 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7534021 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7524934 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7347916 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7192613 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7188119 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
7186865 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6822550 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6738346 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6517051 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6503914 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6497197 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6495838 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6349330 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6349213 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6290860 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6115714 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6061195 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6049723 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
6034672 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5979859 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5738446 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5717572 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5496968 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5298962 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5235146 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5139521 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4851407 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4668143 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4512213 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4402820 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4327422 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
4306224 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3664431 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3645915 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3574277 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3350675 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3325001 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3253052 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
3156437 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812655 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812634 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812472 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2812391 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2811881 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2717381 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2717372 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2627288 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2289590 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2262681 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2244114 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2134059 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2017044 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1856389 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1807885 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1802026 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1764927 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1700891 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1662125 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1662074 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1619549 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1613240 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1579826 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1417810 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1333234 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1333153 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1333096 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1275334 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
2289626 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1235470 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1220599 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1148672 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1179432 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1178571 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1175297 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1174344 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1142705 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1116672 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1104778 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1103103 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1081778 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1080831 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1075614 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1047568 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1044295 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1017768 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
1005767 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
955445 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
955380 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
955436 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
950805 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
947441 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
942392 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
881543 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
881837 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
860634 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
857738 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
856327 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
856163 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
854766 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
851210 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
848335 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
844920 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
842878 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
839158 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
833563 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
825222 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
825174 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
807713 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
788882 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
918203 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
706973 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
687598 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
665505 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
592289 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
580323 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
580315 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
580312 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
579696 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
564373 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
556207 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
556203 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
540816 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
526872 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
514302 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
514298 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
514294 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
508610 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
499361 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
459775 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
388598 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
357591 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
343257 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9421379 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12269043 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12268917 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12268875 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360705 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
265047 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
261221 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
261215 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12365814 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9420917 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338774 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338693 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360712 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338618 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
12365871 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9420791 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9338549 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
152017 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
152016 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
152015 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
152013 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
152011 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
152004 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
151992 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
151988 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360716 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360723 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360724 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360734 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
196212 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9421004 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360744 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360747 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360750 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
360758 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
9337631 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
10902519 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5051194 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
263931 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
489240 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
8075698 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
5738755 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
643511 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
879304 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
495741 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
879324 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
879360 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
842022 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
839489 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
846732 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
839495 /Volumes/2TB/Final_Project/Fanfic lists/Star Trek.txt
13357866 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13340919 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13290900 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13206963 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13137519 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13134705 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13124190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13054566 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13053270 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13051491 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13048104 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13032366 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12781986 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12756987 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12581648 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12571928 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12486216 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12461229 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12300204 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12397731 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12327207 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12294081 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12117948 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
12082554 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11876682 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11875287 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11754501 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11689590 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11689521 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11630385 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11548797 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11520741 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11518569 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11482380 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11425500 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11373495 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11341530 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11292567 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11224098 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9585374 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11133681 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11062683 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10928952 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10829103 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10679217 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10637232 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10628154 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10387416 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10329893 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10313288 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10101023 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10077530 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9815480 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9753317 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9570020 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9457946 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9160954 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
9062578 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8857234 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8886931 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8881417 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8828794 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8799877 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8559196 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8484241 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8300677 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8250994 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8237033 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8151250 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8148449 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8131439 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
8130914 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7450816 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7434142 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7286134 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7266157 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7245934 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7165832 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
7024864 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6975934 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6951454 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6919345 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6779254 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6779185 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6779218 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6604852 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6574159 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6559408 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6485671 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6474076 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6359083 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6349186 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6349012 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6341734 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6334564 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6177070 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6170371 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147694 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147685 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147664 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6147619 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6097132 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5996962 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5975575 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5975539 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5932311 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5902402 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5878291 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5830507 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5645590 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5524313 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5520581 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5489585 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5479157 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5300081 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5340185 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5470190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5450804 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5457578 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5395328 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5443514 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5392769 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5255795 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5290115 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5408627 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5431598 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5430740 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5424971 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5289263 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5418842 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5289203 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5410703 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5405993 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5398139 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5397368 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5393246 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5299541 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5306135 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5388104 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5288909 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5288795 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5280911 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5281124 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5275406 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5274794 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5273669 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5271131 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5300645 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5243648 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5224583 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5157110 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5131490 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5078857 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5027623 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
5001040 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4970251 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4961983 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4961866 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4769162 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4739084 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4739069 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4732214 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4663620 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4571190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4547199 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4477547 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4397906 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4397852 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4397798 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4390220 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4357454 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4354847 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4310331 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4275732 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4275570 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4257072 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4256454 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4233648 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4226331 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4221216 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4220346 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4213491 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4206663 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4093030 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4076539 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4050592 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4040191 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4023082 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022245 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022230 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022194 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022167 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022155 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4022107 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4014772 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
4014718 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3881821 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3849253 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3976246 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3955225 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3951889 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3921025 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3909631 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3909304 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3895525 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3895483 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3891784 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3853381 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3759301 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3836458 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3816571 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3812788 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3811393 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3804157 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3778060 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3770806 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3768874 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3747385 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3696725 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3681789 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3559115 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3554540 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3547763 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3540701 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3538430 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3514553 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3463502 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3439358 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3403682 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3376748 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3340256 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3433448 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3289916 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3195998 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3190178 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3149402 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3113474 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3113444 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3113411 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3104099 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2885768 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2854196 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2826980 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2765081 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2765054 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2756321 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2682719 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2631689 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2613560 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2613581 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2613569 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2557622 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2541809 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2533727 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2533667 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2515571 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2500907 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2459555 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2455541 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2437703 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2435501 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2420729 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2420663 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2391878 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2355743 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2321189 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2312270 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2312672 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2293106 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2290394 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2290184 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2267979 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2248605 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2204727 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2158986 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
2095074 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1996833 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1974915 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1953720 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1894227 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3777760 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1812262 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1799650 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1777162 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1759879 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1739399 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1725851 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1715711 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1711796 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1702442 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1614737 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1580666 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1562417 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1545023 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1535303 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1527218 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1524293 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1523843 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1524296 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1487563 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1487560 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1470121 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1468354 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1450612 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1449496 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1446028 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1446094 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1442278 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1440286 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1414384 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1414888 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1413175 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1480837 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1404214 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1403329 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1378846 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1357444 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1341667 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1339231 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1323775 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1323718 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1321276 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1321732 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1320703 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1318945 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1318936 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1318921 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1311436 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1311220 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1309483 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1309450 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1348210 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1294369 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1273585 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1273435 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1268584 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1235368 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
6065662 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1182381 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1173919 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1170253 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1167121 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1161895 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1159875 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1153793 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1148640 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1133614 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1128067 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1125248 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1115773 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1104527 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1100237 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1097864 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1091059 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1090331 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1084322 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1075566 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1072950 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1072710 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1070829 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1065250 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1065189 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1017942 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1017988 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
1000620 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
988462 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
971527 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
964759 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
964754 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
962349 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
950566 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
928776 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
915428 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
903891 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
900796 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
897945 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
897893 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
881764 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
876190 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
875686 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
918168 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
869863 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
865547 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
860838 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
855347 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
848514 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
843473 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
785906 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
780260 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
778314 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
776018 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
834228 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
767598 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
759661 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
759144 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
757004 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
750135 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
746872 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
746196 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
834229 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
733557 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
732320 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
730010 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
729995 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
730006 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
729988 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
834234 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
723393 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
722806 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
722874 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
719932 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
699716 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
699675 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
697997 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
695649 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
670840 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
657265 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
646743 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
646682 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
646515 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
632861 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
602345 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
576426 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
527245 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
463853 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
234935 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10555436 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11096259 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11162670 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
197139 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
197137 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
197136 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
3409133 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
127265 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
10555630 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11162817 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
11162742 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
254330 /Volumes/2TB/Final_Project/Fanfic lists/Tolkien.txt
13083189 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
12374919 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
6275314 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
11570538 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
11120127 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
11073834 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
9607820 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
9607805 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
8055367 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
8051851 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
6551428 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
6088168 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
6057997 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
4981594 /Volumes/2TB/Final_Project/Fanfic lists/Undertale.txt
"""

"""

Tolkien (new)
620630
Star Trek (old)
9338774 <FreqDist with 0 samples and 0 outcomes>
9338693 <FreqDist with 0 samples and 0 outcomes>
9338618 <FreqDist with 0 samples and 0 outcomes>
9338549 <FreqDist with 0 samples and 0 outcomes>
9337631 <FreqDist with 0 samples and 0 outcomes>
8075698 <FreqDist with 0 samples and 0 outcomes>
"""

"""
10500279 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
9051955 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
6163238 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
6157525 /Volumes/2TB/Final_Project/Fanfic lists/Hamilton.txt
"""