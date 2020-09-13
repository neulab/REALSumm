# REALSumm: Re-evaluating EvALuation in Summarization

## Collected System summaries

| SNo. | Model | Paper | Variant | Type |
| ---- | ----- | ----- | ------- | ---- |
| 1 | HeterGraph | [Want et al., 2020](https://arxiv.org/abs/2004.12393) | default | Extractive |
| 2 | MatchSumm | [Zhong et al., 2020](https://arxiv.org/abs/2004.08795) | default | Extractive |
| 3 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | BERT-LSTM-PN-RL | Extractive |
| 4 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | BERT-LSTM-PN | Extractive |
| 5 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | BERT-LSTM-SL | Extractive |
| 6 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | BERT-TF-PN | Extractive |
| 7 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | BERT-TF-SL | Extractive |
| 8 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | LSTM-PN-RL | Extractive |
| 9 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | LSTM-PN | Extractive |
| 10 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | LSTM-SL | Extractive |
| 11 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | TF-PN | Extractive |
| 12 | PNBERT | [Zhong et al., 2020](https://www.aclweb.org/anthology/P19-1100/) | TF-SL | Extractive |
| 13 | BART | [Lewis et al., 2019](https://arxiv.org/abs/1910.13461) | Ext | Extractive |
| 14 | REFRESH | [Narayan et al., 2018](https://www.aclweb.org/anthology/N18-1158/) | default | Extractive |
| 15 | NeuSumm | [Zhou et al., 2018](https://www.aclweb.org/anthology/P18-1061/) | default | Extractive|
| 16 | BanditSumm | [Dont et al., 2018](https://www.aclweb.org/anthology/D18-1409/) | default | Extractive |
| 17 | SemSim | [Yoon et al., 2020](https://arxiv.org/abs/2002.07767) | default | Abstractive|
| 18 | BART | [Lewis et al., 2019](https://arxiv.org/abs/1910.13461) | Abs | Abstractive |
| 19 | PreSumm | [Liu et al., 2019](https://www.aclweb.org/anthology/D19-1387/) | Abs | Abstractive|
| 20 | PreSumm | [Liu et al., 2019](https://www.aclweb.org/anthology/D19-1387/) | Ext-Abs | Abstractive|
| 21 | PreSumm | [Liu et al., 2019](https://www.aclweb.org/anthology/D19-1387/) | Trans-Abs | Abstractive|
| 22 | TwoStageRL | [Zhang et al., 2019](https://arxiv.org/abs/1902.09243) | default | Abstractive|
| 23 | UniLM | [Dong et al., 2019](https://papers.nips.cc/paper/9464-unified-language-model-pre-training-for-natural-language-understanding-and-generation) | V1 | Abstractive|
| 24 | UniLM | [Dong et al., 2019](https://papers.nips.cc/paper/9464-unified-language-model-pre-training-for-natural-language-understanding-and-generation) | V2 | Abstractive|
| 25 | T5 | [Raffel et al., 2019](https://arxiv.org/abs/1910.10683) | base | Abstractive|
| 26 | T5 | [Raffel et al., 2019](https://arxiv.org/abs/1910.10683) | small | Abstractive|
| 27 | T5 | [Raffel et al., 2019](https://arxiv.org/abs/1910.10683) | large | Abstractive|
| 28 | T5 | [Raffel et al., 2019](https://arxiv.org/abs/1910.10683) | 3B | Abstractive|
| 29 | T5 | [Raffel et al., 2019](https://arxiv.org/abs/1910.10683) | 11B | Abstractive|
| 30 | BottomUp | [Gehrmann et al., 2018](https://www.aclweb.org/anthology/D18-1443/) | default | Abstractive|
| 31 | FastAbsRL | [Chen et al., 2018](https://www.aclweb.org/anthology/P18-1063/) | default | Abstractive|
| 32 | FastAbsRL | [Chen et al., 2018](https://www.aclweb.org/anthology/P18-1063/) | Rerank | Abstractive|
| 33 | PtrGen | [See et al., 2017](https://www.aclweb.org/anthology/P17-1099/) | baseline | Abstractive|
| 34 | PtrGen | [See et al., 2017](https://www.aclweb.org/anthology/P17-1099/) | ptr-gen | Abstractive|
| 35 | PtrGen | [See et al., 2017](https://www.aclweb.org/anthology/P17-1099/) | ptr-gen-cov | Abstractive|

There are total 35 system outputs, 16 extractive and 19 abstractive.

### Preprocessing
For each of the collected system outputs, we first check if the outputs are already tokenized. Most of the outputs that we received were already tokenized. If they were not, we tokenized them using spacy. For all systems, we added a special tag ``<t>`` for beginning of sentence and ``</t>`` for end of sentence. Please see ``process_data/process_*.py`` files for the corresponding pre-processing steps taken. 

For all system outputs, we score them against their provided ``ref.txt`` files i.e. we don't score every output against a common reference file. This is done since some models follow some specific preprocessing rules e.g. the left round brackets ``(`` are replaced by ``-lrb-`` etc. and we did not want to punish a model by scoring it against a reference that is tokenized differently.

- [Raw outputs](Must add link here)
- [Tokenized outputs](Must add link here)

### Alignment
The outputs that we received from different models were not aligned with each other. To analyze them together, it was critical to align them such that we get all the generated summaries of every article. We decided to align all of the generated summaries to the outputs from PtrGen ([See et al., 2017](https://www.aclweb.org/anthology/P17-1099/)). 

For every reference summary provided, say ``ref1``, we search for it's closest match in the reference summaries from PtrGen. To do this, we (1) consider only alpha numeric characters from ``ref1`` and take a random substring from it. If this substring exists in exactly *one* reference summary from PtrGen, we have a match. 

To align any two reference files first run 
```bash
python -m process_data.get_alignment -out <ref file to be aligned> -ref <ref file to align against> -matching_path <output mapping file> -length <length of substring to match> -max_attempts <max attempts to try to align a summary> -n_jobs <parallelize over these many cpus>
``` 
This will create a json file at the specified ``matching_path`` which can be used to permute the contents of any file using 
```bash
python -m process_data.realign -ip <file to realign> -op <output path. -matching_path <output json file created from step 1>
```

Since this is a noisy procedure, on average we find 100 summaries out of 11490 that don't get aligned. We replace them by a special string ``### NO MATCH FOUND ###``.

- [Final aligned outputs used for scoring](Must add link here)

## Scoring system summaries
To score all the outputs, they should be in the following directory structure (already done in the link above). Each file contains one summary per line.
```bash
aligned
|___ ext
|   |___ model_name_1
|   |   |___ out_variant_name_1.txt
|   |   |___ out_variant_name_2.txt
|   |   |___ ref.txt
|   |___ model_name_2
|       |___ out.txt
|       |___ ref.txt
|   .
|   .
|___ abs
    |___ model_name_1
    |   |___ out_variant_name_1.txt
    |   |___ out_variant_name_2.txt
    |   |___ ref.txt
    |___ model_name_2
        |___ out.txt
        |___ ref.txt    
    .
    .
```
Calculating scores of all 11490 summaries for all 35 models and 7 metrics is a time consuming process. We calculate scores separately for ``ext`` and ``abs``, one metric at a time and then merge the results. This allows us to parallely run different metrics. To score the ``ext`` or ``abs`` summaries, run:
```bash
python get_scores.py -dp <path to ext or abs> -m <metric to score> -op <path to store output pickle> -lp <log path> -num_ref <number of references per doc: 1 for cnn_dm, 4 for TAC> -ref_sep || sep || -n_jobs <number of cpus to parallelize over>
```
Supported metrics are ``rouge, js2, bertscore, rwe, moverscore, wms, sms`` where ``rouge`` will calculate R-1, R-2 and R-L. Precision, Recall and F-1 variants of all scores will be stored (if the metrics have these variants).

After scoring the summaries by whichever metrics you want, collect all the output pickle files in a directory and merge them using
```
python add command to merge
```

## Collecting human judgements

### Document Selection
Out of the 11490 documents, we select 100 for which we'll collect human judgments (See Algorithm 1 in [our paper](Add link here) for our selection procedure). Due to budget constraints, we also arbitrarily select 11 extractive and 14 abstractive outputs for each of the 100 documents. These are marked in the table. Please see [this notebook](Add link here) which selects the 100 documents and writes them in the appropriate format for the next step.

### Extracting SCUs
All of our code for creating AMT tasks is based on [LitePyramids](https://github.com/OriShapira/LitePyramids) [[Paper](https://www.aclweb.org/anthology/N19-1072.pdf)]. We create SCUs from the 100 reference summaries ourselves by creating [AMT](https://www.mturk.com/) tasks using the following steps

1. Run ``python pre_create script`` after setting the appropriate global variables to create a csv file.
2. Upload the csv file to AMT and create your own SCUs.
3. Download the results from AMT and run ``python post_script`` to create the csv file containing all the SCUs.

You can download [our created SCUs here](Add link here).

### Gathering annotations
To gather annotations on AMT, use the following steps:
1. Run `` python pre_create script`` to create a csv file for each collected system. 
2. Create a task on AMT and upload one csv file for each task. Please see [annotation_instructions.txt](add link here) for the annotations instructions and [amt_settings.txt](add link here) for the settings used while creating the tasks.
3. Run ``python clean annotators script`` to remove rogue annotators (if any) and get clean annotations.
4. Use ``notebook to get human scores and add to sd`` to calculate the human scores for each summary and add it to our metrics scores dict. This can now be used to analyze metrics!

You can download the [scores dict containing human judgments here](add link here).

## Reevaluating metrics
The [final scores dict](Add link here) contains all automatic metric as well as human judgments. This is used by [analysis_notebook](Add link here) for all the analysis done in the paper.
