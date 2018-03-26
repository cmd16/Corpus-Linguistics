from main import *
import os


def category_wordlists(proj_dir):
    categories = ["F/M", "M/M", "F/F", "Gen", "Multi", "Other"]
    # TODO: fix
    print("DW category")
    for category in categories:
        str_cat = category.replace("/", "")
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Doctor Who %s.txt" % str_cat),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % str_cat))
    # print("H category")
    # for category in categories:
    #     str_cat = category.replace("/", "")
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Hamilton %s.txt" % str_cat),
    #                                     os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % str_cat))
    # print("LM category")
    # for category in categories:
    #     str_cat = category.replace("/", "")
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Les Mis %s.txt" % str_cat),
    #                                     os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % str_cat))
    print("SH category")
    for category in categories:
        str_cat = category.replace("/", "")
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Sherlock %s.txt" % str_cat),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % str_cat))
    print("ST category")
    # for category in categories:
    #     str_cat = category.replace("/", "")
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Star Trek %s.txt" % str_cat),
    #                                     os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % str_cat))
    # print("T category")
    # for category in categories:
    #     str_cat = category.replace("/", "")
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Tolkien %s.txt" % str_cat),
    #                                     os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % str_cat))
    # print("U category")
    # for category in categories:
    #     str_cat = category.replace("/", "")
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale %s.txt" % str_cat),
    #                                     os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % str_cat))


def au_wordlists(proj_dir):
    print("DW AU")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Doctor Who AU.txt"),
                                    os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Doctor_Who_AU_python.txt"))
    print("H AU")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Hamilton AU.txt"),
                                    os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Hamilton_AU_python.txt"))
    print("LM AU")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Les Mis AU.txt"),
                                    os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Les_Mis_AU_python.txt"))
    print("SH AU")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Sherlock AU.txt"),
                                    os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Sherlock_AU_python.txt"))
    print("ST AU")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Star Trek AU.txt"),
                                    os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Star_Trek_AU_python.txt"))
    print("T AU")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Tolkien AU.txt"),
                                    os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Tolkien_AU_python.txt"))
    print("U AU")
    freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale AU.txt"),
                                    os.path.join(proj_dir, "Fanfic_all"))
    freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Undertale_AU_python.txt"))


def tags_wordlists(proj_dir):
    tags_to_check = ["Fluff", "Angst", "Humor", "Romance", "Hurt Comfort", "Established", "Friendship", "Crack"]
    for tag in tags_to_check:
        print("DW", tag)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Doctor Who %s.txt" % tag),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % tag))
    for tag in tags_to_check:
        print("H", tag)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Hamilton %s.txt" % tag),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % tag))
    for tag in tags_to_check:
        print("LM", tag)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Les Mis %s.txt" % tag),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % tag))
    for tag in tags_to_check:
        print("SH", tag)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Sherlock %s.txt" % tag),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % tag))
    for tag in tags_to_check:
        print("ST", tag)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Star Trek %s.txt" % tag),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % tag))
    for tag in tags_to_check:
        print("T", tag)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Tolkien %s.txt" % tag),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % tag))
    for tag in tags_to_check:
        if tag in ["Fluff", "Angst", "Humor", "Romance"]:
            continue
        print("U", tag)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale %s.txt" % tag),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % tag))


def status_wordlists(proj_dir):
    # print("DW status")
    # for status in ["Completed", "Updated"]:
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Doctor Who %s.txt" % status),
    #                                 os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % status))
    # print("H status")
    # for status in ["Completed", "Updated"]:
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Hamilton %s.txt" % status),
    #                                     os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % status))
    # print("LM status")
    # for status in ["Completed", "Updated"]:
    #     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Les Mis %s.txt" % status),
    #                                     os.path.join(proj_dir, "Fanfic_all"))
    #     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % status))
    print("SH status")
    for status in ["Completed", "Updated"]:
        if status == "Completed":  # TODO: delete this part
            continue
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Sherlock %s.txt" % status),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % status))
    print("ST status")
    for status in ["Completed", "Updated"]:
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Star Trek %s.txt" % status),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % status))
    print("T status")
    for status in ["Completed", "Updated"]:
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Tolkien %s.txt" % status),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % status))
    print("U status")
    for status in ["Completed", "Updated"]:
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale %s.txt" % status),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % status))


