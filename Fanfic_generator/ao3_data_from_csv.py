import csv
import os
import math
import openpyxl
import operator
import re
import numpy as np
import matplotlib.pyplot as plt
import time

stats = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'language',
         'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits', 'body']

csv.field_size_limit(1000000000)  # sys.maxsize


def ao3_txt_from_csv(csv_in, path, lang="English", restart=0, end=0):
    """
    Gets the text of each fanfic from a csv file created using ao3_get_fanfics.py
    :param csv_in: the name of a csv file created using ao3_get_fanfics.py
    :param path: path to where you want to store the txt files
    :param restart: the id to restart at
    :return:
    """
    f_in = open(csv_in, 'r+')
    reader = csv.reader(f_in)
    try:
        os.chdir(path)
    except FileNotFoundError:
        os.mkdir(path)
        os.chdir(path)
    next(reader, None)  # skip the headers
    if restart:
        found = False
    else:
        found = True
    for row in reader:
        work_id = row[0]  # stats.index("work_id")
        """if end and int(work_id) == end:
            break"""
        if restart and not found:
            id_ = int(work_id)
            if id_ == restart:
                found = True
                print("found", id_)
            else:
                print("skipping already processed fic")
        if found:
            print("ao3_txt_from_csv processing", work_id)
            if row[8] == lang:
                # print(work_id)
                fandom = row[4]
                # print(fandom)
                filename = work_id + ".txt"
                if os.path.isfile(filename):
                    outfile = open(filename, "w")
                    outfile.write(row[-1])  # stats.index("body")
                    outfile.close()
            else:
                print(work_id, row[8])
    f_in.close()


def ao3_count_stats_from_csv(csv_in):
    """
    Counts the statistics from a csv file created using ao3_get_fanfics.py
    :param csv_in: the name of a csv file created using ao3_get_fanfics.py
    :return: a dictionary containing the instances of each statistic and their frequencies
    """
    f_in = open(csv_in, 'r+')
    reader = csv.reader(f_in)
    header = next(reader)  # change if Sherlock
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'language', 'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits', 'body']
    # header = {stat: stat_names.index(stat) for stat in stat_names}
    header = {stat: header.index(stat) for stat in header}
    for stat in ["work_id", "language", "body"]:  # TODO: add comments later
        del header[stat]  # remove the stats we don't care about
    stats = {stat: {} for stat in header}
    for row in reader:
        # print(row)
        for stat in stats:
            row_stat = row[header[stat]]
            if row_stat == 'null' or row_stat == '':
                row_stat = 0
            if stat in ["words", "kudos", "bookmarks", "comments", "hits"]:  # TODO: put chapters back later
                row_stat = int(row_stat)
                if stat == "words":
                    row_stat = (math.ceil(int(row_stat) / 100.0)) * 100
                elif stat == "hits":
                    row_stat = (math.ceil(int(row_stat) / 10.0)) * 10
            current_entry = stats[stat]
            if row_stat in current_entry:
                current_entry[row_stat] += 1
            else:
                current_entry[row_stat] = 1
    f_in.close()
    return stats


def new_csv(csv_in, csv_out):
    f_in = open(csv_in, 'r+')
    f_out = open(csv_out, 'w')
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    # header = next(reader)
    # writer.writerow(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits']  # no column for body
    writer.writerow(stat_names)
    header = {stat: stat_names.index(stat) for stat in stat_names}
    # print(header)
    # header = {stat: header.index(stat) for stat in header}
    fanfic_dir = "/Volumes/2TB/Final_project/Fanfic_all"
    ids_seen = []
    for row in reader:
        if row[0] == "work_id":
            continue
        word_count = row[header["words"]]
        idname = row[header['work_id']]
        if word_count != 'null' and word_count != '' and word_count != 0 and word_count != "0":
            if idname in ids_seen:
                continue
            try:
                txt_in = open(os.path.join(fanfic_dir, str(row[0]) + ".txt"))
                for i in range(20):
                    if re.search('[a-zA-Z]', txt_in.readline()):  # search the first 20 lines for letters
                        writer.writerow(row[:len(row) - 1])  # don't need to write the body of the fic
                        ids_seen.append(idname)
                        break
                else:  # couldn't find letters
                    print(csv_in, row[0], end=", ")
                txt_in.close()
            except FileNotFoundError:
                print(csv_in, row[0], end="! ")
        else:
            print(csv_in, row[0], end="* ")
    print()


def remove_ids(csv_in, csv_out, idlist):
    f_in = open(csv_in, 'r+')
    f_out = open(csv_out, 'w')
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    header = next(reader)
    writer.writerow(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits']  # no column for body
    writer.writerow(stat_names)
    header = {stat: stat_names.index(stat) for stat in stat_names}
    # print(header)
    # header = {stat: header.index(stat) for stat in header}
    fanfic_dir = "/Volumes/2TB/Final_project/Fanfic_all"
    for row in reader:
        id = row[header["work_id"]]
        if int(id) not in idlist:
            try:
                txt_in = open(os.path.join(fanfic_dir, str(row[0]) + ".txt"))
                for i in range(20):
                    if re.search('[a-zA-Z]', txt_in.readline()):  # search the first 20 lines for letters
                        writer.writerow(row[:len(row) - 1])  # don't need to write the body of the fic
                        break
                else:  # couldn't find letters
                    print(csv_in, row[0], end=", ")
                txt_in.close()
            except FileNotFoundError:
                print(csv_in, row[0], end="! ")
        else:
            print(csv_in, row[0], end="* ")
    print()


def get_numwords_ids(csv_in, out_txt_name, min_words, max_words):
    """
    Get fics with the specified number of words.
    :param csv_in:
    :param out_txt_name:
    :param min_words: inclusive
    :param max_words: inclusive
    :return:
    """
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'a+')
    reader = csv.reader(f_in)
    header = next(reader)
    print(header)
    header = {stat: header.index(stat) for stat in header}
    for row in reader:
        try:
            word_count = int(row[header["words"]])
        except ValueError:
            continue
        if word_count == 'null' or word_count == '':
            continue
        if min_words <= word_count <= max_words:
            f_out.write(row[header["work_id"]])
            f_out.write("\n")


def get_rating_ids(csv_in, out_txt_name, rating):
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        rating_str = row[header['rating']]
        if rating_str == 'null' or rating_str == '':
            continue
        if rating_str == rating:
            f_out.write(row[header['work_id']])
            f_out.write("\n")
    f_in.close()
    f_out.close()


def get_0_word_ids(csv_in, out_txt_name):
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'a+')
    reader = csv.reader(f_in)
    header = next(reader)
    print(header)
    header = {stat: header.index(stat) for stat in header}
    for row in reader:
        word_count = row[header["words"]]
        if word_count == 'null' or word_count == '':
            f_out.write(row[header["work_id"]])
            f_out.write("\n")


