#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
from copy import deepcopy

from peyrard_genetic.greedy import greedy_optimizer

from peyrard_genetic.JS import js_divergence

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

class SwarmOptimizer(object):
	def __init__(self, fitness_fun, docs,  docs_representation, max_length, number_locations, trial_limit, mfe, args=None, maximization=False):
		np.random.seed(123)

		self._fitness_fun = fitness_fun
		self._args = args
		self._maximization = maximization

		self._number_locations = number_locations
		self._trial_limit = trial_limit
		self._mfe = mfe

		self._docs = docs
		self._docs_representation = docs_representation
		self._max_length = max_length

		self._sentences = []
		self._sentence_tokens = []
		for title, doc in docs:
			self._sentences.append(title)
			self._sentence_tokens.append(tokenizer.tokenize(title))
			self._sentences.extend(doc)
			for s in doc:
				self._sentence_tokens.append(tokenizer.tokenize(s))


	def _create_random_food_location(self):
		random_scores = np.random.rand(len(self._sentences))
		scored_sentences = zip(self._sentences, random_scores)
		sorted_sentences = sorted(scored_sentences, key=lambda tup: tup[1], reverse=True)
		return greedy_optimizer(sorted_sentences, self._max_length)

	def _generate_random_foods(self, n):
		foods = []
		for i in xrange(n):
			foods.append(self._create_random_food_location())
		return foods

	def _len_location(self, location):
		len_ = 0
		for sentence in location:
			len_ += len(tokenizer.tokenize(sentence))
		return len_

	def _score_food_location(self, food_location):
		if self._args:
			return self._fitness_fun(food_location, self._docs_representation, self._args)
		return self._fitness_fun(food_location, self._docs_representation)

	def _random_local_search(self, food_location_old):
		food_location = deepcopy(food_location_old)
		sentence_to_remove = random.choice(food_location)
		idx = food_location.index(sentence_to_remove)
		del food_location[idx]

		available_size = self._max_length - self._len_location(food_location)
		
		available_sentences = [s[0] for s in zip(self._sentences, self._sentence_tokens) if len(s[1]) <= available_size]
		if available_sentences != []:
			sentence_to_add = random.choice(available_sentences)
			food_location.append(sentence_to_add)
				
		return food_location

	def initial_foods(self):
		initial_foods = self._generate_random_foods(self._number_locations)
		print "initial number of foods :", len(initial_foods)
		return initial_foods

	def _is_better(self, score_a, score_b):
		if self._maximization:
			return score_a > score_b
		return score_a < score_b

	def swarm_disperse(self):
		foods_locations = self.initial_foods()
		score_vector = [self._score_food_location(loc) for loc in foods_locations]
		trials = [0] * len(foods_locations)
		number_fitness_evalutation = len(foods_locations)

		size_10_percent = int(0.1 * len(foods_locations))
		if self._maximization:
			best_location = (None, -10000)
		else:
			best_location = (None, 10000)

		epoch = 0
		while True:
			epoch += 1
			print "epoch: ", epoch, " -- best location: ", best_location

			# Employed Bees Phase
			for i, location in enumerate(foods_locations):
				new_location = self._random_local_search(location)
				score = self._score_food_location(new_location)
				number_fitness_evalutation += 1

				if self._is_better(score, score_vector[i]):
					if self._is_better(score, best_location[1]):
						best_location = (new_location, score)

					score_vector[i] = score
					foods_locations[i] = new_location
					trials[i] = 0
				else:
					trials[i] += 1

				if number_fitness_evalutation >= self._mfe:
					return best_location

			sum_ = sum(score_vector)
			probability_vector = [s / float(sum_) for s in score_vector]

			# Onlooker Bees Phase
			s = 0
			t = 1
			while t < self._number_locations:
				r = random.uniform(0, 1)
				if r < probability_vector[s]:
					t += 1
					location = foods_locations[s]
					new_location = self._random_local_search(location)
					score = self._score_food_location(new_location)
					number_fitness_evalutation += 1

					if self._is_better(score, score_vector[i]):
						if self._is_better(score, best_location[1]):
							best_location = (new_location, score)

						score_vector[i] = score
						foods_locations[i] = new_location
						trials[i] = 0
					else:
						trials[i] += 1

					if number_fitness_evalutation >= self._mfe:
						return best_location
				s += 1
				if s == self._number_locations:
					s = 0

			# Scout Bees Phase
			mi = trials.index(max(trials))
			if trials[mi] > self._trial_limit:
				new_location = self._create_random_food_location()
				score = self._score_food_location(new_location)
				number_fitness_evalutation += 1
				trials[mi] = 0

				if self._is_better(score, best_location[1]):
					best_location = (new_location, score)

				if number_fitness_evalutation >= self._mfe:
					return best_location

		return best_location
