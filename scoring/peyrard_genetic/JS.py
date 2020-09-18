#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from peyrard_genetic.nlp_utils import *
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()


def get_all_content_words_lemmatized(sentences, N=1):
    all_words = []
    for s in sentences:
        all_words.extend([wordnet_lemmatizer.lemmatize(r) for r in tokenizer.tokenize(s)])
    if N == 1:
        content_words = [w for w in all_words if w not in stopset]
    normalized_content_words = map(normalize_word, content_words)
    if N > 1:
        return [gram for gram in ngrams(normalized_content_words, N)]
    return normalized_content_words


def get_all_content_words_stemmed(sentences, N=1):
    def is_ngram_content(g):
        for a in g:
            if not (a in stopset):
                return True
        return False

    all_words = []
    for s in sentences:
        all_words.extend([stemmer.stem(r) for r in tokenizer.tokenize(s)])

    if N == 1:
        content_words = [w for w in all_words if w not in stopset]
    else:
        content_words = all_words

    normalized_content_words = list(map(normalize_word, content_words))
    if N > 1:
        return [gram for gram in ngrams(normalized_content_words, N) if is_ngram_content(gram)]
    return normalized_content_words


def get_all_content_words(sentences, N=1):
    all_words = []
    for s in sentences:
        all_words.extend(tokenizer.tokenize(s))
    content_words = [w for w in all_words if w not in stopset]
    normalized_content_words = map(normalize_word, content_words)
    if N > 1:
        return [gram for gram in ngrams(normalized_content_words, N)]
    return normalized_content_words


def get_content_words_in_sentence(sentence):
    words = tokenizer.tokenize(sentence)
    return [w for w in words if w not in stopset]


def compute_tf_doc(docs, N=1):
    sentences = []
    for title, doc in docs:
        sentences.append(title)
        sentences.extend(doc)

    content_words = list(set(get_all_content_words_stemmed(sentences, N)))
    docs_words = []
    for title, doc in docs:
        s_tmp = [title]
        s_tmp.extend(doc)
        docs_words.append(get_all_content_words_stemmed(s_tmp, N))

    word_freq = {}
    for w in content_words:
        w_score = 0
        for d in docs_words:
            if w in d:
                w_score += 1
        if w_score != 0:
            word_freq[w] = w_score

    content_word_tf = dict((w, f / float(len(word_freq.keys()))) for w, f in word_freq.items())
    return content_word_tf


def compute_word_freq(words):
    word_freq = {}
    for w in words:
        word_freq[w] = word_freq.get(w, 0) + 1
    return word_freq


def compute_tf(sentences, N=1):
    content_words = get_all_content_words_stemmed(sentences, N)
    content_words_count = len(content_words)
    content_words_freq = compute_word_freq(content_words)

    content_word_tf = dict((w, f / float(content_words_count)) for w, f in content_words_freq.items())
    return content_word_tf


def compute_average_freq(l_freq_1, l_freq_2):
    average_freq = {}

    keys = set(l_freq_1.keys()) | set(l_freq_2.keys())

    for k in keys:
        s_1 = l_freq_1.get(k, 0)
        s_2 = l_freq_2.get(k, 0)

        average_freq[k] = (s_1 + s_2) / 2.

    return average_freq


def kl_divergence(summary_freq, doc_freq):
    sum_val = 0
    for w, f in summary_freq.items():
        if w in doc_freq:
            sum_val += f * math.log(f / float(doc_freq[w]))

    return sum_val


def js_divergence(sys_summary, doc_freq, N=2):
    summary_freq = compute_tf(sys_summary, N=N)
    average_freq = compute_average_freq(summary_freq, doc_freq)

    jsd = kl_divergence(summary_freq, average_freq) + kl_divergence(doc_freq, average_freq)
    return jsd / 2.
