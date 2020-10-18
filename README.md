# REALSumm: Re-evaluating EvALuation in Summarization

#### Author: [Manik Bhandari](https://manikbhandari.github.io/), [Pranav Gour](https://scholar.google.com/citations?user=OKM72KwAAAAJ&hl=en), [Atabak Ashfaq](https://www.linkedin.com/in/atabakashfaq), [Pengfei Liu](http://pfliu.com/), [Graham Neubig](http://www.phontron.com/)

## Outline
* ### [Leaderboard](https://github.com/neulab/Leaderboard)
* ### [Motivation](https://github.com/neulab/REALSumm#Motivation)
* ### [Released Data](https://github.com/neulab/REALSumm#Released-Data)
* ### [Meta-evaluation Tool](https://github.com/neulab/REALSumm#Meta-evaluation-Tool)
* ### [Bib](https://github.com/neulab/REALSumm#Bib)



## Leaderboard
A Leaderboard for Automatic Metrics (Released in two weeks)


## Motivation
Evaluating summarization is hard. Most papers still use ROUGE, but recently a host of metrics (eg BERTScore, MoverScore) report better correlation with human eval. However, these were tested on older systems (the classic TAC meta-evaluation datasets are now 6-12 years old), how do they fare with SOTA models? Will conclusions found there hold with modern systems and summarization tasks>


<img src="fig/eval.gif" width="700">



## Released Data