def year_wordlists(proj_dir):
    for year in range(2009, 2019):
        print("DW", year)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Doctor Who %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % year))
    for year in range(2009, 2019):
        print("H", year)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Hamilton %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % year))
    for year in range(2009, 2019):
        print("LM", year)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Les Mis %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % year))
    for year in range(2009, 2019):
        print("SH", year)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Sherlock %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % year))
    for year in range(2009, 2019):
        print("ST", year)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Star Trek %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % year))
    for year in range(2009, 2019):
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Tolkien %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % year))
        print("T", year)
    for year in range(2009, 2019):
        print("U", year)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale %d.txt" % year),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % year))


def wordnum_wordlists(proj_dir):
    range_tuples = [(1, 100), (1001, 5000), (50001, 10000), (1001, 10000), (10001, 50000), (50001, 100000),
                    (10000, 100000), (100001, 500000), (500001, 1000000), (100001, 1000000)]
    # range_tuples = [(1, 1000)]  # to fix previous. TODO: add back later
    range_tuples = [(5001, 10000)]  # TODO: change back later
    for rtuple in range_tuples:
        print("DW", rtuple)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Doctor Who %d-%d.txt" % (rtuple[0], rtuple[1])),
                                        os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Doctor_Who_%d-%d_python.txt" % (rtuple[0], rtuple[1])))
    for rtuple in range_tuples:
        print("H", rtuple)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Hamilton %d-%d.txt" % (rtuple[0], rtuple[1])),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Hamilton_%d-%d_python.txt" % (rtuple[0], rtuple[1])))
    for rtuple in range_tuples:
        print("LM", rtuple)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Les Mis %d-%d.txt" % (rtuple[0], rtuple[1])),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Les_Mis_%d-%d_python.txt" % (rtuple[0], rtuple[1])))
    for rtuple in range_tuples:
        print("SH", rtuple)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Sherlock %d-%d.txt" % (rtuple[0], rtuple[1])),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Sherlock_%d-%d_python.txt" % (rtuple[0], rtuple[1])))
    for rtuple in range_tuples:
        print("ST", rtuple)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Star Trek %d-%d.txt" % (rtuple[0], rtuple[1])),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Star_Trek_%d-%d_python.txt" % (rtuple[0], rtuple[1])))
    for rtuple in range_tuples:
        print("T", rtuple)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Tolkien %d-%d.txt" % (rtuple[0], rtuple[1])),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Tolkien_%d-%d_python.txt" % (rtuple[0], rtuple[1])))
    for rtuple in range_tuples:
        print("U", rtuple)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Undertale %d-%d.txt" % (rtuple[0], rtuple[1])),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Undertale_%d-%d_python.txt" % (rtuple[0], rtuple[1])))


def rating_wordlists(proj_dir):
    ratings = ["General Audiences", "Teen And Up Audiences", "Mature", "Explicit", "Not Rated"]
    for rating in ratings:
        print("DW", rating)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Doctor Who %s.txt" % rating),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % rating))
    for rating in ratings:
        print("H", rating)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Hamilton %s.txt" % rating),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % rating))
    for rating in ratings:
        print("LM", rating)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Les Mis %s.txt" % rating),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % rating))
    for rating in ratings:
        print("SH", rating)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Sherlock %s.txt" % rating),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % rating))
    for rating in ratings:
        print("ST", rating)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Star Trek %s.txt" % rating),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % rating))
    for rating in ratings:
        print("T", rating)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Tolkien %s.txt" % rating),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % rating))
    for rating in ratings:
        print("U", rating)
        freqdist = freqdist_from_idfile(
            os.path.join(proj_dir, "Fanfic lists/Undertale %s.txt" % rating),
            os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % rating))


