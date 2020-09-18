import argparse
import logging
import os
import glob
import pickle
from pprint import pprint
from joblib import Parallel, delayed
from joblib import parallel_backend
from os.path import join as pjoin

from utils import init_logger

ARTICLE_FILENAME = "src.txt"
REFERENCE_SUM_FILENAME = "ref.txt"
SYSTEM_SUM_FILE_REGEX = "out*.txt"

DEBUG = False


def get_model_paths(data_path):
    model_paths = []
    for model_dir in os.listdir(data_path):
        model_path = pjoin(data_path, model_dir)
        if not os.path.isdir(model_path):
            continue
        model_paths.append(model_path)
    return model_paths


def get_num_lines_ref(data_path):
    """
    Returns the number of ref summaries found in data_path. Also checks if the references of all models have
    the same length.
    :param data_path: Path to root dir of all models
    :return: number of ref summareis found
    """
    nlines = []
    for model_path in get_model_paths(data_path):
        ref_path = pjoin(model_path, REFERENCE_SUM_FILENAME)
        with open(ref_path, 'r') as f:
            nlines.append(sum([1 for _ in f]))

    assert len(set(nlines)) == 1, f"Unequal ref lines in {data_path}: {nlines}"
    return nlines[0]


def get_scores_dict_parallel(document_path, reference_summ_path, system_summ_paths, model_name, metric):
    from scorer import Scorer
    scorer = Scorer(src_path=document_path,
                    ref_path=reference_summ_path,
                    metric=metric,
                    fast_moverscore=args.fast_moverscore,
                    ref_sep=args.ref_sep,
                    num_ref=args.num_ref)

    with parallel_backend('multiprocessing', n_jobs=args.n_jobs):
        score_dicts = Parallel()(
            delayed(scorer.score)(file_num, summ_path, model_name, summ_path.split('/')[-1])
            for file_num, summ_path in enumerate(system_summ_paths)
        )

    return score_dicts


def main(data_path, out_path, metric):
    """
    Updates the scores dict and saves it
    :param data_path: path to top level folder with structure:
           model_name/variant_name/src.txt, model_name/variant_name/ref.txt, model_name/variant_name/out*.txt
    :param out_path: output path to save pickle dict
    :param metric: The metric to use for scoring
    :param save_src_doc: save the source docs in the scores dict. Set False to save space, esp. for Genetic outputs.
    :return: a dict of form
    scores_dict[line_num_int] =
    [{"model_name":"abisee-ptr-gen", "document":"", "reference_summary":"", "system_summary":"", "rouge-1":10.04, ..},
     {"model_name":"abisee-ptr-gen-cov", "document":"", "reference_summary":"", "system_summary":"", "rouge-2":10.04, ..}
      ...
    ]
    """
    all_scores_dict = {}
    num_lines_ref = get_num_lines_ref(data_path)
    for line_num in range(num_lines_ref):
        all_scores_dict[line_num] = {'doc_id': line_num, 'ref_summ': '', 'system_summaries': {}}

    # for each model directory, update all_scores_dict with score dicts from all of the model-variants of that model
    for model_path in get_model_paths(data_path):
        logger.info(f"getting scores for documents in {model_path}")
        reference_summ_path = pjoin(model_path, REFERENCE_SUM_FILENAME)
        document_path = pjoin(model_path, ARTICLE_FILENAME)
        system_summ_paths = glob.glob(model_path + f'/{SYSTEM_SUM_FILE_REGEX}')

        assert len(system_summ_paths) >= 1, "No out file found in {}".format(model_path)

        model_score_dicts = get_scores_dict_parallel(document_path=document_path,
                                                     reference_summ_path=reference_summ_path,
                                                     system_summ_paths=system_summ_paths,
                                                     model_name=model_path.split('/')[-1],
                                                     metric=metric)

        # update scores dict
        for doc_id in all_scores_dict.keys():
            all_scores_dict[doc_id]['ref_summ'] = model_score_dicts[0][doc_id]['ref_summ']
            for modelvariant_score_dict in model_score_dicts:
                all_scores_dict[doc_id]['system_summaries'].update(modelvariant_score_dict[doc_id]['system_summaries'])

    with open(out_path, 'wb') as fp:
        pickle.dump(all_scores_dict, fp)
    print(f"stored dict at {out_path}")

    if DEBUG:
        print("scores dict:")
        pprint(all_scores_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metric', required=True,
                        choices=['rouge', 'js2', 'bertscore', 'rwe', 'moverscore', 'wms', 'sms'],
                        help="Metrics to get.")
    parser.add_argument("-dp", '--data_path', type=str,
                        help="path of directory containing model directories which contain src.txt, "
                             "ref.txt and out.txt files", required=True)
    parser.add_argument("-op", '--output_path', type=str,
                        help="path at which to store dict with scores", required=True)
    parser.add_argument("-lp", '--log_path', type=str,
                        help="path of log file", required=True)
    parser.add_argument("-num_ref", type=int, default=1, help="specify num references per doc")
    parser.add_argument('-ref_sep', default='||NEVER||',
                        help='what is the ref separator. Keep a super unique sequence if only 1 ref per doc.')
    parser.add_argument("-n_jobs", type=int, default=1, help="Number of cores to parallelize over.")
    parser.add_argument("-fast_moverscore", action='store_true', help="makes moverscore scoring faster")

    args = parser.parse_args()
    logger = init_logger(args.log_path, logging.INFO)
    main(data_path=args.data_path,
         out_path=args.output_path,
         metric=args.metric)

    # To run:
    # python get_scores.py -dp ../data/cnn_dm_collected_system_outputs/micro/abs -op ../score_dicts/debug.pkl -lp ../logs/scores.log -n_jobs 1 -m rouge
