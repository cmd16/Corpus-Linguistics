from main import *
import os


def category_wordlists(proj_dir, fandoms, categories):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for category in categories:
            print(fandom, category)
            str_cat = category.replace("/", "")
            freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s %s.txt" % (fandom, str_cat)),
                                            os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, str_cat)))


def au_wordlists(proj_dir, fandoms):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        print(fandom, "AU")
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s AU.txt" % fandom),
                                    os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_AU_python.txt" % _fandom))


def tags_wordlists(proj_dir, fandoms, tags):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for tag in tags:
            print(fandom, tag)
            freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s %s.txt" % (fandom, tag)),
                                        os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, tag)))


def status_wordlists(proj_dir, fandoms, statuses):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for status in statuses:
            print(fandom, status)
            freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s %s.txt" % (fandom, status)),
                                    os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, status)))


def year_wordlists(proj_dir, fandoms, years):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for year in years:
            print(fandom, year)
            freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s %d.txt" % (fandom, year)),
                                        os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, year)))


def wordnum_wordlists(proj_dir, fandoms, range_tuples):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for rtuple in range_tuples:
            print(fandom, rtuple)
            freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s %d-%d.txt" % (fandom, rtuple[0], rtuple[1])),
                                        os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_%d-%d_python.txt" % (_fandom, rtuple[0], rtuple[1])))


def rating_wordlists(proj_dir, fandoms, ratings):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for rating in ratings:
            print(fandom, rating)
            freqdist = freqdist_from_idfile(
                os.path.join(proj_dir, "Fanfic lists/%s %s.txt" % (fandom, rating)),
                os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, rating)))


def fandom_group_wordlists(proj_dir):
    crossovers = ("Wholock", "SuperWhoLock")
    for cross in crossovers:
        print(cross)
        freqdist = freqdist_from_idfile(os.path.join(proj_dir, "Fanfic lists/%s.txt" % cross), os.path.join(proj_dir, "Fanfic_all"))
        freqdist_to_wordlistfile(freqdist, os.path.join(proj_dir, "wordlists/%s_python.txt" % cross))


def anomaly_wordlists(proj_dir, fandoms, stat_tup):
    for fandom in fandoms:
        for stat in stat_tup:
            print(fandom, stat)
            fandom_replaced = fandom.replace(" ", "_")
            freqdist = freqdist_from_idfile(
                os.path.join(proj_dir, "Fanfic lists/%s_%s_lo.txt" % (fandom, stat)),
                os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist,
                                 os.path.join(proj_dir, "wordlists/%s_%s_lo_python.txt" % (fandom_replaced, stat)))
            freqdist = freqdist_from_idfile(
                os.path.join(proj_dir, "Fanfic lists/%s_%s_hi.txt" % (fandom, stat)),
                os.path.join(proj_dir, "Fanfic_all"))
            freqdist_to_wordlistfile(freqdist,
                                     os.path.join(proj_dir, "wordlists/%s_%s_hi_python.txt" % (fandom_replaced, stat)))


def category_keywords(proj_dir, fandoms, categories, comparisons):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for category in categories:
            print(fandom, category)
            keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, category)),
                                                    os.path.join(proj_dir, "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                           "%s Fanfic wordlist.txt" % fandom))
            store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt") % (fandom, category))
        for comparison in comparisons:
            print(fandom, comparison)
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[0])),
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[1])))
            store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/%s_%s vs %s_python.txt" % (fandom, comparison[0], comparison[1])))


def au_keywords(proj_dir, fandoms):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        print(fandom, "AU")
        keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/%s_AU_python.txt" % _fandom),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "%s Fanfic wordlist.txt" % fandom))
        store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_AU vs fanfic_python.txt" % fandom))


def tags_keywords(proj_dir, fandoms, tags, comparisons):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for tag in tags:
            print(fandom, tag)
            keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, tag)),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "%s Fanfic wordlist.txt" % fandom))
            store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" %(fandom, tag)))
        for comparison in comparisons:
            print(fandom, comparison)
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[0])),
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[1])))
            store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/%s_%s vs %s_python.txt" % (fandom, comparison[0], comparison[1])))


def status_keywords(proj_dir, fandoms, statuses, comparisons):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for status in statuses:
            print(fandom, status)
            keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, status)),
                                                os.path.join(proj_dir,
                                                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                             "%s Fanfic wordlist.txt" % fandom))
            store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, status)))
        for comparison in comparisons:
            print(fandom, comparison)
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[0])),
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[1])))
            store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir, "Keywords/%s_%s vs %s_python.txt" % (fandom, comparison[0], comparison[1])))


