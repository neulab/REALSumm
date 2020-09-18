#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pdb
import traceback

import numpy as np
import random
from copy import deepcopy

from .greedy import greedy_optimizer

from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm

from scorer import get_moverscore_forGA

tokenizer = RegexpTokenizer(r'\w+')

metrics_cache = {}

class GeneticOptimizer(object):
    def __init__(self, fitness_fun, docs, docs_representation, max_length, population_size, survival_rate,
                 mutation_rate, reproduction_rate, maximization=False, sentences_rep=None, fitness_fun_args=None,
                 doc_num=None):
        np.random.seed(123)

        self._fitness_fun = fitness_fun
        self._fitness_fun_args = fitness_fun_args
        self._population_size = population_size
        self._survival_rate = survival_rate
        self._mutation_rate = mutation_rate
        self._reproduction_rate = reproduction_rate
        self._maximization = maximization

        self._docs = docs
        self._doc_num = doc_num
        self._docs_representation = docs_representation
        self._sentences_rep = sentences_rep
        self._max_length = max_length

        self._sentences = []
        self._sentence_tokens = []
        for title, doc in docs:
            self._sentences.append(title)
            self._sentence_tokens.append(tokenizer.tokenize(title))
            self._sentences.extend(doc)
            for s in doc:
                self._sentence_tokens.append(tokenizer.tokenize(s))

    def _create_random_individual(self):
        random_scores = np.random.rand(len(self._sentences))
        scored_sentences = zip(self._sentences, random_scores)
        sorted_sentences = sorted(scored_sentences, key=lambda tup: tup[1], reverse=True)
        return greedy_optimizer(sorted_sentences, self._max_length)

    def _generate_random_population(self, n):
        population = []
        for i in range(n):
            population.append(self._create_random_individual())
        return population

    def _score_population(self, population):
        scored_population = []
        global metrics_cache

        # population is a list of generated ext. summaries (lists of sentences)
        # self._docs_representation is the tgt doc (can be list of sentences or str
        # depending on what was passed in run.py generate() function)

        # special case for moverscore
        if self._fitness_fun == get_moverscore_forGA:
            # for moverscore, ref doc should be an str
            assert type(self._docs_representation) is str
            population_as_str_list = [" ".join(individual) for individual in population]
            scores_list = self._fitness_fun(
                summaries_str_list=population_as_str_list,
                reference_str=self._docs_representation,
                **self._fitness_fun_args)
            assert len(scores_list) == len(population)
            scored_population = zip(population, scores_list)
            return scored_population

        # for all other metrics
        for individual in population:
            # score = self._fitness_fun(individual, self._docs)
            # pdb.set_trace()
            # there is a separate GeneticOptimizer object for each document, so
            # we dont need to include _docs_representation in this key.
            individual_sen = " ".join(individual)
            if len(individual_sen.strip()) == 0:
                score = 0
            elif individual_sen in metrics_cache:
                score = metrics_cache[individual_sen]
            else:
                try:
                    if self._fitness_fun_args:
                        score = self._fitness_fun(individual, self._docs_representation, **self._fitness_fun_args)
                    else:
                        score = self._fitness_fun(individual, self._docs_representation)
                except:
                    traceback.print_exc()
                    score = 0
                metrics_cache[individual_sen] = score
            scored_population.append((individual, score))

        return scored_population

    def _select_survivors(self, scored_population):
        sorted_population = sorted(scored_population, key=lambda tup: tup[1], reverse=self._maximization)

        percentage_winner = 0.5

        to_keep = int(self._survival_rate * self._population_size)
        number_winners = int(percentage_winner * to_keep)
        winners = [tup[0] for tup in sorted_population[:number_winners]]

        losers = sorted_population[number_winners:]

        number_losers = int((1 - percentage_winner) * to_keep)

        survivors = deepcopy(winners)
        random_scores = np.random.rand(len(losers))

        sorted_losers = sorted(zip(losers, random_scores), key=lambda tup: tup[1])
        loser_survivors = [tup[0][0] for tup in sorted_losers[:number_losers]]

        survivors.extend(loser_survivors)
        return survivors, winners

    def _new_generation(self, scored_population):
        new_generation, winners = self._select_survivors(scored_population)
        new_generation = self._mutate(new_generation)
        new_generation.extend(self._reproduction(winners, len(new_generation)))
        individuals_to_create = self._population_size - len(new_generation)
        new_generation.extend(self._generate_random_population(individuals_to_create))

        return new_generation

    def _len_individual(self, individual):
        len_ = 0
        for sentence in individual:
            len_ += len(tokenizer.tokenize(sentence))
        return len_

    def _mutate(self, population, mutation_rate="auto"):
        if mutation_rate == "auto":
            mutation_rate = self._mutation_rate

        nb_mutant = int(mutation_rate * len(population))

        random_scores = np.random.rand(len(population))
        sorted_population = sorted(zip(population, random_scores), key=lambda tup: tup[1])
        mutants = [tup[0] for tup in sorted_population[:nb_mutant]]

        mutated = []
        i = 0
        for mutant in mutants:
            to_mutate = deepcopy(mutant)

            sentence_to_remove = random.choice(to_mutate)
            idx = to_mutate.index(sentence_to_remove)
            del to_mutate[idx]

            available_size = self._max_length - self._len_individual(to_mutate)

            available_sentences = [s[0] for s in zip(self._sentences, self._sentence_tokens) if len(s[1]) <= available_size]
            if available_sentences != []:
                i += 1
                sentence_to_add = random.choice(available_sentences)
                to_mutate.append(sentence_to_add)

                mutated.append(to_mutate)

        population.extend(mutated)
        return population

    def _reproduction(self, population_winners, population_size, reproduction_rate="auto"):
        if reproduction_rate == "auto":
            reproduction_rate = self._reproduction_rate

        parents = []
        number_families = int(reproduction_rate * population_size)

        for i in range(number_families):
            parents.append(random.sample(population_winners, 2))

        children = []
        for father, mother in parents:
            genetic_pool = [s for s in self._sentences if s in father]
            genetic_pool.extend([s for s in self._sentences if s in mother])

            random_scores = np.random.rand(len(genetic_pool))

            scored_sentences = zip(self._sentences, random_scores)
            sorted_sentences = sorted(scored_sentences, key=lambda tup: tup[1], reverse=True)
            child = greedy_optimizer(sorted_sentences, self._max_length)

            children.append(child)

        return children

    def initial_population(self):
        initial_population = self._generate_random_population(self._population_size)
        # print("initial population len:", len(initial_population))
        return initial_population

    def _is_better(self, scored_individual, best_scored_individual):
        if self._maximization:
            return scored_individual[1] > best_scored_individual[1]
        return scored_individual[1] < best_scored_individual[1]

    def evolve(self, epoch, out_path=None, out_fname=None, save_each_gen_out=False):
        gen_placeholder_str = "#GEN"
        score_placeholder_str = "#SCORE"
        if save_each_gen_out:
            assert os.path.isdir(out_path), f"if save_outs is True, out path {out_path} should be existing directory"
            assert (out_fname is not None) and \
                   (type(out_fname) is str) and \
                   (gen_placeholder_str in out_fname) and \
                   (score_placeholder_str in out_fname), f"if save_outs is True, out_fname should be a string " \
                                            f"containing {gen_placeholder_str} and {score_placeholder_str}"
        # create initial population and scored_population
        population = self.initial_population()
        scored_population = self._score_population(population)

        # if self._maximization:
        #     best_individual = (None, -10000)
        # else:
        #     best_individual = (None, 10000)

        for i in range(epoch):
            # print("epoch: ", i, " -- best individual: ", best_individual)
            population = self._new_generation(scored_population)
            scored_population = self._score_population(population)
            sorted_population = sorted(scored_population, key=lambda tup: tup[1], reverse=self._maximization)
            best_individual_in_generation = sorted_population[0]

            # if self._is_better(best_individual_in_generation, best_individual):
            #     best_individual = best_individual_in_generation

            if save_each_gen_out:
                # get best and worst scores in this generation and multiply by 100 to express rouge as a %
                highest_score_this_gen = best_individual_in_generation[1] * 100
                lowest_score_this_gen = sorted_population[-1][1] * 100
                this_out_fname = out_fname \
                    .replace(gen_placeholder_str, f"{i:04}") \
                    .replace(score_placeholder_str, f"lowest_{lowest_score_this_gen:.2f}_best_{highest_score_this_gen:.2f}")
                this_out_file_path = os.path.join(out_path, this_out_fname)
                save_scored_population(sorted_population, this_out_file_path, self)
                # print(f"completed epoch {i} for doc {self._doc_num}, saved to {this_out_file_path}", end="\r")
            else:
                # print("completed epoch {} for doc {}".format(i, self._doc_num), end="\r")
                pass

        return best_individual_in_generation, sorted_population


def save_scored_population(scored_population, outfile_path, obj_debug=None):
    with open(outfile_path, 'w', encoding='utf-8', errors='ignore') as f:
        for individual in scored_population:
            sents = individual[0]
            sents = [sent for sent in sents if len(sent) > 0]
            ind_str = "<t> " + " </t>  <t> ".join(sents) + " </t>"
            f.write(ind_str + '\n')