def get_fandom_ids(csv_in, out_txt_name, fandom_list):
    """
    Get all the ids of fics including one or more fandoms in the fandom list, but no fandoms not in the list
    :param csv_in:
    :param out_txt_name:
    :param fandom_list:
    :return:
    """
    # New Who: ["Doctor Who", "Doctor Who (2005)", "Doctor Who & Related Fandoms"]
    # Hamilton: ["Hamilton - Miranda", "Hamilton - Fandom", "Historical RPF", "18th & 19th Century CE RPF", "American Revolution RPF"
    # "Hamilton-Miranda", "18th Century CE RPF", "19th Century CE RPF", "Hamilton- Miranda", "Alexander Hamilton - Ron Chernow"]
    # Les Mis: ["Les Miserables - All Media Types", "Les Miserables - Victor Hugo", "Les Miserables (2012)", "Les Miserables - Schonberg/Boublil",
    # "Les Miserables", "Les Miserables (Dallas 2014)", "les mis"]
    # Sherlock: ["Sherlock (TV)", "Sherlock Holmes & Related Fandoms", "Elementary (TV)", "Elementary", "Sherlock Holmes - Arthur Conan Doyle",
    # "Sherlock - Fandom", "Sherlock BBC", "BBC Sherlock", "Sherlock Holmes (2009)", "Sherlock Holmes (Downey films)",
    # "Sherlock Holmes (1984 TV)", "Sherlock Holmes - Doyle"]
    # Star Trek: ["Star Trek: Alternate Original Series (Movies)", "Star Trek (2009)", "Star Trek: Voyager", "Star Trek: Enterprise",
    # "Star Trek: The Original Series", "Star Trek: Deep Space Nine", "Star Trek: The Next Generation", "Star Trek",
    # "Star Trek: Discovery", "Star Trek XI", "Star Trek: 2009", "Star Trek: Mirror Universe", "Star Trek Voyager",
    # "StarTrek: Voyager", "Star Trek Into Darkness - Fandom", "Star Trek: Into Darkness - Fandom", "Star Trek Reboot",
    # "Star Trek AOS", "Star Trek Enterprise", "StarTrek: Enterprise", "Star Trek - Various Authors", "Star Trek Online",
    # "ST:AOS - Fandom", "StarTrek: The Next Generation", "Star Trek Into Darkness - Fandom", "Star Trek The Next Generation"]
    # Tolkien: ["The Hobbit - All Media Types", "The Silmarillion and other histories of Middle-Earth - J. R. R. Tolkien",
    # "The Lord of the Rings - J. R. R. Tolkien", "The Hobbit (Jackson Movies)", "The Hobbit - J. R. R. Tolkien",
    # "The Lord of the Rings - All Media Types", "The Hobbit (2012)", "TOLKIEN J. R. R. - Works & Related Fandoms",
    # "Lord of the Rings (2001 2002 2003)", "The Lord of the Rings (Movies)", "Lord of the Rings - Fandom", "Lord of the Rings - Tolkien",
    # "The Hobbit" ]
    # Undertale: ["Undertale (Video Game)", "Undertale", "Underfell - Fandom", "Undertail - Fandom", "Undertail - Fandom", "underswap"]

    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        fandom_str = row[header['fandom']]
        if fandom_str == 'null' or fandom_str == '':
            continue
        fandoms = fandom_str.split(", ")
        for fandom in fandoms:
            if fandom not in fandom_list:
                break
        else:  # if all fandoms were in the valid list
            f_out.write(row[header['work_id']])
            f_out.write("\n")
    f_in.close()
    f_out.close()


def get_csv_ids(csv_in, out_txt_name):
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        word_str = row[header['words']]
        if word_str == 'null' or word_str == '' or word_str == 0:
            continue
        f_out.write(row[header['work_id']])
        f_out.write("\n")
    f_in.close()


def get_fandom_group_ids(csv_in, out_txt_name, fandom_groups, num_to_match=1):  # TODO: fix this so it works
    """
    Get fics with at least one fandom from each group and no fandoms that aren't in any group
    :param csv_in:
    :param out_txt_name:
    :param fandom_groups: a list of groups of lists of fandoms (e.g., [["Harry Potter", "HP"], ["Merlin (TV)", "BBC Merlin"], ["Supernatural"]]
                            assumption: the groups are disjoint.
    :param num_to_match: how many fandoms from each group must be matched
    :return:
    """
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        fandom_str = row[header['fandom']]
        if fandom_str == 'null' or fandom_str == '':
            continue
        fandoms = fandom_str.split(", ")
        group_counts = [[x, 0] for x in fandom_groups]  # create a multidimensional array to count the number of tags in each category
        other_fandoms = False  # set a flag for if other fandoms are found
        for fandom in fandoms:
            found = False  # track if the fandom has been found in any of the groups
            for i in range(len(group_counts)):
                group, freq = group_counts[i]
                if fandom in group:
                    freq += 1
                    found = True
            if not found:
                other_fandoms = True
                break
        if not other_fandoms:
            for i in range(len(group_counts)):
                if group_counts[i][1] < num_to_match:  # if not enough fandoms in each group have been found
                    break
            else:
                f_out.write(row[header['work_id']])
                f_out.write("\n")
    f_in.close()
    f_out.close()


def get_category_ids(csv_in, out_txt_name, categories):
    """
    Get all the ids of fics with all of the relationship categories specified
    :param csv_in:
    :param out_txt_name:
    :param categories:
    :return:
    """
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        category_str = row[header['category']]
        if category_str == 'null' or category_str == '':
            continue
        category_list = category_str.split(", ")
        categories.sort()
        category_list.sort()
        if categories == category_list:  # if the lists of categories are identical
            f_out.write(row[header['work_id']])
            f_out.write("\n")
    f_in.close()
    f_out.close()


def get_tag_ids(csv_in, out_txt_name, tags, num=1, exact=False, others=True):  # TODO: change for else
    """
    Get all the ids of fics that match at least (num) of the tags specified
    :param csv_in:
    :param out_txt_name:
    :param num:
    :param tags:
    :param exact: if True, the tag must match exactly. Otherwise, just search for the specified tags
    :param others: if True, no other tags are allowed
    :return:
    """
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        tag_str = row[header['additional tags']]
        if tag_str == 'null' or tag_str == '':
            continue
        num_found = 0
        if exact:
            tag_list = tag_str.split(", ")
            if not others:
                for tag in tag_list:
                    if tag not in tags:
                        break
                    else:
                        num_found += 1
                else:
                    if num_found >= num:  # if no invalid tags present and enough valid tags found
                        f_out.write(row[header['work_id']])
                        f_out.write("\n")
            else:
                for tag in tags:
                    if tag in tags:
                        num_found += 1  # TODO: improve the fact that we keep looking when we don't need to
                if num_found >= num:  # if enough valid tags found
                    f_out.write(row[header['work_id']])
                    f_out.write("\n")
        else:
            if others:
                for tag in tags:
                    if tag in tag_str:
                        num_found += 1
                if num_found >= num:  # if enough of the tags are in the string
                    f_out.write(row[header['work_id']])
                    f_out.write("\n")
            else:
                tag_list = tag_str.split(", ")
                for tag in tags:
                    if tag in tag_str:
                        num_found += 1
                if num_found >= num and num_found == len(tag_list):  # this means no other tags exist
                    f_out.write(row[header['work_id']])
                    f_out.write("\n")
    f_in.close()
    f_out.close()


def get_status_ids(csv_in, out_txt_name, status):
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        if row[header['status']] == status:  # if the lists of categories are identical
            f_out.write(row[header['work_id']])
            f_out.write("\n")
    f_in.close()
    f_out.close()


def get_published_year_ids(csv_in, out_txt_name, year):
    if type(year) != str:
        year = str(year)
    f_in = open(csv_in, 'r+')
    f_out = open(out_txt_name, 'w')
    reader = csv.reader(f_in)
    header = next(reader)
    # print(header)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for row in reader:
        if year in row[header['published']]:  # if the lists of categories are identical
            f_out.write(row[header['work_id']])
            f_out.write("\n")
    f_in.close()
    f_out.close()