def fandom_group_wordlists(proj_dir):
    crossovers = ["Wholock", "SuperWhoLock"]
    for cross in crossovers:
        print(cross)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s.txt" % cross), os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_python.txt" % cross))


def category_keywords(proj_dir):
    categories = ["FM", "MM", "FF", "Gen", "Multi", "Other"]
    comparisons = [("MM", "FM"), ("FM", "MM"), ("FF", "FM"), ("FM", "FF"), ("MM", "FF"), ("FF", "MM"), ("FM", "Gen"),
                   ("Gen", "FM"), ("MM", "Gen"), ("Gen", "MM"), ("FF", "Gen"), ("Gen", "FF")]
    for category in categories:
        print("DW", category)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % category),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                           "Doctor Who Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Doctor Who_%s vs fanfic_python.txt") % category)
    for comparison in comparisons:
        print("DW", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Doctor Who_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for category in categories:
        print("H", category)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % category),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                       "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Hamilton_%s vs fanfic_python.txt" % category))
    for comparison in comparisons:
        print("H", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Hamilton_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for category in categories:
        print("LM", category)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % category),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                       "Les Mis Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Les Mis_%s vs fanfic_python.txt" % category))
    for comparison in comparisons:
        print("LM", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Les Mis_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for category in categories:
        print("SH", category)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % category),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                       "Sherlock Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Sherlock_%s vs fanfic_python.txt" % category))
    for comparison in comparisons:
        print("SH", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Sherlock_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for category in categories:
        print("ST", category)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % category),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                       "Star Trek Fanfic wordlist.txt"))
    for comparison in comparisons:
        print("ST", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Star Trek_%s vs %s_python.txt" % (comparison[0], comparison[1])))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Star Trek_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for category in categories:
        print("T", category)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % category),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                       "Tolkien Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Tolkien_%s vs fanfic_python.txt" % category))
    for comparison in comparisons:
        print("T", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Tolkien_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for category in categories:
        print("U", category)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % category),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                       "Undertale Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Undertale_%s vs fanfic_python.txt" % category))
    for comparison in comparisons:
        print("U", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Undertale_%s vs %s_python.txt" % (comparison[0], comparison[1])))


def au_keywords(proj_dir):
    print("DW AU")
    keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Doctor_Who_AU_python.txt"),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Doctor Who Fanfic wordlist.txt"))
    store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Doctor Who_AU vs fanfic_python.txt"))
    print("H AU")
    keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Hamilton_AU_python.txt"),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Hamilton Fanfic wordlist.txt"))
    store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Hamilton_AU vs fanfic_python.txt"))
    print("LM AU")
    keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Les_Mis_AU_python.txt"),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Les Mis Fanfic wordlist.txt"))
    store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Les Mis_AU vs fanfic_python.txt"))
    print("SH AU")
    keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Sherlock_AU_python.txt"),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Sherlock Fanfic wordlist.txt"))
    store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Sherlock_AU vs fanfic_python.txt"))
    print("ST AU")
    keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Star_Trek_AU_python.txt"),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Star Trek Fanfic wordlist.txt"))
    store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Star Trek_AU vs fanfic_python.txt"))
    print("U AU")
    keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Undertale_AU_python.txt"),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Undertale Fanfic wordlist.txt"))
    store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Undertale_AU vs fanfic_python.txt"))


