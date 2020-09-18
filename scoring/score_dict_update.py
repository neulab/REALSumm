import argparse
import copy
import os
import pdb
from utils import get_pickle, write_pickle, get_metrics_list
import numpy as np
import glob

ACCEPTABLE_METRICS = {'rouge_1_recall',
                      'rouge_1_precision',
                      'rouge_1_f_score',
                      'rouge_1_we',
                      'rouge_2_recall',
                      'rouge_2_precision',
                      'rouge_2_f_score',
                      'rouge_l_recall',
                      'rouge_l_precision',
                      'rouge_l_f_score',
                      'js-2',
                      'bert_f_score',
                      'bert_precision_score',
                      'bert_recall_score',
                      'rouge_w_f_score',
                      'mover_score'}


def sd_to_new_format_file(in_path, out_path):
    old_sd = get_pickle(in_path)
    new_sd = sd_to_new_format(old_sd)
    write_pickle(new_sd, out_path)


def sd_to_new_format(old_sd):
    new_sd = {}
    for doc_id in old_sd.keys():
        ref_summ_set = set([d['reference_summary'] for d in old_sd[doc_id]])

        # assert len(ref_summ_set) == 1, "all ref summs for a doc_id should be equal"
        ref_summ = list(ref_summ_set)[0]

        new_sd[doc_id] = {'doc_id': doc_id,
                          'ref_summ': ref_summ,
                          'system_summaries': {}
                          }
        modelnames = [d['model_name'] for d in old_sd[doc_id]]
        modelnames_unique = list(set(modelnames))
        # pdb.set_trace()
        assert len(modelnames) == len(modelnames_unique), f"modelnames should be unique in old_sd[{doc_id}]"

        for d in old_sd[doc_id]:
            d_keys = set(d.keys())
            metric_keys = d_keys - {'model_name', 'document', 'reference_summary', 'system_summary'}
            metric_keys = list(metric_keys)
            assert set(metric_keys).issubset(ACCEPTABLE_METRICS), f"metric_keys {metric_keys} should be a subset of " \
                                                                  f"acceptable_metrics {ACCEPTABLE_METRICS}"

            new_sd[doc_id]['system_summaries'][d['model_name']] = {'system_summary': d['system_summary'],
                                                                   'scores': {metric_name: float(d[metric_name]) for
                                                                              metric_name in metric_keys},
                                                                   'model_name': d['model_name']
                                                                       }
        print(f"sd_to_new_format: {doc_id}/{len(old_sd)}", end="\r")
    return new_sd


def merge_score_dicts(big_sd, new_sd):
    doc_ids = new_sd.keys()
    doc_ids2 = big_sd.keys()
    assert doc_ids == doc_ids2, "sd1 and sd2 should have same keys (doc ids)"

    for doc_id in doc_ids:
        assert new_sd[doc_id]['doc_id'] == big_sd[doc_id]['doc_id']
        # for this doc_id, get all mode_name values in sd1 and sd2
        big_sd_model_names = set(big_sd[doc_id]['system_summaries'].keys())
        for model_name in new_sd[doc_id]['system_summaries'].keys():
            if model_name in big_sd_model_names:
                new_sd_metric_names = set(new_sd[doc_id]['system_summaries'][model_name]['scores'].keys())
                big_sd_metric_names = set(big_sd[doc_id]['system_summaries'][model_name]['scores'].keys())
                # assert len(new_sd_metric_names.intersection(big_sd_metric_names)) == 0, 'big_sd and new_sd should not' \
                #                                                                         'have any redundant scores'
                # TODO: use update to update a dict
                for scores_key in ['scores', 'normed_scores']:
                    if scores_key in big_sd[doc_id]['system_summaries'][model_name]:
                        big_sd[doc_id]['system_summaries'][model_name][scores_key] = {
                            **big_sd[doc_id]['system_summaries'][model_name][scores_key],
                            **new_sd[doc_id]['system_summaries'][model_name][scores_key]
                        }
            else:
                big_sd[doc_id]['system_summaries'][model_name] = copy.deepcopy(
                    new_sd[doc_id]['system_summaries'][model_name])

        if 'min_scores' in big_sd[doc_id]:
            assert len(set(big_sd[doc_id]['min_scores'].keys()).intersection(
                set(new_sd[doc_id]['min_scores'].keys()))) == 0
            big_sd[doc_id]['min_scores'].update(new_sd[doc_id]['min_scores'])
            big_sd[doc_id]['max_scores'].update(new_sd[doc_id]['max_scores'])

        print(f"merge_score_dicts: {doc_id}/{len(doc_ids)}", end="\r")