Including all the system variants, there are total 25 system outputs - 11 extractive and 14 abstractive.
- [All outputs](https://drive.google.com/file/d/1z9WGs-mC7JO8U5PgEYE_SrekST7nC64x/view?usp=sharing)
- [All ouputs used for human evaluation](https://github.com/neulab/REALSumm/tree/master/selected_docs_for_human_eval)
- [All outputs with human scores](https://github.com/neulab/REALSumm/tree/master/scores_dicts)

Please read our [reproducibility instructions](https://github.com/neulab/REALSumm/blob/master/reproducibility.md) in addition to
our [paper](https://arxiv.org/pdf/2010.07100.pdf) in order to reproduce this work for another dataset.


<table>
<thead>
  <tr>
    <th>Type</th>
    <th>Sys ID</th>
    <th>System Output</th>
    <th>Human Judgement</th>
    <th>Paper</th>
    <th>Variants</th>
    <th>Bib</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="11">Extractive</td>
    <td>1</td>
    <td><a href="https://drive.google.com/drive/folders/1a5qZvCZeqVkmrE_SqpxaOR5dOKYJ-sFy?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1dQf2cTb8KlieQdisIv9x5Xl78AL3rmGJ?usp=sharing">Download</a></td>
    <td colspan=2><a href="https://www.aclweb.org/anthology/2020.acl-main.553.pdf">Heterogeneous Graph Neural Networks for Extractive Document Summarization</a></td>
    <td><a href="https://www.aclweb.org/anthology/2020.acl-main.553.bib">Bib</a></td>
  </tr>
  <tr>
    <td>2</td>
    <td><a href="https://drive.google.com/drive/folders/1ZnYaboV3rbOw-TN6wNy3dG8seFa7INvy?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1sUXx5nHrdc1oxKNPEzRUCVI63pYBaluf?usp=sharing">Download</a></td>
    <td colspan=2><a href="https://arxiv.org/pdf/2004.08795.pdf">Extractive Summarization as Text Matching</a></td>
    <td><a href="https://www.aclweb.org/anthology/2020.acl-main.552.bib">Bib</a></td>
  </tr>
  <tr>
    <td>3</td>
    <td><a href="https://drive.google.com/drive/folders/117wJh4T3tSaeRr1It3O1LR9y0iGXWEEL?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1qyJFkp-86Ve-KjMpFlYKYH1bT3x6twvD/view?usp=sharing">Download</a></td>
    <td rowspan="5"><a href="https://www.aclweb.org/anthology/P19-1100.pdf">Searching for Effective Neural Extractive Summarization: What Works and What’s Next</a></td>
    <td>LSTM+PN+RL</td>
    <td rowspan="5"><a href="https://www.aclweb.org/anthology/P19-1100.bib">Bib</a></td>
  </tr>
  <tr>
    <td>4</td>
    <td><a href="https://drive.google.com/drive/folders/17z7V-qpc1oJ9nGWJa_ebvod2AeeWdH74?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1fqWFPfeHkgIOIw775Lq4OeJIGU7odV0z/view?usp=sharing">Download</a></td>
    <td>BERT+TF+SL</td>
  </tr>
  <tr>
    <td>5</td>
    <td><a href="https://drive.google.com/drive/folders/1Eiv0CoWxpmDxb-30nmgXxFEVdvG6Un1i?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1j3gTJIcM2cyQ2WlVsjoWLlFw9WiXy1fu/view?usp=sharing">Download</a></td>
    <td>BERT+TF+PN</td>
  </tr>
  <tr>
    <td>6</td>
    <td><a href="https://drive.google.com/drive/folders/1xKa2aJpKmOrYJ4KaR7m3aVV7QSyvu-Y2?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/11iDk9QKrPjnWA7U9q0g0OT-6wfexakZL/view?usp=sharing">Download</a></td>
    <td>BERT+LSTM+PN</td>
  </tr>
  <tr>
    <td>7</td>
    <td><a href="https://drive.google.com/drive/folders/1XEOclYKjaV3ekgUki52-qmOrNAqpf0fy?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1cCF4egR8VhvYaAayXXIt3s1SxaGK1lGZ/view?usp=sharing">Download</a></td>
    <td>BERT+LSTM+PN+RL</td>
  </tr>
  <tr>
    <td>8</td>
    <td><a href="https://drive.google.com/drive/folders/1kOnSZ6dkJy3fT4UybhTbuTRP2_9bT13O?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/19KVizzuL7pEv-xPvz5LPKsaHaUot21h0?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://www.aclweb.org/anthology/2020.acl-main.703.pdf">BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension</a></td>
    <td><a href="https://www.aclweb.org/anthology/2020.acl-main.703.bib">Bib</a></td>
  </tr>
  <tr>
    <td>9</td>
    <td><a href="https://drive.google.com/drive/folders/1Rq5TA3ycssLj1kr-U3cNyeTvQoXK5m5_?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/11XvUzbZKa3BV_bt0cBGzsYugRxpmNIew?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://www.aclweb.org/anthology/N18-1158.pdf">Ranking Sentences for Extractive Summarization with Reinforcement Learning</a></td>
    <td><a href="https://www.aclweb.org/anthology/N18-1158.bib">Bib</a></td>
  </tr>
  <tr>
    <td>10</td>
    <td><a href="https://drive.google.com/drive/folders/1k1R21BbpO-K8L-NLRhDqFTWcVe6fabWL?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/16Vux_5Nnpg3_VUUeMmBJA0o4XL5E6SRZ?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://www.aclweb.org/anthology/P18-1061.pdf">Neural Document Summarization by Jointly Learning to Score and Select Sentences</a></td>
    <td><a href="https://www.aclweb.org/anthology/P18-1061.bib">Bib</a></td>
  </tr>
  <tr>
    <td>11</td>
    <td><a href="https://drive.google.com/drive/folders/1Z3ywNNW0so5hUx6SJJQHhipwReYZA1vR?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/140CLeUdNPOwdLM_82n3iHHNbR5bg6H-c?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://www.aclweb.org/anthology/D18-1409.pdf">BanditSum: Extractive Summarization as a Contextual Bandit</a></td>
    <td><a href="https://www.aclweb.org/anthology/D18-1409.bib">Bib</a></td>
  </tr>
  <tr>
    <td rowspan="14">Abstractive</td>
    <td>12</td>
    <td><a href="https://drive.google.com/drive/folders/1Di9TOiy1547a4-buRHIxYqgaMn13DEJo?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1jKnqQbJhYJGVwnLZ9sccT7oSUtpKS4La?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://arxiv.org/pdf/2002.07767.pdf">Learning by Semantic Similarity Makes Abstractive Summarization Better</a></td>
    <td><a href="https://arxiv.org/pdf/2002.07767.pdf">Bib</a></td>
  </tr>
  <tr>
    <td>13</td>
    <td><a href="https://drive.google.com/drive/folders/1M5NQH2gudleynUVRLwQ4mqxzyoxIiO8L?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1bKasCvsZE8w0r1qObKZylDahuOsqpBAh?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://www.aclweb.org/anthology/2020.acl-main.703.pdf">BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension</a></td>
    <td><a href="https://www.aclweb.org/anthology/2020.acl-main.703.bib">Bib</a></td>
  </tr>
  <tr>
    <td>14</td>
    <td><a href="https://drive.google.com/drive/folders/1eIhgKZ04Y1_cp8vONeA9frqi3DF4t1wE?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/14-r55JSgGbT_Ug-SAKALd5H1Sct3IYZ-/view?usp=sharing">Download</a></td>
    <td rowspan="3"><a href="https://www.aclweb.org/anthology/D19-1387.pdf">Text Summarization with Pretrained Encoders</a></td>
    <td>TransAbs</td>
    <td rowspan="3"><a href="https://www.aclweb.org/anthology/D19-1387.bib">Bib</a></td>
  </tr>
  <tr>
    <td>15</td>
    <td><a href="https://drive.google.com/drive/folders/1BAROSNDELNg3zc5qIpE-zJNpk_8r1c0u?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1cWyvyAelJUlX43ibjgSLb13oR9OwUBGY/view?usp=sharing">Download</a></td>
    <td>Abs</td>
  </tr>
  <tr>
    <td>16</td>
    <td><a href="https://drive.google.com/drive/folders/11YnG-a1oxbe1mP_ugvGZxeBgeeBoYrix?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1PrOCVjLWlBQglfIQPAgTMreUs0XhJFmJ/view?usp=sharing">Download</a></td>
    <td>ExtAbs</td>
  </tr>
  <tr>
    <td>17</td>
    <td><a href="https://drive.google.com/drive/folders/1AbxvzXkEjqSVpyMrXbhBsw1sGkFiSan7?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1D8IgFwgi2bGkNFZvbi23TWPhKrprJSjC?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://www.aclweb.org/anthology/K19-1074.pdf">Pretraining-Based Natural Language Generation for Text Summarization</a></td>
    <td><a href="https://www.aclweb.org/anthology/K19-1074.bib">Bib</a></td>
  </tr>
  <tr>
    <td>18</td>
    <td><a href="https://drive.google.com/drive/folders/1zM2IjBpOCBXDLXgVyhYOcGVlNqt90_a3?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1V1W6pluV7Pio_wcjcdtY0GlYDw_VIQzO/view?usp=sharing">Download</a></td>
    <td rowspan="2"><a href="http://papers.nips.cc/paper/9464-unified-language-model-pre-training-for-natural-language-understanding-and-generation.pdf">Unified Language Model Pre-training for Natural Language Understanding and Generation</a></td>
    <td>v1</td>
    <td rowspan="2"><a href="https://scholar.googleusercontent.com/scholar.bib?q=info:u_6By4rPxSAJ:scholar.google.com/&output=citation&scisdr=CgXIMYmZEPmS1n5esr0:AAGBfm0AAAAAX4Jbqr3HHbaP5Zr4wDxP9priYAOQD3i8&scisig=AAGBfm0AAAAAX4Jbqs8g6PXoClyx85xETMb9e7Vwd6B0&scisf=4&ct=citation&cd=-1&hl=en">Bib</a></td>
  </tr>
  <tr>
    <td>19</td>
    <td><a href="https://drive.google.com/drive/folders/1TVFtBHHAhqNIirtH23aEwYDmXknD2bJf?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1OZvULR7PPy37rOYYMShezSM0XbHiwd5a/view?usp=sharing">Download</a></td>
    <td>v2</td>
  </tr>
  <tr>
    <td>20</td>
    <td><a href="https://drive.google.com/drive/folders/12mr2vrNwokpLQ5hJUMGNAdEF2AxW88zO?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1YerGcmYg4FMRjac4361Xf9SSBsG-Ym_0/view?usp=sharing">Download</a></td>
    <td rowspan="3"><a href="https://arxiv.org/pdf/1910.10683.pdf">Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer</a></td>
    <td>Base</td>
    <td rowspan="3"><a href="https://scholar.googleusercontent.com/scholar.bib?q=info:esM38LPDnF0J:scholar.google.com/&output=citation&scisdr=CgXIMYmZEPmS1n5ZDek:AAGBfm0AAAAAX4JcFekfvqjXomIfKDT2-XVfZsQeOt5h&scisig=AAGBfm0AAAAAX4JcFTBxzquHyZT9z__dw7D6Pg_EDePu&scisf=4&ct=citation&cd=-1&hl=en">Bib</a></td>
  </tr>
  <tr>
    <td>21</td>
    <td><a href="https://drive.google.com/drive/folders/1Faim0BHtY6XIgm9Iyh8ujutMDE_yE3Bd?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1N5vkS7v5_JeV6ZN65RUQCADU2kSQk2kp/view?usp=sharing">Download</a></td>
    <td>Large</td>
  </tr>
  <tr>
    <td>22</td>
    <td><a href="https://drive.google.com/drive/folders/1gEDWw2XkeNOBrakO6946MQSNFcG6OHZH?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/file/d/1l6PwbZGeeT-MrLoWyvo-pggQQ-GGtk92/view?usp=sharing">Download</a></td>
    <td>11B</td>
  </tr>
  <tr>
    <td>23</td>
    <td><a href="https://drive.google.com/drive/folders/1BeK0AgkkWK5PdTZv56kOUabrvPBFkKLX?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1feYAEwb972W9tY65eaNNJ4jp8Tzte0LG?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://www.aclweb.org/anthology/D18-1443.pdf">Bottom-Up Abstractive Summarization</a></td>
    <td><a href="https://www.aclweb.org/anthology/D18-1443.bib">Bib</a></td>
  </tr>
  <tr>
    <td>24</td>
    <td><a href="https://drive.google.com/drive/folders/1IFV2dD-1B0eOWo_wukz4wW_E0OukjL02?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1Y6mZimKo_dO44VPKrjHEyg84QI92QDH4?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://arxiv.org/pdf/1805.11080.pdf">Fast Abstractive Summarization with Reinforce-Selected Sentence Rewriting</a></td>
    <td><a href="https://www.aclweb.org/anthology/P18-1063.bib">Bib</a></td>
  </tr>
  <tr>
    <td>25</td>
    <td><a href="https://drive.google.com/drive/folders/1b3wplLG1kQ1UZj8A2TBzrdCbSc76L13P?usp=sharing">Download</a></td>
    <td><a href="https://drive.google.com/drive/folders/1aGjOhaQ5O4JRaJlRaF4VIocJ5Am1UiG8?usp=sharing">Download</a></td>
    <td colspan="2"><a href="https://arxiv.org/pdf/1704.04368.pdf">Get To The Point Summarization with Pointer-Generator Networks</a></td>
    <td><a href="https://www.aclweb.org/anthology/P17-1099.bib">Bib</a></td>
  </tr>
</tbody>
</table>



## Meta-evaluation Tool

1. Calculate the metric scores for each of the summary and create a scores dict in the below format. See the section below to calculate scores with a new metric.
Make sure to include ``litepyramid_recall`` in the scores dict, which is the metric used by human evaluators.
2. Run [the analysis notebook](https://github.com/neulab/REALSumm/blob/master/analysis/analysis.ipynb) on the scores dict to get all the graphs and tables used in the paper.

### Calculating scores with a new metric
1. Update ``scorer.py`` such that (1) if there is any setup required by your metric, it is done in the ``__init__`` function of scorer as the scorer will be used to score all systems. And (2) add your metric in the ``score`` function as
```python
elif self.metric == "name_of_my_new_metric":
  scores = call_to_my_function_which_gives_scores(passing_appropriate_arguments)
```

where ``scores`` is a list of scores corresponding to each summary in a file. It should be a list of dictionaries e.g. ``[{'precision': 0.0, 'recall': 1.0} ...]``


2. Calculate the scores and the scores dict using ``python get_scores.py --data_path ../selected_docs_for_human_eval/<abs or ext> --output_path ../score_dicts/abs_new_metric.pkl --log_path ../logs/scores.log -n_jobs 1 --metric <name of metric> ``
3. Your scores dict is generated at the output path.
4. Merge it with the scores dict with human scores provided in ``scores_dicts/`` using ``python score_dict_update.py --in_path <score dicts folder with the dicts to merge> --out_path <output path to place the merged dict pickle> -action merge``
5. Your dict will be merged with the one with human scores and the output will be placed in ``out_path``. You can now run the analysis notebook on the scores dict to get all the graphs and tables used in the paper.

### Scores dict format used



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
    
## Bib
```
@inproceedings{Bhandari-2020-reevaluating,
title = "Re-evaluating Evaluation in Text Summarization",
author = "Bhandari, Manik  and Narayan Gour, Pranav  and Ashfaq, Atabak  and  Liu, Pengfei and Neubig, Graham ",
booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
year = "2020"
}

```


