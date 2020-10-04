# REALSumm: Re-evaluating EvALuation in Summarization


<img src="fig/eval.gif" width="700">



## Collected System summaries

| Paper | # variants | Type | All Outputs | Scored outputs |
| ----- | ---------- | ---- | ------- | -------------- |
[Heterogeneous Graph Neural Networks for Extractive Document Summarization](https://arxiv.org/abs/2004.12393) | 1 | Extractive | link | link | 
[Extractive Summarization as Text Matching](https://arxiv.org/abs/2004.08795) | 1 | Extractive | link | link |
[Searching for Effective Neural Extractive Summarization: What Works and What’s Next](https://www.aclweb.org/anthology/P19-1100/) | 5 | Extractive | link | link |
[BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461) | 1 | Extractive | link | link |
[Ranking Sentences for Extractive Summarization with Reinforcement Learning](https://www.aclweb.org/anthology/N18-1158/) | 1 | Extractive | link | link |
[Neural Document Summarization by Jointly Learning to Score and Select Sentences](https://www.aclweb.org/anthology/P18-1061/) | 1 | Extractive| link | link |
[BanditSum: Extractive Summarization as a Contextual Bandit](https://www.aclweb.org/anthology/D18-1409/) | 1 | Extractive | link | link |
[Learning by Semantic Similarity Makes Abstractive Summarization Better](https://arxiv.org/abs/2002.07767) | 1 | Abstractive| link | link |
[BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461) | 1 | Abstractive | link | link |
[Text Summarization with Pretrained Encoders](https://www.aclweb.org/anthology/D19-1387/) | 3 | Abstractive| link | link |
[Pretraining-Based Natural Language Generation for Text Summarization](https://arxiv.org/abs/1902.09243) | 1 | Abstractive| link | link |
[Unified Language Model Pre-training for Natural Language Understanding and Generation](https://papers.nips.cc/paper/9464-unified-language-model-pre-training-for-natural-language-understanding-and-generation) | 2 | Abstractive| link | link |
[Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683) | 3 | Abstractive| link | link |
[Bottom-Up Abstractive Summarization](https://www.aclweb.org/anthology/D18-1443/) | 1 | Abstractive| link | link |
[Fast Abstractive Summarization with Reinforce-Selected Sentence Rewriting](https://www.aclweb.org/anthology/P18-1063/) | 1 | Abstractive| link | link |
[Get To The Point: Summarization with Pointer-Generator Networks](https://www.aclweb.org/anthology/P17-1099/) | 1 | Abstractive| link | link |

There are total 25 system outputs, 11 extractive and 14 abstractive.
- [Full aligned outputs used for scoring](https://drive.google.com/file/d/1z9WGs-mC7JO8U5PgEYE_SrekST7nC64x/view?usp=sharing)
- [Full aligned ouputs used for human evaluation](https://drive.google.com/file/d/1z9WGs-mC7JO8U5PgEYE_SrekST7nC64x/view?usp=sharing)

Please read our [reproducibility instructions](https://github.com/neulab/REALSumm/blob/master/reproducibility.md) in addition to
our paper (TODO: add link) in order to reproduce this work for another dataset.





<table>
    <thead>
        <tr>
            <th>Layer 1</th>
            <th>Layer 2</th>
            <th>Layer 3</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=4>L1 Name</td>
            <td rowspan=2>L2 Name A</td>
            <td>L3 Name A</td>
        </tr>
        <tr>
            <td>L3 Name B</td>
        </tr>
        <tr>
            <td rowspan=2>L2 Name B</td>
            <td>L3 Name C</td>
        </tr>
        <tr>
            <td>L3 Name D</td>
        </tr>
    </tbody>
</table>



# Meta-evaluate a new metric on CNN/DM
## I can score all the given summaries 
1. Just give a scores dict in the below format. Make sure to include ``litepyramid_recall``, which is the metric used by human evaluators, in the scores dict.
2. Run [the analysis notebook](https://github.com/neulab/REALSumm/blob/master/analysis/analysis.ipynb) on the scores dict to get all the graphs and tables used in the paper.

## Help me score the given summaries
1. Update ``scorer.py`` such that (1) if there is any setup required by your metric, make sure to do it in the ``__init__`` function of scorere as the scorere will be used to score all systems. And (2) add your metric in the ``score`` function as
```python
elif self.metric == "name_of_my_new_metric":
  scores = call_to_my_function_which_gives_scores(passing_appropriate_arguments)
```

where ``scores`` is a list of scores corresponding to each summary in a file. It should be a list of dictionaries e.g. ``[{'precision': 0.0, 'recall': 1.0} ...]``


2. Calculate the scores and the scores dict using ``python get_scores.py --data_path ../selected_docs_for_human_eval/<abs or ext> --output_path ../score_dicts/abs_new_metric.pkl --log_path ../logs/scores.log -n_jobs 1 --metric <name of metric> ``
3. Your scores dict is generated at the output path.
4. Merge it with the scores dict with human scores provided in ``scores_dicts/`` using ``python score_dict_update.py --in_path <score dicts folder with the dicts to merge> --out_path <output path to place the merged dict pickle> -action merge``
5. Your dict will be merged with the one with human scores and the output will be placed in ``out_path``. You can now run the analysis notebook on the scores dict to get all the graphs and tables

## Scores dict format used



    {
        doc_id: {
                'doc_id': value of doc id,
                'ref_summ': reference summary of this doc,
                'system_summaries': {
                    system_name: {
                            'system_summary': the generated summary,
                            'scores': {
                                'js-2': the actual score,
                                'rouge_l_f_score': the actual score,
                                'rouge_1_f_score': the actual score,
                                'rouge_2_f_score': the actual score,
                                'bert_f_score': the actual score
                            }
                    }
                }
            }
    }
    


