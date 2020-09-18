import rouge


def get_rouge(system_text, reference_text,
              rouge_type,  # rouge type to return
              metric_to_get, # rouge type to evaluate
              max_n,
              limit_length=False,
              length_limit=1024,
              stemming=False,  # not sure what is the standard practise here
              length_limit_type='words',  # can be words or bytes
              prf='f'  # To use precision/recall/f1
              ):

    if isinstance(system_text, list):
        system_text = " ".join(system_text)
    # create pyrouge evaluator (python implementation of rouge)
    evaluator = rouge.Rouge(metrics=[metric_to_get],
                            max_n=max_n,
                            limit_length=limit_length,
                            length_limit=length_limit,
                            length_limit_type=length_limit_type,  # can be words or bytes
                            apply_avg=False,
                            apply_best=False,
                            alpha=0.5,  # Default F1_score
                            weight_factor=1.2,
                            # Weight factor to be used for ROUGE-W. Official rouge score defines it at 1.2. Default: 1.0
                            stemming=stemming)

    # evaluator output looks like
    # {'rouge-2': [{'f': [1.0], 'p': [1.0], 'r': [1.0]}], 'rouge-1': [{'f': [1.0], 'p': [1.0], 'r': [1.0]}]}
    # we want scores_dict[metric] to be a dict, not a list (of length 1) of dict
    scores_dict = evaluator.get_scores(system_text, reference_text)
    cleaned_scores_dict = {}
    for metric, metric_vals_dict_list in scores_dict.items():
        assert (len(metric_vals_dict_list) == 1)
        cleaned_scores_dict[metric] = metric_vals_dict_list[0]
    return cleaned_scores_dict[rouge_type][prf][0]
    # return cleaned_scores_dict