def tags_keywords(proj_dir):
    tags_to_check = ["Fluff", "Angst", "Humor", "Romance", "Hurt Comfort", "Established", "Friendship", "Crack"]
    comparisons = [("Fluff", "Angst"), ("Angst", "Fluff"), ("Fluff", "Humor"), ("Humor", "Fluff"), ("Fluff", "Romance"),
                   ("Romance", "Fluff"), ("Fluff", "Hurt Comfort"), ("Hurt Comfort", "Fluff"), ("Fluff", "Established"),
                   ("Established", "Fluff"), ("Fluff", "Friendship"), ("Friendship", "Fluff"), ("Fluff", "Crack"),
                   ("Crack", "Fluff"), ("Angst", "Humor"), ("Angst", "Hurt Comfort"), ("Hurt Comfort", "Angst"),
                   ("Humor", "Crack"), ("Crack", "Humor"), ("Romance", "Friendship"), ("Friendship", "Romance"),
                   ("Romance", "Established"), ("Established", "Romance")]
    for tag in tags_to_check:
        print("DW", tag)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % tag),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Doctor Who Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Doctor Who_%s vs fanfic_python.txt" %tag))
    for comparison in comparisons:
        print("DW", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Doctor Who_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for tag in tags_to_check:
        print("H", tag)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % tag),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Hamilton_%s vs fanfic_python.txt" %tag))
    for comparison in comparisons:
        print("H", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Hamilton_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for tag in tags_to_check:
        print("LM", tag)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % tag),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Les Mis Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Les Mis_%s vs fanfic_python.txt" %tag))
    for comparison in comparisons:
        print("LM", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Les Mis_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for tag in tags_to_check:
        print("SH", tag)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % tag),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Sherlock Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Sherlock_%s vs fanfic_python.txt" %tag))
    for comparison in comparisons:
        print("SH", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Sherlock_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for tag in tags_to_check:
        print("ST", tag)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % tag),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Star Trek Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Star Trek_%s vs fanfic_python.txt" %tag))
    for comparison in comparisons:
        print("ST", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Star Trek_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for tag in tags_to_check:
        print("T", tag)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % tag),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Tolkien Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Tolkien_%s vs fanfic_python.txt" %tag))
    for comparison in comparisons:
        print("T", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Tolkien_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for tag in tags_to_check:
        print("U", tag)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % tag),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Undertale Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Undertale_%s vs fanfic_python.txt" %tag))
    for comparison in comparisons:
        print("U", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Undertale_%s vs %s_python.txt" % (comparison[0], comparison[1])))


def status_keywords(proj_dir):
    statuses = ["Completed", "Updated"]
    comparisons = [("Completed", "Updated"), ("Updated", "Completed")]
    for status in statuses:
        print("DW", status)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % status),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Doctor Who Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Doctor Who_%s vs fanfic_python.txt" %status))
    for comparison in comparisons:
        print("DW", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Doctor Who_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for status in statuses:
        print("H", status)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % status),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Hamilton_%s vs fanfic_python.txt" %status))
    for comparison in comparisons:
        print("H", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Hamilton_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for status in statuses:
        print("LM", status)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % status),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Les Mis Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Les Mis_%s vs fanfic_python.txt" %status))
    for comparison in comparisons:
        print("LM", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Les Mis_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for status in statuses:
        print("SH", status)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % status),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Sherlock Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Sherlock_%s vs fanfic_python.txt" %status))
    for comparison in comparisons:
        print("SH", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Sherlock_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for status in statuses:
        print("ST", status)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % status),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Star Trek Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Star Trek_%s vs fanfic_python.txt" %status))
    for comparison in comparisons:
        print("ST", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Star Trek_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for status in statuses:
        print("T", status)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % status),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Tolkien Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Tolkien_%s vs fanfic_python.txt" %status))
    for comparison in comparisons:
        print("T", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Tolkien_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for status in statuses:
        print("U", status)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % status),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "Undertale Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Undertale_%s vs fanfic_python.txt" %status))
    for comparison in comparisons:
        print("U", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/Undertale_%s vs %s_python.txt" % (comparison[0], comparison[1])))


def year_keywords(proj_dir):
    years = [str(x) for x in range (2009, 2019)]
    comparisons = []  # TODO: add comparisons later maybe?
    for year in years:
        print("DW", year)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % year),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Doctor Who Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Doctor Who_%s vs fanfic_python.txt" % year))
    for comparison in comparisons:
        print("DW", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Doctor Who_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for year in years:
        print("H", year)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % year),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Hamilton_%s vs fanfic_python.txt" % year))
    for comparison in comparisons:
        print("H", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Hamilton_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for year in years:
        print("LM", year)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % year),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Les Mis Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Les Mis_%s vs fanfic_python.txt" % year))
    for comparison in comparisons:
        print("LM", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Les Mis_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for year in years:
        print("SH", year)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % year),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Sherlock Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Sherlock_%s vs fanfic_python.txt" % year))
    for comparison in comparisons:
        print("SH", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Sherlock_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for year in years:
        print("ST", year)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % year),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Star Trek Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Star Trek_%s vs fanfic_python.txt" % year))
    for comparison in comparisons:
        print("ST", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Star Trek_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for year in years:
        print("T", year)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % year),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Tolkien Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Tolkien_%s vs fanfic_python.txt" % year))
    for comparison in comparisons:
        print("T", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Doctor Who_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for year in years:
        print("U", year)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % year),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Undertale Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Undertale_%s vs fanfic_python.txt" % year))
    for comparison in comparisons:
        print("U", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Undertale_%s vs %s_python.txt" % (comparison[0], comparison[1])))


def wordnum_keywords(proj_dir):
    wordnums = ["%d-%d" % (x, y) for x, y in [(1, 100), (1, 1000), (1001, 5000), (5001, 10000), (1001, 10000), (10001, 50000),
                    (50001, 100000), (10000, 100000), (100001, 500000), (10000, 100000), (500001, 1000000), (100001, 1000000)]]
    comparisons = []  # TODO: add comparisons
    for wordnum in wordnums:
        print("DW", wordnum)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % wordnum),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Doctor Who Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Doctor Who_%s vs fanfic_python.txt" % wordnum))
    for comparison in comparisons:
        print("DW", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Doctor Who_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for wordnum in wordnums:
        print("H", wordnum)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % wordnum),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Hamilton_%s vs fanfic_python.txt" % wordnum))
    for comparison in comparisons:
        print("H", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Hamilton_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for wordnum in wordnums:
        print("LM", wordnum)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % wordnum),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Les Mis Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Les Mis_%s vs fanfic_python.txt" % wordnum))
    for comparison in comparisons:
        print("LM", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Les Mis_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for wordnum in wordnums:
        print("SH", wordnum)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % wordnum),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Sherlock Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Sherlock_%s vs fanfic_python.txt" % wordnum))
    for comparison in comparisons:
        print("SH", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Sherlock_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for wordnum in wordnums:
        print("ST", wordnum)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % wordnum),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Star Trek Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Star_Trek_%s vs fanfic_python.txt" % wordnum))
    for comparison in comparisons:
        print("ST", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Star Trek_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for wordnum in wordnums:
        print("T", wordnum)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % wordnum),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Tolkien Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Tolkien_%s vs fanfic_python.txt" % wordnum))
    for comparison in comparisons:
        print("T", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Tolkien_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for wordnum in wordnums:
        print("U", wordnum)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % wordnum),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Undertale_%s vs fanfic_python.txt" % wordnum))
    for comparison in comparisons:
        print("U", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Undertale_%s vs %s_python.txt" % (comparison[0], comparison[1])))


def rating_keywords(proj_dir):
    ratings = ["General Audiences", "Teen And Up Audiences", "Mature", "Explicit", "Not Rated"]
    comparisons = []  # TODO: make some comparisons
    for rating in ratings:
        print("DW", rating)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % rating),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Doctor Who Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Doctor Who_%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:
        print("DW", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Doctor_Who_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Doctor Who_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for rating in ratings:
        print("H", rating)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % rating),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Hamilton_%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:
        print("H", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Hamilton_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Hamilton_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for rating in ratings:
        print("LM", rating)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % rating),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Les Mis Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Les Mis_%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:
        print("LM", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Les_Mis_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Les Mis_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for rating in ratings:
        print("SH", rating)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % rating),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Sherlock Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Sherlock_%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:
        print("SH", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Sherlock_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Sherlock_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for rating in ratings:
        print("ST", rating)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % rating),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Star Trek Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Star_Trek_%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:
        print("ST", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Star Trek_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for rating in ratings:
        print("T", rating)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % rating),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Tolkien Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Tolkien_%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:
        print("T", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Tolkien_%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for rating in ratings:
        print("U", rating)
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % rating),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "Hamilton Fanfic wordlist.txt"))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/Undertale_%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:
        print("U", comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/Undertale_%s vs %s_python.txt" % (comparison[0], comparison[1])))


def fandom_group_keywords(proj_dir):
    comparisons = [("Wholock", "New Who"), ("New Who", "Wholock"), ("Wholock", "BBC Sherlock"), ("BBC Sherlock", "Wholock"),
                   ("Wholock", "SuperWhoLock"), ("SuperWhoLock", "Wholock"), ("SuperWhoLock", "New Who"),
                   ("New Who", "SuperWhoLock"), ("SuperWhoLock", "BBC Sherlock"), ("BBC Sherlock", "SuperWhoLock")]
    for comparison in comparisons:
        print(comparison)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir, "wordlists/%s_python.txt" % comparison[0]),
            os.path.join(proj_dir, "wordlists/%s_python.txt" % comparison[1]))
        store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/%s vs %s_python.txt" % (comparison[0], comparison[1])))