def store_stats(stat_dict, filename, stat_tup = ('title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits')):
    wb = openpyxl.Workbook()
    ws = wb.active  # get a handle to the sheet in the workbook
    ws['A1'] = "AO3 stats"
    for col in range(1, len(stat_tup) * 2 + 1, 2):
        stat = stat_tup[(col - 1) // 2]
        print(stat, end="... ")
        entry = stat_dict[stat]
        entry_list = sorted(entry.items(), key=operator.itemgetter(1), reverse=True)
        ws.cell(row=2, column=col).value = stat
        for row in range(3, len(entry_list) + 3):  # this number is equal to the number of unique words with that suffix
            idx = row - 3
            value = entry_list[idx][0]
            try:
                ws.cell(row=row, column=col).value = value
            except openpyxl.utils.exceptions.IllegalCharacterError:
                value = input(value + " invalid. New value: ")
                ws.cell(row=row, column=col).value = value
            ws.cell(row=row, column=col+1).value = entry_list[idx][1]  # frequency
        if not filename.endswith(".xlsx"):
            wb.save(filename + ".xlsx")  # add the type extension if not included
        else:
            wb.save(filename)


def numpy_stats(csv_in, stat_list, out_csv_name):
    f_in = open(csv_in, 'r+')
    reader = csv.reader(f_in)
    header = next(reader)
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    stat_dict = {}
    for stat in stat_list:
        stat_dict[stat] = {"array": [], "samples": 0, "mean": 0, "median": 0, "min": 0, "max": 0, "std": 0}
    counter = 0  # counter of ValueError where value == a key
    for row in reader:
        for stat in stat_list:
            try:
                value = row[header[stat]]
            except IndexError:
                # print("error in %s" % stat, row)
                # print(len(row))
                if stat == "hits":
                    value = (row[len(row) - 1])  # try this?
            try:
                value = int(value)
            except ValueError:
                if value == "null" or value == "":
                    value = 0
                elif value in stat_list:
                    counter += 1
                    value = 0
                else:
                    print("ValueError:", value)
                    return
            stat_dict[stat]["array"].append(value)
    print("keys found %d times" % counter)
    f_in.close()
    for stat in stat_list:
        entry = stat_dict[stat]
        entry["samples"] = len(entry["array"])  # easier to get len of list than get len of numpy array
        np_arr = np.array(entry["array"])
        entry["array"] = np_arr
        entry["mean"] = np.mean(np_arr)
        entry["median"] = np.median(np_arr)
        entry["min"] = np.amin(np_arr)
        entry["max"] = np.amax(np_arr)
        entry["std"] = np.std(np_arr)
    f_out = open(out_csv_name, "w")
    writer = csv.writer(f_out, delimiter='\t', quotechar='|')
    writer.writerow(["stat","samples","mean","median","minimum","maximum","standard deviation"])
    for stat in stat_list:  # iterate through list rather than dict to preserve order
        entry = stat_dict[stat]
        row = [stat, entry["samples"], entry["mean"], entry["median"], entry["min"],
                                                    entry["max"], entry["std"]]
        writer.writerow(row)
    f_out.close()
    return stat_dict


def get_anomaly_info(stat_csv):
    f_in = open(stat_csv)
    reader = csv.reader(f_in, delimiter="\t", quotechar='|')
    header = next(reader)
    stat_conds = {}
    for row in reader:
        stat, samples, mean, median, min, max, std = row
        mean = float(mean)
        std = float(std)
        stat_conds[stat] = (mean-std, mean+std)  # find the abnormally low and high values based on mean and standard deviation
    f_in.close()
    return stat_conds


def get_anomaly_ids(stat_conds, csv_in, outfiledict):
    """

    :param stat_conds:
    :param csv_in:
    :param outfiledict: maps stats (e.g., "comments") to the filenames to store this info in. "val" will be replaced with "hi" or "lo"
    :return:
    """
    stat_names = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character',
                  'additional tags',
                  'language',
                  'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks',
                  'hits',
                  'body']
    header = {stat: stat_names.index(stat) for stat in stat_names}
    for stat in stat_conds:
        print(stat)
        min, max = stat_conds[stat]
        lo_name = outfiledict[stat].replace("val", "lo")
        out_lo = open(lo_name, "w")
        out_hi = open(outfiledict[stat].replace("val", "hi"), "w")
        with open(csv_in) as f_in:
            reader = csv.reader(f_in)
            next(reader)
            for row in reader:
                value = row[header[stat]]
                try:
                    value = int(value)
                except ValueError:
                    value = 0
                if value < min:
                    out_lo.write(row[header['work_id']] + '\n')
                elif value > max:
                    out_hi.write(row[header['work_id']] + '\n')
        out_hi.close()
        out_lo.close()


def anomaly_hist(stat_dict):
    for stat in stat_dict:
        # print(row)
        entry = stat_dict[stat]
        array = entry["array"]
        plt.hist(array, bins=1000, range=(entry["min"], entry["max"]))
        plt.title(stat)
        plt.show()
        # input()  # wait for user to type something to move on


def only_english(csv_in, csv_out):
    f_in = open(csv_in, 'r+')
    f_out = csv.writer(open(csv_out, 'a'), delimiter=',')
    reader = csv.reader(f_in)
    header = next(reader)
    langidx = header.index("language")
    for row in reader:
        print("only_english processing", row[0])
        lang = row[langidx]
        if lang == "English":
            f_out.writerow(row)
    f_in.close()


def find_other_lang(csv_in, target):
    f_in = open(csv_in, 'r+')
    reader = csv.reader(f_in)
    header = next(reader)
    langidx = header.index("language")
    for row in reader:
        lang = row[langidx]
        if lang != target:
            print(row[0], lang)


def category_ids(proj_dir, fandoms, categories):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for category in categories:
            print(fandom, category)
            str_category = category.replace("/", "")
            get_category_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom), os.path.join(proj_dir, "Fanfic lists/%s %s.txt"
                    % (fandom, str_category)), [category])


def au_ids(proj_dir, fandoms):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        print(fandom, "AU")
        get_tag_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom), os.path.join(proj_dir, "Fanfic lists/%s AU.txt" % fandom),
                    ["Alternate Universe", "AU"], num=1, exact=False, others=True)


def other_tags_ids(proj_dir, fandoms, tags):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for tag in tags:
            print(fandom, tag)
            get_tag_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom),
                os.path.join(proj_dir, "Fanfic lists/%s %s.txt" % (fandom, tag.replace("/", " "))), [tag], num=1, exact=False, others=True)


def status_ids(proj_dir, fandoms, statuses):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for status in statuses:
            print(fandom, status)
            get_status_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom),
                           os.path.join(proj_dir, "Fanfic lists/%s %s.txt" %(fandom, status)), status)


def year_ids(proj_dir, fandoms, years):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for year in years:
            print(fandom, year)
            get_published_year_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom), os.path.join(proj_dir,
                    "Fanfic lists/%s %s.txt" % (fandom, year)), year)


def word_ids(proj_dir, fandoms, range_tuples):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for rtuple in range_tuples:
            print(fandom, rtuple)
            get_numwords_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" %_fandom),
                         os.path.join(proj_dir, "Fanfic lists/%s %d-%d.txt" % (fandom, rtuple[0], rtuple[1])), rtuple[0], rtuple[1])


def rating_ids(proj_dir, fandoms, ratings):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for rating in ratings:
            print(fandom, rating)
            get_rating_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom),
                   os.path.join(proj_dir, "Fanfic lists/%s %s.txt" % (fandom, rating)), rating)


