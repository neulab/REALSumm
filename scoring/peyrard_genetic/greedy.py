#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .nlp_utils import *

def get_len(element):
	return len(tokenizer.tokenize(element))
	
def greedy_optimizer(sorted_elements, K):
	available_space = K
	summary = []

	while True:
		for element in sorted_elements:
			len_element = get_len(element[0])
			if available_space - len_element >= 0:
				idx = sorted_elements.index(element)
				del sorted_elements[idx]  # why?
				available_space -= len_element
				summary.append(element[0])
		else:
			break

	return summary


if __name__ == '__main__':
	sentence = []
	sentence.append(('A B C D E F G H I', 7))
	sentence.append(('A B C D E F', 5))
	sentence.append(('A B C', 3))

	simple_summarizer(sentence, 10)