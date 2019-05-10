# Adopted from https://medium.com/@davidmasse8/predicting-the-next-word-back-off-language-modeling-8db607444ba9

import re
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk import FreqDist
from nltk.tokenize import word_tokenize
np.random.seed(seed=234)

def iterator_from_idfile(idfile, path, end=".txt"):
    """
    Get a file iterator for the files specified in idfile

    :param idfile: open file object containing relative filenames
    :return:
    """
    names = [os.path.join(path, line.strip() + end) for line in idfile]
    return iter(names)
    # for line in idfile:
    #     name = os.path.join(path, line.strip() + end)
    #     yield name

def ngram_df(file_iterator):
    """
    The below breaks up the words into n-grams of length 1 to 5 and puts their counts into a Pandas dataframe with the n-grams as column names.
    The maximum number of n-grams can be specified if a large corpus is being used.

    :param file_iterator: An iterable which yields either str, unicode or file objects
    """
    ngram_bow = CountVectorizer(tokenizer=word_tokenize, preprocessor=lambda s: s.lower(), ngram_range=(1, 5))
    ngram_count_sparse = ngram_bow.fit_transform(file_iterator)
    ngram_count = pd.DataFrame(ngram_count_sparse.toarray())
    ngram_count.columns = ngram_bow.get_feature_names()
    return ngram_count

def ngram_df_from_idfile(idfile, path, end=".txt"):
    file_iterator = [os.path.join(path, line.strip() + end) for line in idfile]
    return ngram_df(file_iterator)

def write_ngramf_df_from_idfile(idfilename, idfiledir, path, resultfilename, end=".txt"):
    """

    :param idfilename: relative name of idfile
    :param idfiledir: path to idfile
    :param path: path to id files
    :param end: suffix (e.g., file type) for filenames
    :return:
    """
    with open(os.path.join(idfiledir, idfilename)) as idfile:
        df = ngram_df_from_idfile(idfile, path, end)
        df.to_csv(path_or_buf=resultfilename, sep="\t")

def write_ngram_df_fanfic():
    proj_dir = "/Volumes/2TB/Final_Project"
    idfiledir = os.path.join(proj_dir, "Fanfic lists")
    fanfic_dir = os.path.join(proj_dir, "Fanfic_all")
    ngrams_dir = os.path.join(proj_dir, "Ngrams_df")
    for idlist in os.listdir(idfiledir):
        if idlist.endswith(".txt"):
            print(idlist)
            write_ngramf_df_from_idfile(idfilename=idlist, idfiledir=idfiledir, path=fanfic_dir,
                                        resultfilename=os.path.join(ngrams_dir, idlist))

def ngram_series(ngram_count, cutoff=0):
    """
    The below turns the n-gram-count dataframe into a Pandas series with the n-grams as indices for ease of working with the counts.
    The second line can be used to limit the n-grams used to those with a count over a cutoff value.

    :param ngram_count: Pandas dataframe with ngram counts (from ngram_df)
    :param cutoff: the frequency threshold below which ngrams will not be included
    """
    sums = ngram_count.sum(axis=0)
    sums = sums[sums > cutoff]
    ngrams = list(sums.index.values)
    return ngrams, sums

def ngrams_from_df(ngram_df, filename, path):
    """

    :param ngram_df: dataframe containing ngrams
    :param path: the path to the ngram folders
    :return:
    """
    ngrams, sums = ngram_series(ngram_df)
    files = [open(os.path.join(path, "%d_grams/%s" % (n, filename)), "w") for n in range(1, 6)]
    freqdists = [FreqDist(), FreqDist(), FreqDist(), FreqDist(), FreqDist()]
    for ng in ngrams:
        size = len(ng.split(" "))
        freqdists[size - 1][ng] += sums[ng]
    for i in range(0, 5):
        freqdist = freqdists[i]
        file = files[i]
        tokens = freqdist.N()
        file.write("#Ngram types: %d\n" % len(freqdist))
        file.write("#Ngram tokens: %d\n" % tokens)
        rank = 1
        for tup in freqdist.most_common():
            ngram = tup[0]
            freq = tup[1]
            file.write("%d\t%s\t%d\t%f\n" % (rank, ngram, freq, freq * 1000000 / tokens))
            rank += 1
    for file in files:
        file.close()


def number_of_onegrams(sums, ngrams):
    """
    The function below gives the total number of occurrences of 1-grams in order to calculate 1-gram frequencies

    :param sums: sum of ngram_count
    :param ngrams: list of ngrams (from ngram_series)
    :return:
    """
    onegrams = 0
    for ng in ngrams:
        ng_split = ng.split(" ")
        if len(ng_split) == 1:
            onegrams += sums[ng]
    return onegrams

def base_freq(og, sums, ngrams):
    """
    The function below makes a series of 1-gram frequencies.
    This is the last resort of the back-off algorithm if the n-gram completion does not occur in the corpus with any of the prefix words.

    :param og:
    :param sums: sum of ngram_count
    :param ngrams: list of ngrams (from ngram_series)
    :return:
    """
    freqs = pd.Series()
    for ng in ngrams:
        ng_split = ng.split(" ")
        if len(ng_split) == 1:
            freqs[ng] = sums[ng] / og
    return freqs

# For use in later functions so as not to re-calculate multiple times:
# bf = base_freq(number_of_onegrams(sums))

if __name__ == "__main__":
    write_ngram_df_fanfic()