def year_keywords(proj_dir, fandoms, years, comparisons):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for year in years:
            print(fandom, year)
            keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, year)),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "%s Fanfic wordlist.txt" % fandom))
            store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, year)))
        for comparison in comparisons:
            print(fandom, comparison)
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[0])),
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[1])))
            store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/%s_%s vs %s_python.txt" % (fandom, comparison[0], comparison[1])))


def wordnum_keywords(proj_dir, fandoms, range_tuples):
    comparisons = []  # TODO: add comparisons
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for wordnum in range_tuples:
            print(fandom, wordnum)
            keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, wordnum)),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "%s Fanfic wordlist.txt" % fandom))
            store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, wordnum)))
        for comparison in comparisons:
            print(fandom, comparison)
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[0])),
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[1])))
            store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/%s_%s vs %s_python.txt" % (fandom, comparison[0], comparison[1])))


def rating_keywords(proj_dir, fandoms, ratings, comparisons):
    for fandom in fandoms:
        _fandom = fandom.replace(" ", "_")
        for rating in ratings:
            print(fandom, rating)
            keyword_dict = keyword_tuple_from_wordlists(os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, rating)),
                                                    os.path.join(proj_dir,
                                                                 "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                                                                 "%s Fanfic wordlist.txt" % fandom))
            store_keyword_txt(keyword_dict, os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, rating)))
        for comparison in comparisons:
            print(fandom, comparison)
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[0])),
                os.path.join(proj_dir, "wordlists/%s_%s_python.txt" % (_fandom, comparison[1])))
            store_keyword_txt(keyword_dict,
                          os.path.join(proj_dir,
                                       "Keywords/%s_%s vs %s_python.txt" % (fandom, comparison[0], comparison[1])))


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


def anomaly_keywords(proj_dir, fandoms, stat_tup):  # TODO: hits hi vs comments hi vs bookmarks hi
    for fandom in fandoms:
        for stat in stat_tup:
            print(fandom, stat)
            fandom_replaced = fandom.replace(" ", "_")
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_lo_python.txt" % (fandom_replaced, stat)),
                os.path.join(proj_dir,
                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                             "%s Fanfic wordlist.txt" % fandom))
            if keyword_dict:
                store_keyword_txt(keyword_dict,
                              os.path.join(proj_dir, "Keywords/%s_%s lo vs fanfic_python.txt" % (fandom, stat)))
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_hi_python.txt" % (fandom_replaced, stat)),
                os.path.join(proj_dir,
                             "Antconc results/AntConc/Ant Fanfic/Fanfic wordlists/"
                             "%s Fanfic wordlist.txt" % fandom))
            if keyword_dict:
                store_keyword_txt(keyword_dict,
                              os.path.join(proj_dir, "Keywords/%s_%s hi vs fanfic_python.txt" % (fandom, stat)))
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_lo_python.txt" % (fandom_replaced, stat)),
                os.path.join(proj_dir, "wordlists/%s_%s_hi_python.txt" % (fandom_replaced, stat)))
            if keyword_dict:
                store_keyword_txt(keyword_dict,
                              os.path.join(proj_dir, "Keywords/%s_%s lo vs hi_python.txt" % (fandom, stat)))
            keyword_dict = keyword_tuple_from_wordlists(
                os.path.join(proj_dir, "wordlists/%s_%s_hi_python.txt" % (fandom_replaced, stat)),
                os.path.join(proj_dir, "wordlists/%s_%s_lo_python.txt" % (fandom_replaced, stat)))
            if keyword_dict:
                store_keyword_txt(keyword_dict,
                              os.path.join(proj_dir, "Keywords/%s_%s hi vs lo_python.txt" % (fandom, stat)))


def csv_keywords(proj_dir, fandoms):
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


def category_similar_keywords(proj_dir, fandoms, categories, comb_comparisons, other_comparisons):  # TODO: include other comparisons
    for fandom in fandoms:
        for comparison in comb_comparisons:
            print(fandom, comparison)
            find_similar_keywords([os.path.join(proj_dir, "Keywords/%s_%s_python.txt" % (fandom, x)) for x in comb_comparisons[comparison]],
            os.path.join(proj_dir, "Similar Keywords/%s_%s_python.csv" % (fandom, comparison)))
    for category in categories:
        print(category)
        find_similar_keywords([os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, category)) for fandom in fandoms],
                              os.path.join(proj_dir, "Similar Keywords/%s_python.csv" % category))
    for comparison in comb_comparisons:
        print(comparison)
        filenames = []
        for fandom in fandoms:
            for cmp_str in comb_comparisons[comparison]:
                filenames.append(os.path.join(proj_dir, "Keywords/%s_%s_python.txt" % (fandom, cmp_str)))
        find_similar_keywords(filenames, os.path.join(proj_dir, "Similar Keywords/%s_python.csv" % comparison))
    for comparison in other_comparisons:
        print(comparison)
        comparison_name = comparison[0] + " vs " + comparison[1]
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s_python.txt" % (fandom, comparison_name)) for fandom in fandoms],
            os.path.join(proj_dir, "Similar Keywords/%s_python.csv" % comparison_name))


