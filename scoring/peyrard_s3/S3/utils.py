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

from nltk.corpus import stopwords
stopset = frozenset(stopwords.words('english'))

# normalize and stem the word
def stem_word(word):
	return stemmer.stem(normalize_word(word))

# convert to unicode and convert to lower case
def normalize_word(word):
	return word.lower()

def get_len(element):
	return len(tokenizer.tokenize(element))

def get_ngrams(sentence, N):
	tokens = tokenizer.tokenize(sentence.lower())
	clean = [stemmer.stem(token) for token in tokens]
	return [gram for gram in ngrams(clean, N)]

def get_words(sentence, stem=True):
	if stem:
		words = [stemmer.stem(r) for r in tokenizer.tokenize(sentence)]
		return map(normalize_word, words)
	else:
		return map(normalize_word, tokenizer.tokenize(sentence))

