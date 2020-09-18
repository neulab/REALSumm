#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import gzip


def _convert_to_numpy(vector):
    return np.array([float(x) for x in vector])


def load_embeddings(filepath):
    dict_embedding = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.rstrip().split(" ")
            key = line[0]
            vector = line[1::]
            dict_embedding[key.lower()] = _convert_to_numpy(vector)
    return dict_embedding