def au_similar_keywords(proj_dir, fandoms):
    find_similar_keywords(
        [os.path.join(proj_dir, "Keywords/%s_AU vs fanfic_python.txt" % x) for x in fandoms],
        os.path.join(proj_dir, "Similar Keywords/AU vs fanfic_python.csv"))


def tags_similar_keywords(proj_dir, fandoms, tags, comparisons, combinations):
    for tag in tags:
        print(tag)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (x, tag)) for x in fandoms],
            os.path.join(proj_dir, "Similar Keywords/%s vs fanfic_python.csv" % tag))
    for comparison in comparisons:
        print(comparison)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs %s_python.txt" % (x, comparison[0], comparison[1])) for x in fandoms],
            os.path.join(proj_dir, "Similar Keywords/%s vs %s_python.csv" % (comparison[0], comparison[1])))
    for combination in combinations:
        print(combination)
        components = combination.split(" and ")
        for fandom in fandoms:
            print(fandom, combination)
            find_similar_keywords(
                [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, x)) for x in components],
                os.path.join(proj_dir, "Similar Keywords/%s_%s_python.csv" % (fandom, combination)))
        # TODO: implement include combination across fandoms


def status_similar_keywords(proj_dir, fandoms, statuses):
    for status in statuses:
        print(status)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (x, status)) for x in fandoms],
            os.path.join(proj_dir, "Similar Keywords/%s_python.csv" % status))


def year_similar_keywords(proj_dir, year_fandoms):
    # year_fandoms = {year: fandoms}
    for year in year_fandoms:
        print(year)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, year)) for fandom in year_fandoms[year]],
            os.path.join(proj_dir, "Similar Keywords/%s_python.csv" % year))
    # TODO: pick year ranges to look at?


def word_similar_keywords(proj_dir, fandoms, range_tuples):
    for wordstr in range_tuples:
        print(wordstr)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, wordstr)) for fandom in fandoms],
            os.path.join(proj_dir, "Similar Keywords/%s_python.csv" % wordstr))
    # TODO: grouping


def rating_similar_keywords(proj_dir, fandoms, ratings, comparisons, combinations):
    for rating in ratings:
        print(rating)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (x, rating)) for x in fandoms],
            os.path.join(proj_dir, "Similar Keywords/%s vs fanfic_python.csv" % rating))
    for comparison in comparisons:  # TODO: add some comparisons
        print(comparison)
        find_similar_keywords(
            [os.path.join(proj_dir, "Keywords/%s_%s vs %s_python.txt" % (x, comparison[0], comparison[1])) for x in fandoms],
            os.path.join(proj_dir, "Similar Keywords/%s vs %s_python.csv" % (comparison[0], comparison[1])))
    for combination in combinations:
        print(combination)
        components = combination.split(" and ")
        for fandom in fandoms:
            print(fandom, combination)
            find_similar_keywords(
                [os.path.join(proj_dir, "Keywords/%s_%s vs fanfic_python.txt" % (fandom, x)) for x in components],
                os.path.join(proj_dir, "Similar Keywords/%s_%s_python.csv" % (fandom, combination)))
        # TODO: implement include combination across fandoms
    # TODO: complete


def fandom_similar_keywords(proj_dir, fandoms):
    find_similar_keywords(
        [os.path.join(proj_dir, "Keywords/%s_Fanfic vs canon_python.txt" % x) for x in fandoms],
        os.path.join(proj_dir, "Similar Keywords/Fanfic vs canon_python.csv"))


def anomaly_similar_keywords(proj_dir, fandoms):
    stat_tup = ("comments", "kudos", "hits", "bookmarks")
    # TODO: finish


proj_dir = "/Volumes/2TB/Final_Project"
fandoms = ("Doctor Who", "Hamilton", "Les Mis", "Sherlock", "Star Trek", "Tolkien", "Undertale")
categories = ("F/M", "M/M", "F/F", "Gen", "Multi", "Other")
category_comparisons = [("MM", "FM"), ("FM", "MM"), ("FF", "FM"), ("FM", "FF"), ("MM", "FF"), ("FF", "MM"), ("FM", "Gen"),
               ("Gen", "FM"), ("MM", "Gen"), ("Gen", "MM"), ("FF", "Gen"), ("Gen", "FF")]