def csv_keywords(proj_dir):
    fandoms = ("Doctor Who", "Les Mis", "Hamilton", "Sherlock", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    for fandom in fandoms:
        print(fandom)
        keyword_dict = keyword_tuple_from_wordlists(
            os.path.join(proj_dir,
                         "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                         "%s Fanfic wordlist.txt" % fandom),
            os.path.join(proj_dir,
                         "Antconc results/AntConc/Ant Original Canon/Original Canon wordlists/"
                         "%s Original Canon wordlist.txt" % fandom))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_Fanfic vs canon_python.txt" % fandom))


def category_similar_keywords(proj_dir):  # TODO: include other comparisons
    categories = ["FM", "MM", "FF", "Gen", "Multi", "Other"]
    comparisons = {"gay vs fanfic": ("MM vs fanfic", "FF vs fanfic"), "gay vs gen": ("MM vs Gen", "FF vs Gen"), "gay vs straight":
        ("MM vs FM", "FF vs FM"), "straight vs gay": ("FM vs MM", "FM vs MM")}
    fandoms = ("Doctor Who", "Hamilton", "Les Mis", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    for comparison in comparisons:
        print("DW", comparison)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/Doctor Who_%s_python.txt" % x) for x in comparisons[comparison]],
        os.path.join(proj_dir, "Keywords/Doctor Who_%s_python.txt" % comparison))
    for comparison in comparisons:
        print("H", comparison)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/Hamilton_%s_python.txt" % x) for x in comparisons[comparison]],
        os.path.join(proj_dir, "Keywords/Hamilton_%s_python.txt" % comparison))
    for comparison in comparisons:
        print("LM", comparison)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/Les Mis_%s_python.txt" % x) for x in comparisons[comparison]],
        os.path.join(proj_dir, "Keywords/Les Mis_%s_python.txt" % comparison))
    for comparison in comparisons:
        print("SH", comparison)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/Sherlock_%s_python.txt" % x) for x in comparisons[comparison]],
        os.path.join(proj_dir, "Keywords/Sherlock_%s_python.txt" % comparison))
    for comparison in comparisons:
        print("ST", comparison)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/Star Trek_%s_python.txt" % x) for x in comparisons[comparison]],
        os.path.join(proj_dir, "Keywords/Star Trek_%s_python.txt" % comparison))
    for comparison in comparisons:
        print("U", comparison)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/Undertale_%s_python.txt" % x) for x in comparisons[comparison]],
        os.path.join(proj_dir, "Keywords/Undertale_%s_python.txt" % comparison))
    for category in categories:
        print(category)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, category)) for fandom in fandoms],
                              os.path.join(proj_dir, "Keywords/%s_python.txt" % category))
    # for comparison in comparisons:
    #     print(comparison)
    #     find_similar_keywords([os.path.join(proj_dir, "Keywords/%s_%s_python.txt" % (fandom, comparison)) for fandom in fandoms],
    #                           os.path.join(proj_dir, "Keywords/%s_python.txt" % comparison))
    # TODO: change this part