def remove_duplicates(sd, duplicate_string='### DUPLICATE ###'):
    num_duplicates = 0
    for doc_id in sd:
        all_summaries = sd[doc_id]['system_summaries']
        original_length = len(all_summaries)
        model_names = list(all_summaries.keys())
        for model_name in model_names:
            if all_summaries[model_name]['system_summary'].startswith('#'):
                assert all_summaries[model_name]['system_summary'].strip() == duplicate_string
                all_summaries.pop(model_name)
        num_duplicates += original_length - len(all_summaries)
    print(f"removed {num_duplicates} duplicate genetic outputs from scores dict.")


def remove_dup_sys_summs(sd, eps=1e-3):
    def come_close(d1, d2):
        for key in d1:
            if abs(d1[key] - d2[key]) > eps:
                print(f"{key} scores did not match")
                return False
        return True

    num_removed_l = []
    for doc_id in sd.keys():
        # for each doc, mantain a dict of summaries we have seen and their corresponding model names
        seen_sys_summs = dict()  # key: system summary, value: model name
        num_removed = 0
        models_to_remove = []
        for model_name in sorted(sd[doc_id]['system_summaries'].keys()):
            this_sys_summ_dict = sd[doc_id]['system_summaries'][model_name]
            # if we encounter a sytem-generated summary that we have already seen,
            # make sure the scores matched too (just trying to catch bugs here :-) )
            if this_sys_summ_dict['system_summary'] in seen_sys_summs.keys():
                seen_model_name = seen_sys_summs[this_sys_summ_dict['system_summary']]
                try:
                    assert sd[doc_id]['system_summaries'][seen_model_name]['system_summary'] == this_sys_summ_dict[
                        'system_summary']
                    assert come_close(sd[doc_id]['system_summaries'][seen_model_name]['scores'],
                                      this_sys_summ_dict['scores']), \
                        f"expected close match between sd[{doc_id}]['system_summaries'][{seen_model_name}]['scores']:\n" \
                        f"{sd[doc_id]['system_summaries'][seen_model_name]['scores']}\n" \
                        f"with sys summary:\n{sd[doc_id]['system_summaries'][seen_model_name]['system_summary']}\n" \
                        f" and this_sys_summ_dict['scores']:\n" \
                        f"{this_sys_summ_dict['scores']}\n" \
                        f"of model {model_name}\n" \
                        f"with sys summary:\n{this_sys_summ_dict['system_summary']}"
                except:
                    print("Same summary but different scores")
                models_to_remove.append(model_name)
                num_removed += 1
            else:
                seen_sys_summs[this_sys_summ_dict['system_summary']] = model_name
        # remove redundant models for this doc
        for model_name in models_to_remove:
            del sd[doc_id]['system_summaries'][model_name]
        print(f"done {doc_id}/{len(sd)}", end="\r")
        num_removed_l.append(num_removed)
    print(f"removed average {np.mean(num_removed_l)} summaries for each doc")


def remove_metrics(sd, suffixes_to_remove=['_precision', '_recall']):
    # TODO: Not needed, better to keep all scores
    # ensure common list of all_metrics for each sys summ, and get metrics_list
    metrics_tuple_set = set(
        [tuple(sorted(list(x['scores'].keys()))) for d in sd.values() for x in d['system_summaries'].values()])
    assert len(metrics_tuple_set) == 1, "all system summary score dicts should have the same set of all_metrics"
    metrics_list = list(list(metrics_tuple_set)[0])

    metrics_to_remove = [metric for metric in metrics_list if metric.endswith(tuple(suffixes_to_remove))]

    for doc_id in sd.keys():
        for model_name in sd[doc_id]['system_summaries'].keys():
            for metric in metrics_to_remove:
                del sd[doc_id]['system_summaries'][model_name]['scores'][metric]
        print(f"done {doc_id}/{len(sd)}", end="\r")


def invert_metric(sd, metric_to_invert):
    # TODO: Not needed now since JS-2 is inverted in get_scores
    for doc_id in sd.keys():
        for model_name in sd[doc_id]['system_summaries'].keys():
            try:
                sd[doc_id]['system_summaries'][model_name]['scores'][metric_to_invert] = - \
                    sd[doc_id]['system_summaries'][model_name]['scores'][metric_to_invert]
            except:
                pdb.set_trace()
        print(f"done {doc_id}/{len(sd)}", end="\r")


