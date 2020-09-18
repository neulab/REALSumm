#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .JS import js_divergence, compute_tf
from .GeneticOptimizer import GeneticOptimizer, save_scored_population
from joblib import Parallel, delayed, parallel_backend
import argparse
import os
import logging
import re
from utils import logger, init_logger
from scorer import get_bert_score_onlyVal
from utils import read_file
from all_metrics.get_rouge_pyrouge import get_rouge


def get_sents(text, sent_start_tag, sent_end_tag):
    sents = re.findall(r'%s (.+?) %s' % (sent_start_tag, sent_end_tag), text)
    sents = [sent for sent in sents if len(sent) > 0]  # remove empty sents
    return sents


def generate(src_doc_str, tgt_doc_str, length_max, n_epochs,
             out_path, population_size, doc_num, optim_metric,
             moverscore_args,
             prf='f'):
    logger.info("started doc {}".format(doc_num))

    src_doc_sentlist = get_sents(src_doc_str, sent_start_tag='<t>', sent_end_tag='</t>')
    tgt_doc_sentlist = get_sents(tgt_doc_str, sent_start_tag='<t>', sent_end_tag='</t>')

    # keep the heading an empty string
    src_doc_sentlist_tuple = [("", src_doc_sentlist)]

    if optim_metric == "js2":
        tgt_docs_rep = compute_tf(tgt_doc_sentlist, N=2)
        fitness_fun = js_divergence
        fitness_fun_args = {
            'N': 2
        }
        maximization = False
    elif optim_metric == "moverscore":
        from scorer import get_moverscore_forGA
        tgt_docs_rep = " ".join(tgt_doc_sentlist)
        maximization = True
        fitness_fun = get_moverscore_forGA
        fitness_fun_args = moverscore_args
    elif optim_metric == "bertscore":
        tgt_docs_rep = tgt_doc_sentlist
        fitness_fun = get_bert_score_onlyVal
        fitness_fun_args = {'scorer': scorer}
        maximization = True
    else:
        tgt_docs_rep = " ".join(tgt_doc_sentlist)
        maximization = True
        fitness_fun = get_rouge

        if optim_metric == 'rouge-1':
            metric_to_get = 'rouge-n'
            max_n = 1
        elif optim_metric == 'rouge-2':
            metric_to_get = 'rouge-n'
            max_n = 2
        elif optim_metric == 'rouge-l':
            metric_to_get = 'rouge-l'
            max_n = 1
        elif optim_metric == 'rouge-w':
            metric_to_get = 'rouge-w'
            max_n = 1
        else:
            raise NotImplementedError(f"expected rouge type ['rouge-1', 'rouge-2', 'rouge-l', 'rouge-w'] "
                                      f"but found {optim_metric}")
        fitness_fun_args = {
            'rouge_type': optim_metric,
            'prf': prf,
            'metric_to_get': metric_to_get,
            'max_n': max_n
        }

    gen_optimizer = GeneticOptimizer(fitness_fun=fitness_fun,
                                     docs=src_doc_sentlist_tuple,
                                     docs_representation=tgt_docs_rep,
                                     max_length=length_max,
                                     population_size=population_size,
                                     survival_rate=0.4,
                                     mutation_rate=0.4,
                                     reproduction_rate=0.4,
                                     maximization=maximization,
                                     fitness_fun_args=fitness_fun_args)

    best_individual, sorted_population = gen_optimizer.evolve(n_epochs)
    logger.info(f"Gen (with optim_metric: {optim_metric}) complete for doc "
                f"{doc_num} with best score in last gen: {best_individual[1] * 100:.2f}")

    outfile_path = os.path.join(out_path, f"out_doc_{doc_num}_{optim_metric}_{(best_individual[1] * 100):.2f}")
    save_scored_population(sorted_population, outfile_path, gen_optimizer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_jobs", type=int, default=32, help="number of parallel multiprocessing jobs for Rouge_Gen")
    parser.add_argument("--n_epochs", type=int, required=True, help="number of epochs (generations) to run")
    parser.add_argument("--max_len", type=int, required=True, help="max len (number of tokens) of generated docs")
    parser.add_argument("--pop_size", type=int, required=True, help="population size")
    parser.add_argument("--src_docs", type=str, required=True, help="file containing src docs (1 doc/line)")
    parser.add_argument("--tgt_docs", type=str, required=True, help="file containing tgt docs (1 doc/line) against "
                                                                    "which Rouge_Gen will optimize Rouge")
    parser.add_argument("--out_path", type=str, required=True,
                        help="dir where outputs for each generation will be saved")
    parser.add_argument("--log_path", type=str, required=True, help="path to save the logs")
    parser.add_argument("--start_doc_idx", type=int, default=0, help="start running from this doc")
    parser.add_argument("--end_doc_idx", type=int, default=None, help="run upto this doc (inclusive)")
    parser.add_argument("--store_each_gen", action="store_true", help="set this flag to store output "
                                                                      "from each generation")
    parser.add_argument("--metric", required=True, choices=["js2", "bertscore", "rouge-1",
                                                            "rouge-2", "rouge-l", "moverscore"],
                        help="metric to use as optimizer in genetic algorithm")
    args = parser.parse_args()

    assert os.path.isdir(args.out_path), f"{args.out_path} should be an existing directory"

    logger = init_logger(log_file=args.log_path, log_file_level=logging.INFO)
    logger.info(f"optimizing metric: {args.metric}")
    logger.info(f"reading src docs from {args.src_docs}")
    logger.info(f"reading tgt docs from {args.tgt_docs}")

    src_docs = read_file(args.src_docs)
    tgt_docs = read_file(args.tgt_docs)
    assert len(src_docs) == len(tgt_docs), "src_docs and tgt_docs should have equal number of docs"
    logger.info(f"{len(src_docs)} docs read")

    if args.end_doc_idx is None:
        args.end_doc_idx = len(src_docs)
    assert len(tgt_docs) >= args.end_doc_idx >= 0

    # if metric is moverscore, prepare the fitness func args here itself (optimization)
    if args.metric == 'moverscore':
        from all_metrics.moverscore import get_idf_dict
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            stop_words = set(f.read().strip().split(' '))
        moverscore_args = {
            'idf_dict_ref': get_idf_dict([" ".join(ref) for ref in src_docs]),
            'idf_dict_hyp': get_idf_dict([" ".join(src) for src in tgt_docs]),
            'stop_words': stop_words
        }
    else:
        moverscore_args = None

    if args.metric == 'bertscore':
        from bert_score import BERTScorer
        scorer = BERTScorer(lang='en', rescale_with_baseline=True)

    with parallel_backend('multiprocessing', args.n_jobs):
        Parallel()(
            delayed(generate)(src_doc_str=src_docs[doc_num],
                              tgt_doc_str=tgt_docs[doc_num],
                              length_max=args.max_len,
                              n_epochs=args.n_epochs,
                              population_size=args.pop_size,
                              doc_num=doc_num,
                              optim_metric=args.metric,
                              out_path=args.out_path,
                              moverscore_args=moverscore_args,
                              prf='f',
                              )
            for doc_num in range(args.start_doc_idx, args.end_doc_idx)
        )

    # To run for CNNDM JS
    # python -m peyrard_genetic.run --n_jobs 5 --n_epochs 10 --max_len 60 --pop_size 400 --src_docs ../data/cnn_dm/test/src.txt \
    # --tgt_docs ../data/cnn_dm/test/ref.txt --out_path ../data/cnn_dm/genetic_out_js_2 --js_type 2 --n_docs 5 \
    # --log_path ../logs/cnn_dm_genetic_js_2.log

    # To run for XSUM JS
    # python -m peyrard_genetic.run --n_jobs 5 --n_epochs 10 --max_len 35 --pop_size 400 --src_docs ../data/xsum/test/src.txt \
    # --tgt_docs ../data/xsum/test/ref.txt --out_path ../data/xsum/genetic_out_js_2 --js_type 2 --n_docs 5 \
    # --log_path ../logs/xsum_genetic_js_2.log