def au_similar_keywords(proj_dir):
    fandoms = ("Doctor Who", "Les Mis", "Hamilton", "Sherlock", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    find_similar_keywords(
        [os.path.join(proj_dir, "Keywords/%s_AU vs fanfic_python.txt" % x) for x in fandoms],
        os.path.join(proj_dir, "Keywords/AU vs fanfic_python.txt"))


def tags_similar_keywords(proj_dir):
    fandoms = ("Doctor Who", "Les Mis", "Hamilton", "Sherlock", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    tags_to_check = ["Fluff", "Angst", "Humor", "Romance", "Hurt Comfort", "Established", "Friendship", "Crack"]
    comparisons = [("Fluff", "Angst"), ("Angst", "Fluff"), ("Fluff", "Humor"), ("Humor", "Fluff"), ("Fluff", "Romance"),
                   ("Romance", "Fluff"), ("Fluff", "Hurt Comfort"), ("Hurt Comfort", "Fluff"), ("Fluff", "Established"),
                   ("Established", "Fluff"), ("Fluff", "Friendship"), ("Friendship", "Fluff"), ("Fluff", "Crack"),
                   ("Crack", "Fluff"), ("Angst", "Humor"), ("Angst", "Hurt Comfort"), ("Hurt Comfort", "Angst"),
                   ("Humor", "Crack"), ("Crack", "Humor"), ("Romance", "Friendship"), ("Friendship", "Romance"),
                   ("Romance", "Established"), ("Established", "Romance")]
    combinations = ("Fluff and Romance", "Friendship and Romance", "Friendship and Fluff", "Humor and Crack", "Romance and Established",
                   "Humor and Crack", "Angst and Hurt Comfort")
    for tag in tags_to_check:
        print(tag)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (x, tag)) for x in fandoms],
            os.path.join(proj_dir, "Keywords/%s vs fanfic_python.txt" % tag))
    for comparison in comparisons:
        print(comparison)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs %s_python.txt" % (x, comparison[0], comparison[1])) for x in fandoms],
            os.path.join(proj_dir, "Keywords/%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for combination in combinations:
        print(combination)
        components = combination.split(" and ")
        for fandom in fandoms:
            print(fandom, combination)
            find_similar_keywords(
                [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, x)) for x in components],
                os.path.join(proj_dir, "Keywords/%s_%s_python.txt" % (fandom, combination)))
        # TODO: implement include combination across fandoms


