# A General Optimization Framework for Multi-Document Summarization Using Genetic Algorithms and Swarm Intelligence

In this project, we develop a general framework for Multi-Document Summarization based on Genetic Algorithm and Swarm Intelligence. Any objective function can be given as input to these algorithm they will use efficient search strategy to extract summaries with high scores (according to the given objective function).

If you reuse this software, please use the following citation:

```
@inproceedings{TUD-CS-20164649,
  author = {Maxime Peyrard and Judith Eckle-Kohler},
  title = {A General Optimization Framework for Multi-Document Summarization Using
Genetic Algorithms and Swarm Intelligence},
  month = {dec},
  year = {2016},
  booktitle = {Proceedings of the 26th International Conference on Computational
Linguistics (COLING 2016)},
  pages = {247 -- 257},
  location = {Osaka, Japan},
}
```

> **Abstract:** Extracting summaries via integer linear programming and submodularity are popular and successful techniques in extractive multi-document summarization. However, many interesting optimization objectives are neither submodular nor factorizable into an integer linear program. We address this issue and present a general optimization framework where any function of input documents and a system summary can be plugged in. Our framework includes two kinds of summarizers – one based on genetic algorithms, the other using a swarm intelligence approach. In our experimental evaluation, we investigate the optimization of two information-theoretic summary evaluation metrics and find that our framework yields competitive results compared to several strong summarization baselines. Our comparative analysis of the genetic and swarm summarizers reveals interesting complementary properties.


Contact person: Maxime Peyrard, peyrard@aiphes.tu-darmstadt.de

http://www.ukp.tu-darmstadt.de/

http://www.tu-darmstadt.de/


Don't hesitate to send us an e-mail or report an issue, if something is broken (and it shouldn't be) or if you have further questions.

> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication. 


## Requirements

* Numpy 1.11.1 (http://www.numpy.org)
* nltk 3.2.1 (http://www.nltk.org)

To check the installation, a trivial toy example is computed by running:
`python example.py`

### Parameter description for the Genetic Algorithm

* `fitness_fun`
  * The objective function to maximize.

* `docs`
  * The list of source documents in the format [(title, [sentence])].

* `docs_representation`
  * A possible representation for the document to speed-up evaluation. (see example.py)
  
* `population_size`
  * The number of summaries in the population.

* `survival_rate`
  * Percentage of summaries who live to the next generation.

* `mutation_rate`
  * Percentage of summaries which will undergo a mutation.

* `reproduction_rate`
  * Percentage of summaries which will be born in the new generation.

* `maximization`
  * True if the function should be maximized, False otherwise.

### Parameter description for the Swarm Intelligence

* `fitness_fun`
  * The objective function to maximize.

* `docs`
  * The list of source documents in the format [(title, [sentence])].

* `docs_representation`
  * A possible representation for the document to speed-up evaluation. (see example.py)
  
* `number_location`
  * The number of food location in the field.

* `trial_limit`
  * Number of neighbors checked by a worker bee before moving somewhere else.

* `mfe`
  * Maximal number of function evaluation before terminating the algorithm.

* `maximization`
  * True if the function should be maximized, False otherwise.
