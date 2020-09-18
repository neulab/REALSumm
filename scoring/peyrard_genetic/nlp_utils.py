#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, unicode_literals

# Get the python version (used to try decode an unknow instance to unicode)
from sys import version_info

PY3 = version_info[0] == 3

# Use classical Snowball stemmer for english
import nltk
from nltk.util import ngrams

from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
# class WordTokenizer(object):
# 	"""docstring for WordTokenizer"""
# 	def __init__(self):
# 		pass
# 	def tokenize(self, arg):
# 		return nltk.word_tokenize(arg)
# tokenizer =  WordTokenizer()


from nltk.corpus import stopwords

stopset = frozenset(stopwords.words('english'))


#  Convert an object to its unicode representation (if possible)
def to_unicode(object):
    if isinstance(object, unicode):
        return object
    elif isinstance(object, bytes):
        return object.decode("utf8")
    else:
        print(str(object))
        if PY3:
            if hasattr(instance, "__str__"):
                return unicode(instance)
            elif hasattr(instance, "__bytes__"):
                return bytes(instance).decode("utf8")
        else:
            if hasattr(instance, "__unicode__"):
                return unicode(instance)
            elif hasattr(instance, "__str__"):
                return bytes(instance).decode("utf8")


#  normalize and stem the word
def stem_word(word):
    return stemmer.stem(normalize_word(word))


#  convert to unicode and convert to lower case
def normalize_word(word, already_unicode=True):
    if already_unicode:
        return word.lower()
    return to_unicode(word).lower()


#  convert the sentence to a list of tokens
def sentence_tokenizer(sentence):
    return tokenizer.tokenize(sentence)


def get_len(element):
    return len(tokenizer.tokenize(element))


def get_ngrams(sentence, N):
    tokens = tokenizer.tokenize(sentence.lower())
    clean = [stemmer.stem(token) for token in tokens]
    return [gram for gram in ngrams(clean, N)]