def status_similar_keywords(proj_dir):
    fandoms = ("Doctor Who", "Hamilton", "Les Mis", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    statuses = ["Completed", "Updated"]
    for status in statuses:
        print(status)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (x, status)) for x in fandoms],
            os.path.join(proj_dir, "Keywords/%s_python.txt" % status))


def year_similar_keywords(proj_dir):
    fandoms = ["Doctor Who", "Hamilton", "Les Mis", "Sherlock", "Star Trek", "Tolkien", "Undertale"]
    years = [str(x) for x in range(2009, 2019)]
    for year in years:
        print(year)
        if int(year) < 2015:
            fandoms.remove("Undertale")  # Undertale was realeased in 2015
        elif "Undertale" not in fandoms:
            fandoms.append("Undertale")
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, year)) for fandom in fandoms],
            os.path.join(proj_dir, "Keywords/%s_python.txt" % year))
    # TODO: pick year ranges to look at?


def word_similar_keywords(proj_dir):
    fandoms = ("Doctor Who", "Hamilton", "Les Mis", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    wordnums = ["%d-%d" % (x, y) for x, y in
                [(1, 100), (1, 1000), (1001, 5000), (5001, 10000), (1001, 10000), (10001, 50000),
                 (50001, 100000), (10000, 100000), (100001, 500000), (10000, 100000), (500001, 1000000),
                 (100001, 1000000)]]
    for wordstr in wordnums:
        print(wordstr)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, wordstr)) for fandom in fandoms],
            os.path.join(proj_dir, "Keywords/%s_python.txt" % wordstr))
    # TODO: grouping


