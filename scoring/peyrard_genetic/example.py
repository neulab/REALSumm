#!/usr/bin/env python
# -*- coding: utf-8 -*-

from JS import js_divergence, compute_tf

from GeneticOptimizer import GeneticOptimizer
from SwarmOptimizer import SwarmOptimizer

def JS_Gen(docs, length_max, epoch, population_size=1000):
	sentences = []
	for title, doc in docs:
		sentences.append(title)
		sentences.extend(doc)

	doc_freq = compute_tf(sentences)
	
	gen_optimizer = GeneticOptimizer(fitness_fun=js_divergence, 
									 docs=docs, 
									 docs_representation = doc_freq,
									 max_length=length_max, 
									 population_size=population_size, 
									 survival_rate=0.4,
									 mutation_rate=0.2,
									 reproduction_rate=0.4,  
									 maximization=False)

	return gen_optimizer.evolve(epoch)

def JS_Swarm(docs, length_max, mfe=80000, number_locations=1000):
	sentences = []
	for title, doc in docs:
		sentences.append(title)
		sentences.extend(doc)

	doc_freq = compute_tf(sentences)
	
	swarm_optimizer = SwarmOptimizer(fitness_fun=js_divergence, 
									 docs=docs, 
									 docs_representation = doc_freq,
									 max_length=length_max, 
									 number_locations=number_locations, 
									 trial_limit=400,
									 mfe=mfe,  
									 maximization=False)

	return swarm_optimizer.swarm_disperse()

if __name__ == '__main__':
	doc_1 = ("title of the first document", ["first sentence of first doc", "second sentence", "third sentence of the first document here", "another one", "what is going on "])
	doc_2 = ("second title", ["one sentnece quite random", "here is another one completely random", "sentence here", "que pasa", "a sentence in an other document"])
	doc_3 = ("title of the third document", ["it will be a short docuemnt", "only two sentences"])
	docs = [doc_1, doc_2, doc_3]

	length_max = 10
	epoch = 20
	population_size = 10
	print "Genetic Algorithm example:"
	print JS_Gen(docs, length_max, epoch, population_size)

	print "\n==================\n"
	mfe = 400
	number_locations = population_size
	print "Swarm Intelligence example:"
	print JS_Swarm(docs, length_max, mfe, number_locations)