def fandom_id_files(proj_dir):
    print("DW")
    get_fandom_ids(os.path.join(proj_dir, "CSV/Doctor_Who_edit.csv"), os.path.join(proj_dir, "Fanfic lists/New Who.txt"),
                   ["Doctor Who", "Doctor Who (2005)", "Doctor Who & Related Fandoms"])
    get_fandom_ids(os.path.join(proj_dir, "CSV/Doctor_Who_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Classic Who.txt"),
                   ["Doctor Who", "Doctor Who (1963)", "Doctor Who: Eighth Doctor Adventures - Various Authors", "Doctor Who & Related Fandoms"])
    print("H")
    get_fandom_ids(os.path.join(proj_dir, "CSV/Hamilton_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Hamilton.txt"),
                   ["Hamilton - Miranda", "Hamilton - Fandom", "Historical RPF", "18th & 19th Century CE RPF", "American Revolution RPF",
                    "Hamilton-Miranda", "18th Century CE RPF", "19th Century CE RPF", "Hamilton- Miranda", "Alexander Hamilton - Ron Chernow"])
    get_fandom_ids(os.path.join(proj_dir, "CSV/Les_Mis_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Les Mis.txt"),
                   ["Les Miserables - All Media Types", "Les Miserables - Victor Hugo", "Les Miserables (2012)",
                    "Les Miserables - Schonberg/Boublil", "Les Miserables", "Les Miserables (Dallas 2014)", "les mis"])
    print("SH")
    get_fandom_ids(os.path.join(proj_dir, "CSV/Sherlock_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Sherlock.txt"),
                   ["Sherlock (TV)", "Sherlock Holmes & Related Fandoms", "Elementary (TV)", "Elementary", "Sherlock Holmes - Arthur Conan Doyle",
                    "Sherlock - Fandom", "Sherlock BBC", "BBC Sherlock", "Sherlock Holmes (2009)", "Sherlock Holmes (Downey films)",
                    "Sherlock Holmes (1984 TV)", "Sherlock Holmes - Doyle"])
    print("SH BBC")
    get_fandom_ids(os.path.join(proj_dir, "CSV/Sherlock_edit.csv"), os.path.join(proj_dir, "Fanfic lists/BBC Sherlock.txt"),
                   ["Sherlock (TV)", "Sherlock Holmes & Related Fandoms", "Sherlock - Fandom", "Sherlock BBC", "BBC Sherlock"])
    print("ST")
    get_fandom_ids(os.path.join(proj_dir, "CSV/Star_Trek_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Star Trek.txt"), ["Star Trek: Alternate Original Series (Movies)", "Star Trek (2009)", "Star Trek: Voyager", "Star Trek: Enterprise", "Star Trek: The Original Series", "Star Trek: Deep Space Nine", "Star Trek: The Next Generation", "Star Trek",
    "Star Trek: Discovery", "Star Trek XI", "Star Trek: 2009", "Star Trek: Mirror Universe", "Star Trek Voyager",
        "StarTrek: Voyager", "Star Trek Into Darkness - Fandom", "Star Trek: Into Darkness - Fandom", "Star Trek Reboot",
        "Star Trek AOS", "Star Trek Enterprise", "StarTrek: Enterprise", "Star Trek - Various Authors", "Star Trek Online",
        "ST:AOS - Fandom", "StarTrek: The Next Generation", "Star Trek Into Darkness - Fandom", "Star Trek The Next Generation"])
    print("T")
    get_fandom_ids(os.path.join(proj_dir, "CSV/Tolkien_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Tolkien.txt"), ["The Hobbit - All Media Types", "The Silmarillion and other histories of Middle-Earth - J. R. R. Tolkien",
        "The Lord of the Rings - J. R. R. Tolkien", "The Hobbit (Jackson Movies)", "The Hobbit - J. R. R. Tolkien",
        "The Lord of the Rings - All Media Types", "The Hobbit (2012)", "TOLKIEN J. R. R. - Works & Related Fandoms",
        "Lord of the Rings (2001 2002 2003)", "The Lord of the Rings (Movies)", "Lord of the Rings - Fandom", "Lord of the Rings - Tolkien",
        "The Hobbit" ])
    print("U")
    get_fandom_ids(os.path.join(proj_dir, "CSV/Undertale_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Undertale.txt"), ["Undertale (Video Game)", "Undertale", "Underfell - Fandom", "Undertail - Fandom", "Undertail - Fandom", "underswap"])


def csv_id_files(proj_dir, fandoms):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        get_csv_ids(os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom),
                   os.path.join(proj_dir, "Fanfic lists/%s all.txt" % fandom))


def get_fandom_group_id_files(proj_dir):
    print("Wholock")
    get_fandom_group_ids(os.path.join(proj_dir, "CSV/Doctor_Who_edit.csv"), os.path.join(proj_dir, "Fanfic lists/Wholock.txt"),
                         [["Doctor Who", "Doctor Who (2005)", "Doctor Who & Related Fandoms", "Doctor Who (1963)", "Doctor Who: Eighth Doctor Adventures - Various Authors"],
                          ["Sherlock (TV)", "Sherlock Holmes & Related Fandoms", "Sherlock - Fandom", "Sherlock BBC", "BBC Sherlock"]])
    print("SuperWhoLock")
    get_fandom_group_ids(os.path.join(proj_dir, "CSV/Doctor_Who_edit.csv"), os.path.join(proj_dir, "Fanfic lists/SuperWhoLock.txt"),
                         [["Doctor Who", "Doctor Who (2005)", "Doctor Who & Related Fandoms", "Doctor Who (1963)", "Doctor Who: Eighth Doctor Adventures - Various Authors"],
                          ["Sherlock (TV)", "Sherlock Holmes & Related Fandoms", "Sherlock - Fandom", "Sherlock BBC", "BBC Sherlock"],
                          ["Supernatural"]])


def fandom_numpy_stats(proj_dir, fandoms):
    stat_tup = ("words", "comments", "kudos", "hits", "bookmarks")
    for fandom in fandoms:
        print(fandom)
        numpy_stats(os.path.join(proj_dir, "CSV/%s_edit.csv" % fandom.replace(" ", "_")), stat_tup, os.path.join(proj_dir,
                                                                    "CSV stats/%s num stats.csv" % fandom))