def rating_similar_keywords(proj_dir):
    fandoms = ("Doctor Who", "Hamilton", "Les Mis", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    ratings = ["General Audiences", "Teen And Up Audiences", "Mature", "Explicit", "Not Rated"]
    comparisons = []
    combinations = [("Mature and Explicit"), ("Teen And Up Audiences and Mature and Explicit"),
                   ("General Audiences and Teen And Up Audiences"), ("General Audiences and Not Rated")]
    for rating in ratings:
        print(rating)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (x, rating)) for x in fandoms],
            os.path.join(proj_dir, "Keywords/%s vs fanfic_python.txt" % rating))
    for comparison in comparisons:  # TODO: add some comparisons
        print(comparison)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs %s_python.txt" % (x, comparison[0], comparison[1])) for x in fandoms],
            os.path.join(proj_dir, "Keywords/%s vs %s_python.txt" % (comparison[0], comparison[1])))
    for combination in combinations:
        print(combination)
        components = combination.split(" and ")
        for fandom in fandoms:
            print(fandom, combination)
            find_similar_keywords(
                [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, x)) for x in components],
                os.path.join(proj_dir, "Keywords/%s_%s_python.txt" % (fandom, combination)))
        # TODO: implement include combination across fandoms
    # TODO: complete


def fandom_similar_keywords(proj_dir):
    fandoms = ("Doctor Who", "Les Mis", "Hamilton", "Sherlock", "Sherlock", "Star Trek", "Tolkien", "Undertale")
    find_similar_keywords(
        [os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                           "%s Fanfic wordlist.txt" % x) for x in fandoms],
        os.path.join(proj_dir, "Keywords/Fanfic vs canon_python.txt"))


proj_dir = "/Volumes/2TB/Final_Project"

# category_keywords(proj_dir)
# au_keywords(proj_dir)
# tags_keywords(proj_dir)
# status_keywords(proj_dir)
# year_keywords(proj_dir)  #TODO: redo
# for year in range(2009, 2019):
#     print("ST", year)
#     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Star Trek %d.txt" % year),
#                                     os.path.join(proj_dir, "Fanfic_all"))
#     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Star_Trek_%s_python.txt" % year))
# for year in range(2009, 2019):
#     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Tolkien %d.txt" % year),
#                                     os.path.join(proj_dir, "Fanfic_all"))
#     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Tolkien_%s_python.txt" % year))
#     print("T", year)
# for year in range(2009, 2019):
#     print("U", year)
#     freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/Undertale %d.txt" % year),
#                                     os.path.join(proj_dir, "Fanfic_all"))
#     freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/Undertale_%s_python.txt" % year))

#  fandom_group_keywords(proj_dir)

# category_keywords(proj_dir)
# au_keywords(proj_dir)
# tags_keywords(proj_dir)
# status_keywords(proj_dir)

category_similar_keywords(proj_dir)
au_similar_keywords(proj_dir)
tags_similar_keywords(proj_dir)
status_similar_keywords(proj_dir)
year_similar_keywords(proj_dir)
word_similar_keywords(proj_dir)
rating_similar_keywords(proj_dir)
fandom_similar_keywords(proj_dir)