category_comb_comparisons = {"gay vs fanfic": ("MM vs fanfic", "FF vs fanfic"), "gay vs gen": ("MM vs Gen", "FF vs Gen"), "gay vs straight":
        ("MM vs FM", "FF vs FM"), "straight vs gay": ("FM vs MM", "FM vs FF")}
tags = ("Fluff", "Angst", "Humor", "Romance", "Hurt Comfort", "Established", "Friendship", "Crack")
tag_comparisons = [("Fluff", "Angst"), ("Angst", "Fluff"), ("Fluff", "Humor"), ("Humor", "Fluff"), ("Fluff", "Romance"),
                   ("Romance", "Fluff"), ("Fluff", "Hurt Comfort"), ("Hurt Comfort", "Fluff"), ("Fluff", "Established"),
                   ("Established", "Fluff"), ("Fluff", "Friendship"), ("Friendship", "Fluff"), ("Fluff", "Crack"),
                   ("Crack", "Fluff"), ("Angst", "Humor"), ("Angst", "Hurt Comfort"), ("Hurt Comfort", "Angst"),
                   ("Humor", "Crack"), ("Crack", "Humor"), ("Romance", "Friendship"), ("Friendship", "Romance"),
                   ("Romance", "Established"), ("Established", "Romance")]
tag_combinations = ("Fluff and Romance", "Friendship and Romance", "Friendship and Fluff", "Humor and Crack", "Romance and Established",
                   "Humor and Crack", "Angst and Hurt Comfort")
statuses = ("Completed", "Updated")
status_comparisons = [("Completed", "Updated"), ("Updated", "Completed")]
years = [str(x) for x in range(2009, 2019)]
year_fandoms = {year: fandoms for year in years}
print(year_fandoms)
for year in range(2009, 2015):
    year_fandoms[str(year)] = ("Doctor Who", "Les Mis", "Sherlock", "Star Trek", "Tolkien")
    year_fandoms[str(year)] = ("Doctor Who", "Les Mis", "Sherlock", "Star Trek", "Tolkien")
range_tuples = [(1, 100), (1, 1000), (1001, 5000), (5001, 10000), (1001, 10000), (10001, 50000), (50001, 100000),
                    (10000, 100000), (100001, 500000), (500001, 1000000), (100001, 1000000)]
ratings = ("General Audiences", "Teen And Up Audiences", "Mature", "Explicit", "Not Rated")
rating_combinations = [("Mature and Explicit"), ("Teen And Up Audiences and Mature and Explicit"),
                   ("General Audiences and Teen And Up Audiences"), ("General Audiences and Not Rated")]
stat_tup = ("comments", "kudos", "hits", "bookmarks")  # TODO: words later?

fix_fands = ("Sherlock", "Star Trek")

category_wordlists(proj_dir, fix_fands, categories)
au_wordlists(proj_dir, fix_fands)
tags_wordlists(proj_dir, fix_fands, tags)
status_wordlists(proj_dir, fix_fands, statuses)
year_wordlists(proj_dir, fix_fands, years)
wordnum_wordlists(proj_dir, fix_fands, range_tuples)
rating_wordlists(proj_dir, fix_fands, ratings)
anomaly_wordlists(proj_dir, fix_fands, stat_tup)

category_keywords(proj_dir, fandoms, categories, category_comparisons)
au_keywords(proj_dir, fandoms)
tags_keywords(proj_dir, fandoms, tags, tag_comparisons)
status_keywords(proj_dir, fandoms, statuses, status_comparisons)
year_keywords(proj_dir, fandoms, years, [])  # TODO: add comparisons?
wordnum_keywords(proj_dir, fandoms, range_tuples)
rating_keywords(proj_dir, fandoms, ratings, [])
csv_keywords(proj_dir, fandoms)
anomaly_keywords(proj_dir, fandoms, stat_tup)

category_similar_keywords(proj_dir, fandoms, category_comb_comparisons, category_comparisons, category_comb_comparisons)
au_similar_keywords(proj_dir, fandoms)
tags_similar_keywords(proj_dir, fandoms, tags, tag_comparisons, tag_combinations)
status_similar_keywords(proj_dir, fandoms, statuses)
year_similar_keywords(proj_dir, year_fandoms)
word_similar_keywords(proj_dir, fandoms, range_tuples)
rating_similar_keywords(proj_dir, fandoms, ratings, [], rating_combinations)
fandom_similar_keywords(proj_dir, fandoms)