def fandom_anomaly_hist(proj_dir):
    stat_tup = ("words", "comments", "kudos", "hits", "bookmarks")
    fandoms = ("Doctor Who", "Les Mis", "Hamilton", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    for fandom in fandoms:
        print(fandom)
        np_stats = numpy_stats(os.path.join(proj_dir, "CSV/%s_edit.csv" % fandom.replace(" ", "_")), stat_tup, os.path.join(proj_dir,
                                                                    "CSV stats/%s num stats.csv" % fandom))
        anomaly_hist(np_stats)


def fandom_anomaly_ids(proj_dir, fandoms):
    stat_tup = ("words", "comments", "kudos", "hits", "bookmarks")
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        print(fandom)
        stat_conds = get_anomaly_info(os.path.join(proj_dir, "CSV stats/%s num stats.csv" % fandom))
        outfiledict = {stat: os.path.join(proj_dir, "Fanfic lists/%s_%s_val.txt" % (fandom, stat)) for stat in stat_tup}
        get_anomaly_ids(stat_conds, os.path.join(proj_dir, "CSV/%s_edit.csv" % _fandom), outfiledict)


proj_dir = "/Volumes/2TB/Final_project"
fandoms = ("Doctor Who", "Hamilton", "Les Mis", "Sherlock", "Star Trek", "Tolkien", "Undertale")
categories = ("F/M", "M/M", "F/F", "Gen", "Multi", "Other")
tags = ("Fluff", "Angst", "Humor", "Romance", "Hurt/Comfort", "Established", "Friendship", "Crack")
statuses = ("Completed", "Updated")
years = [str(x) for x in range(2009, 2019)]
range_tuples = [(1, 100), (1, 1000), (1001, 5000), (5001, 10000), (1001, 10000), (10001, 50000), (50001, 100000), (10000, 100000),
                   (100001, 500000), (500001, 1000000), (100001, 1000000)]
ratings = ("General Audiences", "Teen And Up Audiences", "Mature", "Explicit", "Not Rated")

# fix_fand = ("Sherlock", "Star Trek")
# fandom_numpy_stats(proj_dir, fix_fand)
# category_ids(proj_dir, fix_fand, categories)
# au_ids(proj_dir, fix_fand)
# other_tags_ids(proj_dir, fix_fand, tags)
# status_ids(proj_dir, fix_fand, statuses)
# year_ids(proj_dir, fix_fand, years)
# word_ids(proj_dir, fix_fand, range_tuples)
# rating_ids(proj_dir, fix_fand, ratings)
# fandom_id_files(proj_dir)
# csv_id_files(proj_dir, fix_fand)
# fandom_anomaly_ids(proj_dir, fix_fand)


# fanfic_dir = os.path.join(proj_dir, "Fanfic_all")
# idlist_dir = os.path.join(proj_dir, "Fanfic lists")
# for idlist in os.listdir(idlist_dir):
#     print(idlist)
#     filenames = []
#     if idlist.endswith(".txt"):
#         f_in = open(os.path.join(idlist_dir, idlist))
#         for line in f_in:
#             filename = os.path.join(fanfic_dir, line.strip() + ".txt")
#             if filename not in filenames:
#                 filenames.append(filename)
#             else:
#                 print(filename)
#         f_in.close()
# fandom_anomaly_hist(proj_dir)


# new_csv(os.path.join(proj_dir, "CSV/Doctor_Who_works.csv"), os.path.join(proj_dir, "CSV/Doctor_Who_edit.csv"))
# start = time.time()
# stat_dictionary = ao3_count_stats_from_csv(os.path.join(proj_dir, "CSV/Doctor_Who_edit.csv"))
# count_stat_time = time.time() - start
# print("Time to count Doctor Who stats:", count_stat_time)
# start = time.time()
# store_stats(stat_dictionary, os.path.join(proj_dir, "CSV stats/Doctor_Who_edit.xlsx"))
# store_time = time.time() - start
# print("Time to store Doctor Who stats:", store_time)
#
# new_csv(os.path.join(proj_dir, "CSV/Hamilton_works.csv"), os.path.join(proj_dir, "CSV/Hamilton_edit.csv"))
# start = time.time()
# stat_dictionary = ao3_count_stats_from_csv(os.path.join(proj_dir, "CSV/Hamilton_edit.csv"))
# count_stat_time = time.time() - start
# print("Time to count Hamilton stats:", count_stat_time)
# start = time.time()
# store_stats(stat_dictionary, os.path.join(proj_dir, "CSV stats/Hamilton_edit.xlsx"))
# store_time = time.time() - start
# print("Time to store Hamilton stats:", store_time)
#
# # new_csv(os.path.join(proj_dir, "CSV/Les_Mis_works.csv"), os.path.join(proj_dir, "CSV/Les_Mis_edit.csv"))
# start = time.time()
# stat_dictionary = ao3_count_stats_from_csv(os.path.join(proj_dir, "CSV/Les_Mis_edit.csv"))
# count_stat_time = time.time() - start
# print("Time to count Les Mis stats:", count_stat_time)
# start = time.time()
# store_stats(stat_dictionary, os.path.join(proj_dir, "CSV stats/Les_Mis_edit.xlsx"))
# store_time = time.time() - start
# print("Time to store Les Mis stats:", store_time)
#
# new_csv(os.path.join(proj_dir, "CSV/Sherlock_works.csv"), os.path.join(proj_dir, "CSV/Sherlock_edit.csv"))
# start = time.time()
# stat_dictionary = ao3_count_stats_from_csv(os.path.join(proj_dir, "CSV/Sherlock_edit.csv"))
# count_stat_time = time.time() - start
# print("Time to count Sherlock stats:", count_stat_time)
# start = time.time()
# store_stats(stat_dictionary, os.path.join(proj_dir, "CSV stats/Sherlock_edit.xlsx"))
# store_time = time.time() - start
# print("Time to store Sherlock stats:", store_time)
#
# new_csv(os.path.join(proj_dir, "CSV/Star_Trek_works.csv"), os.path.join(proj_dir, "CSV/Star_Trek_edit.csv"))
# start = time.time()
# stat_dictionary = ao3_count_stats_from_csv(os.path.join(proj_dir, "CSV/Star_Trek_edit.csv"))
# count_stat_time = time.time() - start
# print("Time to count Star Trek stats:", count_stat_time)
# start = time.time()
# store_stats(stat_dictionary, os.path.join(proj_dir, "CSV stats/Star_Trek_edit.xlsx"))
# store_time = time.time() - start
# print("Time to store Star Trek stats:", store_time)
# #
# new_csv(os.path.join(proj_dir, "CSV/Tolkien_works.csv"), os.path.join(proj_dir, "CSV/Tolkien_edit.csv"))
# start = time.time()
# stat_dictionary = ao3_count_stats_from_csv(os.path.join(proj_dir, "CSV/Tolkien_edit.csv"))
# count_stat_time = time.time() - start
# print("Time to count Tolkien stats:", count_stat_time)
# start = time.time()
# store_stats(stat_dictionary, os.path.join(proj_dir, "CSV stats/Tolkien_edit.xlsx"))
# store_time = time.time() - start
# print("Time to store Tolkien stats:", store_time)
# #
# new_csv(os.path.join(proj_dir, "CSV/Undertale_works.csv"), os.path.join(proj_dir, "CSV/Undertale_edit.csv"))
# start = time.time()
# stat_dictionary = ao3_count_stats_from_csv(os.path.join(proj_dir, "CSV/Undertale_works.csv"))
# count_stat_time = time.time() - start
# print("Time to count Undertale stats:", count_stat_time)
# start = time.time()
# store_stats(stat_dictionary, os.path.join(proj_dir, "CSV stats/Undertale_stats.xlsx"))
# store_time = time.time() - start
# print("Time to store Undertale stats:", store_time)

# get_drabble_ids(os.path.join(proj_dir, "CSV/Doctor_Who_works.csv"), os.path.join(proj_dir, "Fanfic lists/Doctor Who drabbles.txt"))


# remove_ids(os.path.join(proj_dir, "CSV/Sherlock_edit.csv"), os.path.join(proj_dir, "CSV/Sherlock_edit2.csv"), [5661940, 3536660, 3363959, 2289575, 2284830, 2284857, 620622, 620665, 620635, 620624])
# os.rename(os.path.join(proj_dir, "CSV/Sherlock_edit2.csv"), os.path.join(proj_dir, "CSV/Sherlock_edit.csv"))
# os.rename(os.path.join(proj_dir, "CSV/Star_Trek_edit2.csv"), os.path.join(proj_dir, "CSV/Star_Trek_edit.csv"))
# category_ids(proj_dir)
# other_tags_ids(proj_dir)
# status_ids(proj_dir)
# year_ids(proj_dir)
# word_ids(proj_dir)
# rating_ids(proj_dir)
# get_fandom_group_id_files(proj_dir)

"""
# Sherlock all.txt /Volumes/2TB/Final_project/Fanfic_all/work_id.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/12284460.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/11080263.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/11037063.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/11036334.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/10766178.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/6758869.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/5509559.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/5348297.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/4483961.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1861815.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1553114.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1465528.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1399027.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1399003.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1398964.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1118402.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/998174.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/988000.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/983084.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/977536.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/975245.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/973889.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/962764.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/805993.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/9578879.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/641265.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/556449.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/526555.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/523800.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/522433.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/521122.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/521116.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/518627.txt
! Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/517445.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/12052728.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/9610910.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/9610769.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/9662114.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/9578228.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/9257879.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/12366036.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/9577883.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/1898088.txt
# Doctor Who drabbles.txt /Volumes/2TB/Final_project/Fanfic_all/5098.txt
"""
"""
/Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13289610* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13278003* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13243146* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6610069* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13230948* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13197792* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13148625* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12879648* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13129275* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12879690* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13123575* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13104996* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12879435* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12435993* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13033530* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13026777* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12942441* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12941598* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12926265* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12805116* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12805005* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10596960* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12804858* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12804726* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12840495* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12804687* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13245642* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12452571* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12679935* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12674235* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12645486* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12614528* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12606024* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12571932* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12544380* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12544340* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12544308* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12544284* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12544272* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12543504* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12511296* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12493880* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11498667* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12471784* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12470116* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 884719* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12405948* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12395280* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12388956* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12344973* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12318093* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12221472* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12152970* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12116946* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 12032574* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11988822* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11980866* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11980833* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 13245342* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11920302* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11920251* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11920092* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11668233* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11907453* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11658927* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11805495* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11737848* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11735223* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11727516* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7982869* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11685066* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11550009* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11658549* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11638779* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11469051* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11469525* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11623413* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11597511, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11585604* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11468739* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11454126* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11551530! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11449101* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11526003* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11674542* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11456253, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11196546* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11378106* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11274936* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11234931* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11223300* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11089659* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11201325* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11080008* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11096607* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11093532* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11081970* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10684650* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 11011005* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10973382* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10928925* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10914372, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10894818* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1125241* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10858374* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10858230* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10857432* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10850253* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10827966* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10803849* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9632186* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6967069* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10737327* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10603455* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10700802* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10603182* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10675593* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10666479* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10603056* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10640190* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10622352* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10593786* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10565856* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10555150* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10518234* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10494243* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10435524* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10410147* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10398882* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10398819* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10398543* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10372014* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10370064* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10368342* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10368171* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10367667* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10282535* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10282163* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10181504* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10105988, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10087871* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10051703* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10076405* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10066232* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10061447* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 10053188* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9991997* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9927548* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9922349* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9468068* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9908516* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9896039* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9842945* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9841733* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9841721* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9841688* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9819569* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9816584* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9743420* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9646244* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9622256* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9557684* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9545372, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9532940* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9491330* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9470360* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9460901* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9438992* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9428093* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9389663* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9118744* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9372347* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9322739* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9321074* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9320960* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9296354, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9118711* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9236465* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9118801* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9171799* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9163747* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9147202* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9122314* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9110644* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9131071* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9094576* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 9062902* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8703607* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8965204* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8684842* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8819317* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8804422* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8783701* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8775793* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8648887* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8639893* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8616592* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8616508* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8616439* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8616346* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8615398* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8570596* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8566456* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8540218* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8513437* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8513428* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8508448* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8508121* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6724645* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8477572* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8465659* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8460997* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8424721* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8418748* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8407213* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8397184* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8369725* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8337175* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3205226* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8328724* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7945978* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7878454* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8290762, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3998593, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8257946* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8249590* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8154991* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8132383* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8140693* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8106610* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8074327* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8061160* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8052652* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8044699* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8033536* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8137298* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7934206* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7948078* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7940662* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7916908* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7865023* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7895986* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7856401* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7693156* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7824967* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7794484* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7788799* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7766599* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7754644* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7752076* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7744177* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7722688* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7722628* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7722619* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7722604* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7570834* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7669195* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7655821* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7646287* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7622239* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7561351* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7548307* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7537111* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7536943* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7530409* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7519735* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7514764* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1153843* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7484229* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7483497* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7474674* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7471209* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7467189* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7465299* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7456153* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7448341* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7444195* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7411162* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7417063* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7416931* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7253251* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7388791* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7388458* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7388437* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7391062* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7379392* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7372075* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7372036* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7375594* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7372018* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7345825* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7332508* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7327381* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7327366* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7327357* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7309465* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7266814* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7269115* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7263238* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7237384* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7226530* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7208564* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7199882* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7187057* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7178330* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7162832* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7155215* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6971182* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7136672* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7131131* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7133915, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7072423* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7052836* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7045204* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7022545* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6972142* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6976417* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6797533* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6965686* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6962632* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6953458* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6953413* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6947716* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6929629* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6929614* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6911773* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6902272* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6892912* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6892732* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6883942* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6785086* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6745141* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6745087* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6736099* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6727036* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6695071* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6652069* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6651892* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6680086* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6651817* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6674077* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6673975* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6499024* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6651670* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6663904* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6663886* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6651466* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6649630* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6643669* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6626941* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6626860* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6525733* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6590695* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6571819* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6561532* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6552247* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6552241* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6552232* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6544354* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6544333* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6544306* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6536641* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6535768* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4112260* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6527014* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6527008* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6525466* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6510958* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6497554* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6493825* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6236290, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6486967* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6486955* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6485086* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6476140* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6466234* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6459499* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6459484* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6457576* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6424522* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6422752* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6415399* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6414214* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6393730* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6387022* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6385876* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6385543* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6385531* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6385501* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6365131* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6359380* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6346183* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6346129* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6345721* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6344620* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6341365* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6333604* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6324847* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6324445* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6323302* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6323263* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6323104* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6323101* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6323074* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6314401* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6289564* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6286033* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6282685* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6275767* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6273625* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6273592* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6266056* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6265861* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6256192* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6251068* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6249283* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6249076* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6234379* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6246928* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6224527* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6215911* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6211054* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6176485* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6205522* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6205366* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6203605* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6176443* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6189625* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6173848* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6171130* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6168247* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6163633* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6163241* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6159831* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6159768* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5862562* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6158773* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6153804* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6148725* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6147823* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6147250* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6141636* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6135480* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6134049* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6132858* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6128452* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6128227* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6124834* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6121506* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6121147* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6118525* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6114826* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6112641* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6111952* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6111446* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6111267* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6108163* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6109585* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6105277* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6105096* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6105007* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6097063* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6098293* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6098290* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6077055* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6076971* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6063589* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6055717* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6035800* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6031348* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6019773* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6010708! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6006508* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5990689* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5990653* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5990635* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6035905* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5986432* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5976001* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5972767* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5970064* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5969257* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5969200* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5969254* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5953126* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5905927* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5898337* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5880382* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5881438* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5869150* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5848780* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5846344* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5834353* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5803936* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5809228* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5800948* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5677003, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5783914* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5780377* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5773690* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5743171* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5719390* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5719363* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5712826* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5680648* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5680330* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5680009* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5679901* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5671534, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5669722* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5659957* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5652253* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5626345* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5619070* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5620648* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5620627* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5620606* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5620546* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5620465* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5620387* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5619775* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5615329* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5612029* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5611504* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5611471* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5608546* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5599789* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5599741* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5599603* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5170508* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5560285* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5415725* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5538398* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5497901* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5486699* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5481980* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5481956* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5481932* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5473085* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5470997* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5470805* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5470736* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5470274* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5463335* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5463137* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5462924* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5462636* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5454734* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5449757* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2240751* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5426048* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5414834* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5409719* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5317247* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5312540* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5274215* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5271521* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5232314* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5202212* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5201507* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5188805* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5188943* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5188676* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5187311* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5188856* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5188763* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5173691* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5173784* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5173865* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5171750* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5165126* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5164706* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5167706* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5167640* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5162885* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5154659* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5149940* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5148959* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5148731* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5149019* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5148938* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5139464* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5128670* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5108306* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5072173, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5092397* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5070028* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5057089* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5030737* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5012479* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 5004262* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4980433* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4963144* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4943380* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4902937* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4884406* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4877920* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4870954* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4860176* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4857545* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4847159* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4753205* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4732706* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4732460* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4699355* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4682684* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4642833* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4557663* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4554567* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4551441* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4538964* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4540773* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4531695* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4531890* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4531497* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4508700* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4502469* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4505298* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4484105* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4430552* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4392956* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4392674* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4391534* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4386317* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4334174* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4335776* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4328196* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4286397* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4286283* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4285767* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4282638* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4279266* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4279236* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4279221* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4255065* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4257486* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4252548* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4227924* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4204218* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4193130* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4191402* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4165413* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4147623* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4127667* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4109245* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4090150* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4067578, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3740317, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4003939* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4003909* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3988801* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3986413* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3984784* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4025227* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3920548* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3920500* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3905599* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3873511* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3854299* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3839980* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3833656* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3822091* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3803092* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3803026* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3802978* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3802402* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3761767* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2208000! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3694433* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3689520* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3684360* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3675993* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3673011* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3668853* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3649734* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3644982* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3636123* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3634620* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3628137* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3627015* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3626667* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3626307* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3618159* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3613431* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3613452* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3602400* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3589164* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3605124* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3562991* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3538721* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3538460! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3527822* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3515375* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3515858* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3514649* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3470471* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3433877* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3422396* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3405815* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3349088* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3362147* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3318140* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3313721* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3362105* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3300182* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3289340* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3274877* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 4662267* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3266762* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3254285* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3247031* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3231125* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3221351* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3215987* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3181025* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3178742* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3175330* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3159179* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3158996* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3122501* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3121802* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3116015* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3112694* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3112520* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3100922, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3091499* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3087560* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 3067049* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2843156* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2839055* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2838500* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2791718* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2765096* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2767289* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2766890* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2763617* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2742848* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2739005* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2727452* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2714114* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2702954* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2699204* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2681123* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2669159* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2664902* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2612156* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2582600* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2572673* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2561696* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2546390* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2170536* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2530745* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2521058* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2518922* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2518388* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2510786* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2485586* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2475494! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2449601* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2447021* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2448947* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2445695* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2444324* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 880256, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2437580* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2437217* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2433773, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2433497* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2425706* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2388932, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2388524* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2362796* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2357300* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2354843* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1784626* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2347247* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2335307* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2319881* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2319665* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2319254* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2318585* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2315516* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2315498* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2299838* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2299757* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2299688* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2275356* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2269347* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2258256* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2245872* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2240445* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2237673* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2228727* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2226687* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2223837* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2223801* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2215776* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2215698* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2215659* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2198319* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2190981* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2190936* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2182830* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2182758* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2174979* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2174199* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2171292* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2169009* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2159442* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2153082* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2136675* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2131509* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2124486* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2123466, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2120898* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2119689* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2119557* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2119449, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2116287* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2112792* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2111481* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2102778* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2094336* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2095170, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2063160* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2037672* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2022924* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2003799* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 2002413* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1995918* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1977963* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1964091, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1961058* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1957854* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1957110* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1956825* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1956114* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1942593* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1940913* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1937454* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1926876* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1891953* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1880427* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1877175* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1864848* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1858563* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1852186* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1852147* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1849927* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1846642* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1843780* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1841137* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1830487* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1830358* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1830322* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1830298* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1830124* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1830028* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1829947* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1829914* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1829854* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1825186* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1826617* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1826626* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1810990* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1806985* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1801663* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1799209* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1793959* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1786687* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1777792* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1778284* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1761999* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1761983* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1761961* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1761943* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1748861* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1728737* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1705070* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1694264* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1691870* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1690913* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1688744* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1687982! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1675202* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1669376* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1669361* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1666034* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1662200* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1662104* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1661903* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1657184* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1654058* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1653422* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1620809, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1619402* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1616120* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1614161* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1598432* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1592786* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1590167* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1578920* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1579091* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1578857* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1557698, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1548491* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1524434* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1519043* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1515707* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1515266* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1515188, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1509710* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1510235* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1149979* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1503995* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1503020, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1496383* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1499819* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1499660* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1499062* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1492429* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 582966* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1468450, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1461304* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1456498* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1451707* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1433011* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1415044* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1411420, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1404310* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1399882* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1398253* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1398724* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1394398* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1390924* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1381573* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1374655* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1360897* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1360891* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1356088* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1353388* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1349503* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348966* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348663* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348714* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348648* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348915* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348840* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347979* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348807* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348939* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348681* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348903* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1349011* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348789* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348855* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348165* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348150* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348123* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348108* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348096* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348081* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348066* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348057* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348027* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1348012* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347997* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347964* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347931* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347916* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347877* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347808* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347784* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347775* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347757* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347709* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347673* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347655* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347625* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347598* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347595* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347586* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347535* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347502* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347478* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347460* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347448* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347442* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347421* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347406* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347376* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347307* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347157* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347142* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347109* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347082* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347073* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1347058* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1346263* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1328995* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1328716* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1328509* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1318909* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1318876* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1313410* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1308982* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1308211* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1306603* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1305760* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1302658* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1297516* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1295878* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1293415* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1282051* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1274734* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1269253* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1269184* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1269160* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1266322* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1229491* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1220341* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1212064* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1207618* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1197612* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1197306* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1188510* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1188381* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1186364* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1187781* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1185034* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1182968* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1181955* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1181617* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1181599* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1176983* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1177649* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1176946, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1174563* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1174865* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1174876* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1174136* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1168512* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1166008, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1153297* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1142410* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1137709* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1132121* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1131782* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1130526* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1130345* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1124165* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1123338* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6066324* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1119854* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1119612* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1118757* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1118730* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1117793, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1114758* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1114302* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1113980* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 976995, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1111000* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1109378, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1108887* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1108166* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1106243, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1103183* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1093300* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1090700* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1089399* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1083726* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1077574* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1074105* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1071572* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1071125* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1070758* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1067900, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1065256* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1065024* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1063961* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1063349* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1062787* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1046092* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1040641* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1038793* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1024401* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1017959* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1017159* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1015321* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1013318* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1012684* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 871426* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1009930* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1007510* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1006983* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 996131* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 994740* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 994743* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 994738* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 992158* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 989761* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 989286* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 989281* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 985578* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 985261* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 985247* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 984425* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 981698* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 981359* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 976313* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 974409* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 973440* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 973437* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 970537! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 968989* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 967919* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 967556* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 965946! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 960550* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 956686* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 956653* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 955392* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 955010* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 954886* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 954111* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 953192* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 953186* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 953184* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 953181* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 953173* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 953176* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 953073* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 960020* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 951602* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 950344* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 950336* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 949004* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 947645* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 944254* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 944431* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 942810* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 940046* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 940337* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 938145* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 937023* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 935121* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 934662* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 934446* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 934379* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 932822* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 931779* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 931119* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 930865* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 930227* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 927544* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 916664* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 914639* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 914031* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 912012* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 912007* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 911990* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 910877* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 910869* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 910853* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 910848* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 910839* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 910836* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 910833* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 899271* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 900277* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 898571* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 897523* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 896561* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 892866* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 903206* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 889668* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 885792, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 883620* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 882091* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 826969* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 875963* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873837* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873831* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873830* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873826* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873822* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873819* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873817* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873812* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873809* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873805* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873801* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873797* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873795* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 873036* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 870104* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 865317* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 863436* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 857276* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 853407* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 853081* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7213126* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 844384* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 844382* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 844378* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 844375* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 844371* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 843790* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 841156* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 840843* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 840625* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 839555* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 836062* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 837654* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834165* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 833110* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 832777* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 832638* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 832003* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 832434* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 826775* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 826315* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 825131* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 643227, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816486* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816483* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816481* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816474* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816473* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816470* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816467* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 816459* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 807567* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 800066* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 790249* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 783782* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834184* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834182* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 777534! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 779549* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 779049* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834187* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 779094* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 778487* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834176* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 774805, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 772460* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 772066* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 771836* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 771841* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 769168* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 768531* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 767482* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 764363* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 540684* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 760902* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 759769* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 759583* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834148* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 757638* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834131* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 752693* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 751025* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 749829* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 747111* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 747058* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 744364* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 741718* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 739429* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 737565* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 737296* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 737290* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 737285* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 737283* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 735326* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834145* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834141* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 730088* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 727675* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 727668* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 727575* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 727161* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834138* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 708226* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 708216* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 707177* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 706485* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 705363* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 703217* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 701576* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 701576* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699689* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699687* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699683* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699681* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699676* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699672* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699667* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699653* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699645* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699640* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699635* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699634* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699632* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699629* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699623* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699616* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699611* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699606* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699602* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699599* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699593* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699589* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699582* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699570* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699574* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 699567* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 698956* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 698311* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 698211* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 694623* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 692449* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 692270* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 686476* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 679889* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 330436* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 673924* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 672554* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 666826* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 665549* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 665526* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663924* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663351* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663167* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663161* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663154* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663109* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663104* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663096* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663089* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 663085* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 662779* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 662755* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 660190* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 659072* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 645914* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 644432* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 641488* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 834119* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 635264* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 634060* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 630962* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 628324* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 627102* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 626734* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 626781* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 625790, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6049165* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 618113* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 617716* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 617706* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 617699* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 616172* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 616164* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 613473* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 612748* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 611590* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 611587* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 611584* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 610441* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 609273* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 607130* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 604255* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 604260* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 603004* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 603033* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 597273* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 595379* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 594685* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 594488! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 593475* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 593258* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 593022* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 592389* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 590167* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 589971* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 589061* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 589201* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 589208* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 585595* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 586838* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 586837* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 584116* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583198* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583195* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583182* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583168* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583163* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583162* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583161* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583158* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 165133* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 581222* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 574686* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 574820* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 574824* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 573612* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 570527* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6049216* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 560024* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 558543* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 556736* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 556304* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 554345* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 553333* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 552952* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 551882* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 551016* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 550579* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 550086* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 549083* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 549081* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 548460* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 548448* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 548444* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 544173* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 544452* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 544453* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 544028! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 543449* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583142* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 541656* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 540876* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 538249* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 536265* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 531806* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 531174* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 531168* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 527941* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 527535* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583134* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 526555, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 524792* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 523137! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 522132* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 519130* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583118* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583126* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583112* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 515988* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 512149* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 512481* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 509644* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 509642* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 509441* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 508555* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 508482* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 507904* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 507163* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 507171* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 503549* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 502999* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 501357* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 500833* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 500823* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 500453* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 500270* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 500026* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 499179* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 407796* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 495926* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 491299* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 490472* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 488911* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 479298* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 476446* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 465641* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 465638* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 464429* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 463878* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 463624* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 463233* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 460264* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 460032* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 455171* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 453522* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 452834* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583103* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 479399* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 479385* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 479397* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 479383* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 479391* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 479404* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 445905* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 445324* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 443611* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 443263* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 440644* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 439915* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 440188* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 439008* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 438462* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 434492* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 429127* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 531750* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 421534* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 412310* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 407676* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 407480* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 398297* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 396871* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 396986* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 392860* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 390677* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 390385* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 390797* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 389909* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 389347* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 384872* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 384946* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 384930* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 384950* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 384912* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 375967* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 375924* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583096* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 374114* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 372587* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 369644* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 366516* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 365929* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 360874* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 359611* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 606127* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 352158* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 348508* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 345822* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 345625* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 344352* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 343267* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 343252* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 342487* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 284108* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 337139* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 335800* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 332339* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 331811* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 331498* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 332041* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 328833* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 327477* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 327475* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 327474* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 273512* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 324237* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 323246* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 321944* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 321575* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 369433* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 321276* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 319631* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 319610* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 264886* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 319278* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 318703* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583085* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 312902* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583099* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 290502* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583089* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 284119* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 285907* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583071* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583065* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 275562* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583062* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 270818* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 269271* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 269228! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583037* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583016* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583060* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 256355* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 249875* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 247742* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 247658* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 243199, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 583000* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 237486* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 235426* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 234941* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 233895* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 233714* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 226339* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 225457* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 220314* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 212986* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 212977* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 212971* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 212678* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 211688* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 230969* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 322771, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 195503, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 195074* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 582988* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 582986* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 190728* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 184100* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 179664! /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 178610* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6319810, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1058362, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6319828, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1058360, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 6319978, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 1058355, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 582888* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 149549* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 151302* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 146908* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 142450* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 141386* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 138593* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 137565* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 137053* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 136857* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 136367* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 136267* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 134972* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 134373* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 131003* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 130809, /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 130531* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 100101* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 263715* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 7153814* /Volumes/2TB/Final_project/CSV/Sherlock_works.csv 8397355*
/Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 13340475* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 13278189* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 13325424* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 13222062! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 13221975! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 13213452* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 13172514* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12918969* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12903456* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12724581* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7759687* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12353994, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1228105* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12257427* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12215016* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12144471* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12032574* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11965590* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11963226* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11963133* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11851005* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11703957* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11597337* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11594424* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8722708* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11352573* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 11006187* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10994832* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10694073* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10861974* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10837317* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10808076* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10801716* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10701651* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10701294* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 819776, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10675533* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10572321* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10540755* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10495179* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10355619* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9649487* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10342764* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10262447* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10225031* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10165913* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10141892* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9984788* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9953198* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9949661* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9949355* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9949250* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9925046* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9857927* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9697016* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9696665* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9529388* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9498848* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9295424* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9293888* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9219842* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8939704* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8843515* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8748226* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7142849, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8696662* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8599879* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8569939* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8498938* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8483692* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8441497* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8412091* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8396629* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8419117* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8339359* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8338432* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8337628* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8332564* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8156506* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8153468* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8039770* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8037436* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8017099* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7996621* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7987651, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7892617* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8172460* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7759042* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7757248* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7744999* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7614352* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7614286* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7599382* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7534021* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7524934* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7480428* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7347916* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7192613* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7188119* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 7186865* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6822550* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6738346* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6619804* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6517051* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6503914* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6497197* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6495838* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6386458* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6349330* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6349252* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6349213* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6290860* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6254851* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6244393* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6115714* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6063589* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6061195* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6049723* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6034672* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1344013* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 6004888* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5979859* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5976001* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5738446* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5743171* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5717572* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5593621* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5551109* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5496968* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5391995* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5381552* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5329865* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5298962* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5291009* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5235146* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5187311* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5139521* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5051731* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4851407* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4735010* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4668143* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4512213* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4402820* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4327422, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4306224* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4132195* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4021024! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3736285* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3664431* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3645915* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3574277* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3464909, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3350675* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3325001* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3253052* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3156437* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3158225, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 3114542* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2841419* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2812655* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2812634* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2812472* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2812391* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2811881* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2811722* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2791979* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2717381* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2717372* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2655686, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2646077, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2627288* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2317169* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2315024* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2289590* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2268369* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2248785* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2262681* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2248641* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2248626* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2244114* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2223837* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2223801* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2215776* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2215698* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2215659* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2190981* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2190936* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2171292* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2171058* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2169009* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2159442* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2134059* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2123466, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2119449, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2112792* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2102778* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2095170, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2065536* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2017044* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1871247, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1856389* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1807885* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1808044* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1802026* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1764927* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1700891* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1662125* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1662074* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1619549* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1613240* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1579826* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 4241142* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1537205* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1461514! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1417810* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1379323, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1358194* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1333234* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1333153* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1333105* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1333096* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1318876* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1275334* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1293415* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1292407* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1284085, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 2289626* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1235470* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1220599* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1217191, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1148672* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1179432* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1178571* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1175297* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1174344* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1142705* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1137072* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1131073* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1116672* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1104778* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1103103* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1084444* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1081778* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1080831* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1077675* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1075614* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1047568* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1044295* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1024401* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1017768* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 1005767* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 925829, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 955445* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 955380* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 955436* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 950805* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 921266, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 947441* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 942392* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 881543* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 881837* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 860634, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 857738* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 856327* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 856163* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 854766* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 851210* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 850718* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 848335* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 844920* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 842878* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 839158* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 833563* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 825222* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 825174* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 813400* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 811837* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 807713* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 788882* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 739011* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 918203* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 783532* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 834187* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 738947* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 706973* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 917204* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 692270* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 687598* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 680086, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 662048* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 665505* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 611848* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 592289* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 580323, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 580315* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 580312* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 579696, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 565646* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 564373* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 556207* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 556203* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 544173* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 540816* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9421325* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 526872, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 514302* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 514298* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 514294* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 508610* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 499951, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 499361* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 459775* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 416661* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 388598* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 366516* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 357591* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 343257* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 343252* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9421379* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 330008, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12269043! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12268917! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12268875! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360705* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 265047* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 261221* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 261215* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12365814! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9420917* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 227455* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360712* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 12365871! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9420791* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 152017* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 152016* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 152015* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 152013* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 152011* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 152004* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 151992* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 151988* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360716* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360723* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360724* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360734* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 130841, /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 196212* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9421004* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360744* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360747* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360750* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 360758* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 9421256* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 10902519* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5051194* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 263931* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 489240* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 854292* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 8046* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 5738755* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 643511! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 879304* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 495741! /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 879324* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 879360* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 842022* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 839489* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 846732* /Volumes/2TB/Final_project/CSV/Star_Trek_works.csv 839495*
"""