# add data in scores dict:
# at document level: mean scores, stdev scores
# at system summary level: normed scores, ranks
def add_normed_scores(sd):
    m_list = get_metrics_list(sd)
    for doc_id, isd in sd.items():
        summdicts_d = isd['system_summaries']
        isd['min_scores'] = {}
        isd['max_scores'] = {}
        for m in m_list:
            isd['min_scores'][m] = np.min([d['scores'][m] for d in summdicts_d.values()])
            isd['max_scores'][m] = np.max([d['scores'][m] for d in summdicts_d.values()])
        for model_name, summdict in summdicts_d.items():
            summdict['normed_scores'] = {}
            for m in m_list:
                if isd['max_scores'][m] - isd['min_scores'][m] == 0:
                    isd['max_scores'][m] = 1e-6
                summdict['normed_scores'][m] = \
                    (summdict['scores'][m] - isd['min_scores'][m]) / (isd['max_scores'][m] - isd['min_scores'][m])
                try:
                    assert 0 <= summdict['normed_scores'][m] <= 1
                except:
                    pdb.set_trace()
        print(f"done {doc_id}/{len(sd)}", end="\r")


# retain system summaries for which the score exceeds the lexrank score on at least one metric
def apply_cutoff(sd, cutoff_model='lexrank'):
    # TODO: Not needed since we don't use lexrank cutoff now.
    metrics_tuple_set = set(
        [tuple(sorted(list(x['scores'].keys()))) for d in sd.values() for x in d['system_summaries'].values()])
    assert len(metrics_tuple_set) == 1, "all system summary score dicts should have the same set of all_metrics"
    metrics_list = list(list(metrics_tuple_set)[0])
    num_removed_l = []

    for doc_id in sd.keys():
        num_removed = 0
        models_to_remove = []
        # identify which system summmaries to remove
        for model_name in sd[doc_id]['system_summaries'].keys():
            this_sys_summ_dict = sd[doc_id]['system_summaries'][model_name]
            remove_this = True
            for metric in metrics_list:
                if this_sys_summ_dict['scores'][metric] > sd[doc_id]['system_summaries'][cutoff_model]['scores'][ metric]:
                    remove_this = False
                    break
            if remove_this:
                models_to_remove.append(model_name)
                num_removed += 1
        # remove identified system summaries for this doc
        for model_name in models_to_remove:
            del sd[doc_id]['system_summaries'][model_name]
        print(f"done {doc_id}/{len(sd)}", end="\r")
        num_removed_l.append(num_removed)
        # sanity check assert
        assert not (cutoff_model in sd[doc_id][
            'system_summaries'].keys()), f"cutoff_model {cutoff_model} should have been eliminated as part of apply_cutoff"
    print(f"removed average {np.mean(num_removed_l)} summaries for each doc")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-action", nargs='+',
                        choices=["convert_to_new", "add_normed_scores", "merge", "dedup",
                                 "dedup_old", "remove_metrics", "apply_cutoff", "invert_js2"])
    parser.add_argument("-ip", '--in_path', type=str,
                        help="path of directory containing score dicts to convert/merge",
                        required=True)
    parser.add_argument("-op", '--out_path', type=str,
                        help="path of directory to store converted score dicts OR path "
                             "of file at which to store merged file",
                        required=True)
    args = parser.parse_args()
    assert not os.path.exists(args.out_path)
    assert args.out_path.endswith('.pkl')
    print(args.action)

    new_sds = []
    merged_sd = None
    for action in args.action:
        print(f'action: {action}')
        if action == "convert_to_new":
            assert os.path.isdir(args.in_path)
            for sd_fname in glob.glob(os.path.join(args.in_path, '*')):
                new_sds.append(sd_to_new_format(get_pickle(sd_fname)))

        elif action == "merge":
            if len(new_sds) == 0:
                assert os.path.isdir(args.in_path)
                for sd_fname in glob.glob(os.path.join(args.in_path, '*')):
                    new_sds.append(get_pickle(sd_fname))

            for sd in new_sds:
                if merged_sd is None:
                    merged_sd = copy.deepcopy(sd)
                else:
                    merge_score_dicts(merged_sd, sd)

        else:
            if merged_sd is None:
                merged_sd = get_pickle(args.in_path)

            if action == "dedup":
                remove_duplicates(merged_sd, duplicate_string='### DUPLICATE ###')

            elif action == "dedup_old":
                remove_dup_sys_summs(merged_sd)

            elif action == "remove_metrics":
                remove_metrics(merged_sd)

            elif action == "add_normed_scores":
                add_normed_scores(merged_sd)

            elif action == "apply_cutoff":
                apply_cutoff(merged_sd)

            elif action == "invert_js2":
                invert_metric(sd=merged_sd, metric_to_invert="js-2")

    write_pickle(merged_sd, args.out_path)
