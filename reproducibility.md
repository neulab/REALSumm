### Preprocessing
For each of the collected system outputs, we first check if the outputs are already tokenized. Most of the outputs that we received were already tokenized. If they were not, we tokenized them using spacy. For all systems, we added a special tag ``<t>`` for beginning of sentence and ``</t>`` for end of sentence. Please see ``process_data/process_*.py`` files for the corresponding pre-processing steps taken. 

For all system outputs, we score them against their provided ``ref.txt`` files i.e. we don't score every output against a common reference file. This is done since some models follow some specific preprocessing rules e.g. the left round brackets ``(`` are replaced by ``-lrb-`` etc. and we did not want to punish a model by scoring it against a reference that is tokenized differently.

- [Tokenized outputs](https://drive.google.com/file/d/1V-GFsLeXtIB_XjFqF9XtaDQ78Bg3HKmx/view?usp=sharing)

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

- [Final aligned outputs used for scoring](https://drive.google.com/file/d/1z9WGs-mC7JO8U5PgEYE_SrekST7nC64x/view?usp=sharing)

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
python get_scores.py -dp <path to ext or abs> -m <metric to score> -op <path to store output pickle> -lp <log path> -n_jobs <number of cpus to parallelize over>
```
Supported metrics are ``rouge, js2, bertscore, rwe, moverscore`` where ``rouge`` will calculate R-1, R-2 and R-L. Precision, Recall and F-1 variants of all scores will be stored (if the metrics have these variants).

After scoring the summaries by whichever metrics you want, collect all the output pickle files in a directory and merge them using
```
python -m score_dict_update.py --in_path <directory with all scored dicts> --out_path <output scores dict path> -action merge dedup
```

## Collecting human judgements

### Document Selection
Out of the 11490 documents, we select 100 for which we'll collect human judgments (See Algorithm 1 in [our paper](Add link here) for our selection procedure). Due to budget constraints, we also arbitrarily select 11 extractive and 14 abstractive outputs for each of the 100 documents. These are marked in the table. Please see [this notebook](Add link here) which selects the 100 documents and writes them in the appropriate format for the next step.

### Extracting SCUs
We create SCUs from the 100 reference summaries ourselves by creating [AMT](https://www.mturk.com/) tasks as done in LitePyramids. All of our code for creating AMT tasks is based on [LitePyramids](https://github.com/OriShapira/LitePyramids) [[Paper](https://www.aclweb.org/anthology/N19-1072.pdf)].

You can download [our created SCUs here](Add link here).

### Gathering annotations
To gather annotations we create tasks on AMT using these [annotation_instructions.txt](https://github.com/neulab/REALSumm/blob/master/human_annotations/annotation_instructions.txt) and [amt_settings.txt](https://github.com/neulab/REALSumm/blob/master/human_annotations/amt_settings.txt). Finally we use the post processing scripts provided by LitePyramids to collect human judgments.

## Reevaluating metrics
The [final scores dicts](https://github.com/neulab/REALSumm/tree/master/scores_dicts) contain all automatic metric as well as human judgments. These are used by [analysis_notebook](https://github.com/neulab/REALSumm/blob/master/analysis/analysis.ipynb) for all the analysis done in the paper.
