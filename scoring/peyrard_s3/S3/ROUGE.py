#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import collections

import numpy
import nltk
from nltk.util import ngrams
from peyrard_s3.S3.utils import stemmer, tokenizer, stopset, normalize_word

from scipy import spatial

import six


###################################################
###             Pre-Processing
###################################################

def get_all_content_words(sentences, N, stem):
    all_words = []
    for s in sentences:
        if stem:
            all_words.extend([stemmer.stem(r) for r in tokenizer.tokenize(s)])
        else:
            all_words.extend(tokenizer.tokenize(s))

    normalized_content_words = list(map(normalize_word, all_words))
    return normalized_content_words


def pre_process_summary(summary, N, stem=True):
    summary_ngrams = get_all_content_words(summary, N, stem)
    return summary_ngrams


def _ngrams(words, n):
    queue = collections.deque(maxlen=n)
    for w in words:
        queue.append(w)
        if len(queue) == n:
            yield tuple(queue)


def _ngram_counts(words, n):
    return collections.Counter(_ngrams(words, n))


def _ngram_count(words, n):
    return max(len(words) - n + 1, 0)


def _counter_overlap(counter1, counter2):
    result = 0
    for k, v in six.iteritems(counter1):
        result += min(v, counter2[k])
    return result


def _safe_divide(numerator, denominator):
    if denominator > 0:
        return numerator / denominator
    else:
        return 0


def _safe_f1(matches, recall_total, precision_total, alpha):
    recall_score = _safe_divide(matches, recall_total)
    precision_score = _safe_divide(matches, precision_total)
    denom = (1.0 - alpha) * precision_score + alpha * recall_score
    if denom > 0.0:
        return (precision_score * recall_score) / denom
    else:
        return 0.0


def rouge_n(peer, models, n, alpha):
    """
    Compute the ROUGE-N score of a peer with respect to one or more models, for
    a given value of `n`.
    """

    peer = pre_process_summary(peer, n)
    models = [pre_process_summary(model, n) for model in models]

    matches = 0
    recall_total = 0
    peer_counter = _ngram_counts(peer, n)
    for model in models:
        model_counter = _ngram_counts(model, n)
        matches += _counter_overlap(peer_counter, model_counter)
        recall_total += _ngram_count(model, n)
    precision_total = len(models) * _ngram_count(peer, n)
    return _safe_f1(matches, recall_total, precision_total, alpha)


def _has_embedding(ngram, embs):
    for w in ngram:
        if not (w in embs):
            return False
    return True


def _get_embedding(ngram, embs):
    res = []
    for w in ngram:
        res.append(embs[w])
    return numpy.sum(numpy.array(res), 0)


def _find_closest(ngram, counter, embs):
    ## If there is nothin to match, nothing is matched
    if len(counter) == 0:
        return "", 0, 0

    ## If we do not have embedding for it, we try lexical matching
    if not (_has_embedding(ngram, embs)):
        if ngram in counter:
            return ngram, counter[ngram], 1
        else:
            return "", 0, 0

    ranking_list = []
    ngram_emb = _get_embedding(ngram, embs)
    for k, v in six.iteritems(counter):
        ## First check if there is an exact match
        if k == ngram:
            ranking_list.append((k, v, 1.))
            continue

        ## if no exact match and no embeddings: no match
        if not (_has_embedding(k, embs)):
            ranking_list.append((k, v, 0.))
            continue

        ## soft matching based on embeddings similarity
        k_emb = _get_embedding(k, embs)
        ranking_list.append((k, v, 1 - spatial.distance.cosine(k_emb, ngram_emb)))

    ## Sort ranking list according to sim
    ranked_list = sorted(ranking_list, key=lambda tup: tup[2], reverse=True)

    ## extract top item
    return ranked_list[0]


def _soft_overlap(peer_counter, model_counter, embs):
    THRESHOLD = 0.8
    result = 0
    for k, v in six.iteritems(peer_counter):
        closest, count, sim = _find_closest(k, model_counter, embs)
        if sim < THRESHOLD:
            continue
        if count <= v:
            del model_counter[closest]
            result += count
        else:
            model_counter[closest] -= v
            result += v

    return result


def rouge_n_we(peer, models, embs, n, alpha):
    """
    Compute the ROUGE-N-WE score of a peer with respect to one or more models, for
    a given value of `n`.
    """

    peer = pre_process_summary(peer, n, False)
    models = [pre_process_summary(model, n, False) for model in models]

    matches = 0
    recall_total = 0
    peer_counter = _ngram_counts(peer, n)
    for model in models:
        model_counter = _ngram_counts(model, n)
        matches += _soft_overlap(peer_counter, model_counter, embs)
        recall_total += _ngram_count(model, n)
    precision_total = len(models) * _ngram_count(peer, n)
    return _safe_f1(matches, recall_total, precision_total, alpha)
