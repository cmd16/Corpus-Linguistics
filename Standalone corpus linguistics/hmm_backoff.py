# Adopted from https://medium.com/@davidmasse8/predicting-the-next-word-back-off-language-modeling-8db607444ba9

import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import word_tokenize, WhitespaceTokenizer, TweetTokenizer
np.random.seed(seed=234)

def ngram_df(file_iterator):
    """
    The below breaks up the words into n-grams of length 1 to 5 and puts their counts into a Pandas dataframe with the n-grams as column names.
    The maximum number of n-grams can be specified if a large corpus is being used.

    :param file_iterator: An iterable which yields either str, unicode or file objects
    """
    ngram_bow = CountVectorizer(tokenizer=word_tokenize, ngram_range=(1, 5))
    ngram_count_sparse = ngram_bow.fit_transform(file_iterator)
    ngram_count = pd.DataFrame(ngram_count_sparse.toarray())
    ngram_count.columns = ngram_bow.get_feature_names()
    return ngram_count

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
    return ngrams

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

