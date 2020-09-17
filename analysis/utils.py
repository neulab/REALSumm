import numpy as np
import pickle
import logging

from scipy.stats import pearsonr, spearmanr, kendalltau
from joblib import Parallel, delayed
from joblib import parallel_backend
from tabulate import tabulate
from collections import defaultdict as ddict


logger = logging.getLogger()
doc_y_types = ['ktau', 'pearson', 'spearman', 'm']


def init_logger(log_file=None, log_file_level=logging.NOTSET, format='simple'):
    if format == 'simple':
        log_format = logging.Formatter("[%(asctime)s %(levelname)s %(filename)s:%(lineno)s "
                                       ": %(funcName)s()] %(message)s")
    else:
        log_format = logging.Formatter("[%(asctime)s %(levelname)s %(filename)s:%(lineno)s "
                                       "PID %(process)d PN %(processName)s "
                                       "TID %(thread)d TN %(threadName)s "
                                       ": %(funcName)s()] %(message)s")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]

    if log_file and log_file != '':
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_file_level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger


def get_pickle(file_path):
    with open(file_path, 'rb') as fp:
        x = pickle.load(fp)
    return x


def print_score_ranges(sd):
    metrics_list = get_metrics_list(sd)
    print_list = []
    headers = ["min", "25-perc", "median", "75-perc", "max", "mean"]
    for m in metrics_list:
        scores = [s['scores'][m] for d in sd.values() for s in d['system_summaries'].values()]
        print_list.append([m,
                           np.min(scores),
                           np.percentile(scores, 25),
                           np.median(scores),
                           np.percentile(scores, 75),
                           np.max(scores),
                           np.mean(scores)])
    print(tabulate(print_list, headers=headers, floatfmt=".6f", tablefmt="simple"))


def get_metrics_list(sd):
    """
    Does each system summary dict have same all_metrics?
    :param sd: scores dict
    :return: list of all_metrics in the scores dict
    """
    metrics_tuple_set = set(
        [tuple(sorted(list(x['scores'].keys())))
         for d in sd.values() for x in d['system_summaries'].values()])
    assert len(metrics_tuple_set) == 1, (metrics_tuple_set, "all system summary score dicts should have the same set of all_metrics")
    metrics_list = list(list(metrics_tuple_set)[0])
    return metrics_list


def print_ktau_matrix(metrics, percentile, sd, cutoff_metric='bert_f_score', y_type='ktau', n_jobs=8):
    high_pvals = 0
    print(metrics)
    human_scores = []
    for min_j, mx in enumerate(metrics):
        mean_ktaus = np.zeros((len(percentile), len(metrics)))
        for i, perc in enumerate(percentile):
            for j, my in enumerate(metrics):
                if mx == my or j <= min_j:
                    continue
                with parallel_backend('multiprocessing', n_jobs=n_jobs):
                    ktaus_pvals = Parallel()(
                        delayed(get_doc_y_val)(isd, mx, my, y_type=y_type, cutoff_metric=cutoff_metric, percentile=perc)
                        for doc_num, isd in enumerate(sd.values())
                    )
                ktaus = []
                for ktau, pval in ktaus_pvals:
                    # ktaus.append(ktau)
                    if pval <= 0.05:
                        ktaus.append(ktau)
                    else:
                        high_pvals += 1
                mean_ktaus[i, j] = np.mean(ktaus)
                if my == 'pyr_score' or my == 'litepyramid_recall':
                    human_scores.append(mean_ktaus[i, j])
                # logger.info(f"Finished {mx} {my} {perc}: {mean_ktaus[i, j]}")

        print(mean_ktaus)
        print()

    total_ktaus = (len(metrics) / 2) * (len(metrics) - 1) * len(percentile) * len(sd)
    print(f"total {high_pvals}/{total_ktaus} = {high_pvals * 100 / total_ktaus}% values ignored")
    return human_scores


def filter_summaries(isd, cutoff_metric, percentile):
    c_scores = [summdict['scores'][cutoff_metric] for summdict in isd['system_summaries'].values()]
    cutoff_score_min = np.percentile(c_scores, percentile[0])
    cutoff_score_max = np.percentile(c_scores, percentile[1])
    filtered_sumdicts_l = [summdict for summdict in isd['system_summaries'].values()
                           if (
                                   (summdict['scores'][cutoff_metric] >= cutoff_score_min)
                                   and (summdict['scores'][cutoff_metric] <= cutoff_score_max)
                           )
                           ]
    return filtered_sumdicts_l


def get_doc_y_val(isd, m1, m2, y_type, cutoff_metric=None, percentile=None):
    assert (y_type in doc_y_types)
    if y_type == 'm':
        return isd['mean_scores'][m1], 0

    filtered_summaries = isd['system_summaries'].values()
    if cutoff_metric is not None:
        filtered_summaries = filter_summaries(isd, cutoff_metric, percentile)

    m1_scores = [summdict['scores'][m1] for summdict in filtered_summaries]
    m2_scores = [summdict['scores'][m2] for summdict in filtered_summaries]

    if y_type == 'ktau':
        ktau, pval = kendalltau(m1_scores, m2_scores, nan_policy="raise")
        if np.isnan(ktau):
            # return high pvalue to ignore
            return 0, 1
            # return 0, 1, 1
            # import pdb; pdb.set_trace()
        return ktau, pval
        # return ktau, pval, len(filtered_summaries)

    elif y_type == 'pearson':
        pearson_corr, pval = pearsonr(m1_scores, m2_scores)
        return pearson_corr, pval

    elif y_type == 'spearman':
        # TODO: is this tested?
        spearman_corr, pval = spearmanr(m1_scores, m2_scores)
        return spearman_corr, pval


def get_system_level_scores(sd, metrics, agg='mean', nas=False):
    systems = ddict(lambda: ddict(list))

    for isd in sd.values():
        for system_name, scores in isd['system_summaries'].items():
            for m in metrics:
                systems[system_name][m].append(scores['scores'][m])

    for system_name, scores in systems.items():
        for m in scores:
            all_scores = systems[system_name][m]
            if agg == 'mean':
                systems[system_name][m] = np.mean(all_scores)

    if nas:
        min_scores = {}
        max_scores = {}
        for m in metrics:
            min_scores[m] = np.min([systems[sys][m] for sys in systems.keys()])
            max_scores[m] = np.max([systems[sys][m] for sys in systems.keys()])
        for sys in systems:
            systems[sys]['nas'] = np.mean([
                (systems[sys][m] - min_scores[m]) / (max_scores[m] - min_scores[m]) for m in metrics
            ])

    return systems


def get_topk(systems, k, metric='rouge_2_f_score'):
    systems_l = [(name, score[metric]) for name, score in systems.items()]
    systems_l = sorted(systems_l, key=lambda x: x[1], reverse=True)
    topk_system_names = [tup[0] for tup in systems_l[:k]]
    return {name: systems[name] for name in topk_system_names}


def get_correlation(topk_systems, metric_pairs, method='pearson'):
    # disagreement between every pair of metrics for the topk
    corr = {}
    pval = {}
    for pair in metric_pairs:
        m1_scores = []
        m2_scores = []
        for scores in topk_systems.values():
            m1_scores.append(scores[pair[0]])
            m2_scores.append(scores[pair[1]])

        if method == 'pearson':
            correlation, p_value = pearsonr(m1_scores, m2_scores)
        elif method == 'kendalltau':
            correlation, p_value = kendalltau(m1_scores, m2_scores)
        else:
            raise ValueError(f"method {method} not supported")

        key = '_'.join(pair)
        corr[key] = correlation
        pval[key] = p_value

    return corr, pval
