#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peyrard_s3.S3 import ROUGE
from peyrard_s3.S3 import JS_eval
import pickle
import os
import numpy as np


def extract_feature(references, summary_text, word_embs):
    features = {}

    ### Get ROUGE-1, ROUGE-2, ROUGE-3 and ROUGE-L both Recall and Precision
    features["ROUGE_1_R"] = ROUGE.rouge_n(summary_text, references, 1, 0.)
    features["ROUGE_2_R"] = ROUGE.rouge_n(summary_text, references, 2, 0.)

    ### Get JS
    features["JS_eval_1"] = JS_eval.JS_eval(summary_text, references, 1)
    features["JS_eval_2"] = JS_eval.JS_eval(summary_text, references, 2)

    features["ROUGE_1_R_WE"] = ROUGE.rouge_n_we(summary_text, references, word_embs, 1, 0.)
    features["ROUGE_2_R_WE"] = ROUGE.rouge_n_we(summary_text, references, word_embs, 2, 0.)

    return features


def S3(references, system_summary, word_embs, model_pyr=None, model_resp=None):
    ### Extract features
    instance = extract_feature(references, system_summary, word_embs)
    features = sorted([f for f in instance.keys()])

    feature_vector = []
    for feat in features:
        feature_vector.append(instance[feat])

    ### Apply models
    X = np.array([feature_vector])
    score_pyr = model_pyr.predict(X)[0]
    score_resp = model_resp.predict(X)[0]

    return (score_pyr, score_resp)
