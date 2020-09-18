import argparse

from peyrard_genetic.JS import js_divergence, compute_tf
from peyrard_s3.S3 import ROUGE as pd_rouge
from peyrard_s3.S3 import word_embeddings as we
from gehrmann_rouge_opennmt.rouge_baselines.baseline import baseline_main

from utils import read_file, get_sents_from_tags
from utils import logger

bert_model = None
tokenizer = None


class Scorer:
    def __init__(self, src_path, ref_path, metric, ref_sep, fast_moverscore=False, num_ref=1):
        self.src_path = src_path
        self.ref_path = ref_path
        self.metric = metric
        self.ref_sep = ref_sep
        self.num_ref = num_ref

        self.ref_lines_with_tags = read_file(ref_path)
        self.ref_lines = [
            ' '.join(get_sents_from_tags(ref.replace(self.ref_sep, ''), sent_start_tag='<t>', sent_end_tag='</t>'))
            for ref in self.ref_lines_with_tags]

        for i, ref in enumerate(self.ref_lines):
            if len(ref) == 0:
                self.ref_lines[i] = '### DUPLICATE ###'

        self.idf_refs = None
        self.idf_hyps = None
        if metric == 'moverscore':
            from all_metrics.moverscore import get_idf_dict
            with open('all_metrics/stopwords.txt', 'r', encoding='utf-8') as f:
                self.stop_words = set(f.read().strip().split(' '))
            if fast_moverscore:
                assert src_path is not None, f"src_path must be provided for fast moverscore"
                src_lines_with_tags = read_file(src_path)
                src_lines = [' '.join(get_sents_from_tags(src, sent_start_tag='<t>', sent_end_tag='</t>'))
                             for src in src_lines_with_tags]
                self.idf_refs = get_idf_dict(self.ref_lines)
                self.idf_hyps = get_idf_dict(src_lines)

        if metric == 'bertscore':
            from bert_score import BERTScorer
            self.bert_scorer = BERTScorer(lang='en', rescale_with_baseline=True)

        if metric == 'js2':
            ref_sents = [get_sents_from_tags(ref_line.replace(ref_sep, ''), sent_start_tag='<t>',
                                             sent_end_tag='</t>')
                         for ref_line in self.ref_lines_with_tags]

            self.ref_freq = [compute_tf(rs, N=2) for rs in ref_sents]

        if metric == 'rwe':
            self.embs = we.load_embeddings('../data/peyrard_s3/deps.words')

    def score(self, file_num, summ_path, model_name, variant_name):
        """
        :return: a list with format: [{score: value}] with scores for each doc in each dict
        """
        logger.info(f"getting scores for model: {model_name}, variant: {variant_name}, file num: {file_num}")
        summ_lines_with_tags = read_file(summ_path)
        summ_lines = [' '.join(get_sents_from_tags(summ, sent_start_tag='<t>', sent_end_tag='</t>'))
                      for summ in summ_lines_with_tags]
        for i, summ in enumerate(summ_lines):
            if len(summ) == 0:
                summ_lines[i] = '### DUPLICATE ###'

        if self.metric == 'moverscore':
            from all_metrics.moverscore import word_mover_score, get_idf_dict
            idf_refs = get_idf_dict(self.ref_lines) if self.idf_refs is None else self.idf_refs
            idf_hyps = get_idf_dict(summ_lines) if self.idf_hyps is None else self.idf_hyps
            scores = word_mover_score(self.ref_lines, summ_lines, idf_refs, idf_hyps, self.stop_words,
                                      n_gram=1, remove_subwords=True, batch_size=64, device='cuda:0')
            scores = [{'mover_score': s} for s in scores]

        elif self.metric == 'bertscore':
            (P, R, F) = self.bert_scorer.score(summ_lines, self.ref_lines)
            P, R, F = list(F.numpy()), list(P.numpy()), list(R.numpy())
            scores = [{'bert_precision_score': p, 'bert_recall_score': r, 'bert_f_score': f_score}
                      for p, r, f_score in zip(P, R, F)]

        elif self.metric == 'js2':
            summ_sents = [get_sents_from_tags(summ_line, sent_start_tag='<t>', sent_end_tag='</t>')
                          for summ_line in summ_lines_with_tags]
            # import pdb; pdb.set_trace()
            scores = [{'js-2': -js_divergence(summ_sent, ref_freq, N=2)}
                      for summ_sent, ref_freq in zip(summ_sents, self.ref_freq)]

        elif self.metric == 'rouge':
            args = argparse.Namespace(check_repeats=True, delete=True, get_each_score=True, stemming=True,
                                      method='sent_tag_verbatim', n_bootstrap=1000, run_google_rouge=False,
                                      run_rouge=True, source=summ_path, target=self.ref_path,
                                      ref_sep=self.ref_sep, num_ref=self.num_ref, temp_dir='../data/temp/')

            scores = baseline_main(args, return_pyrouge_scores=True)['individual_score_results']
            scores = [scores[doc_id] for doc_id in range(len(self.ref_lines))]

        elif self.metric == 'rwe':
            scores = [{'rouge_1_we': pd_rouge.rouge_n_we(ref, [summ], self.embs, n=1, alpha=0.5)}
                      for ref, summ in zip(self.ref_lines, summ_lines)]

        elif self.metric == 'sms' or self.metric == 'wms':
            from all_metrics.sentence_mover.smd import smd
            scores = smd(self.ref_lines, summ_lines, word_rep='glove', metric=self.metric)
            scores = [{self.metric: s} for s in scores]

        else:
            raise NotImplementedError(f"metric {self.metric} not supported")

        assert len(scores) == len(self.ref_lines)
        sd = {}
        for doc_id in range(len(self.ref_lines)):
            sd[doc_id] = {
                'doc_id': doc_id,
                'ref_summ': self.ref_lines_with_tags[doc_id],
                'system_summaries': {
                    f'{model_name}_{variant_name}': {
                        'system_summary': summ_lines_with_tags[doc_id],
                        'scores': scores[doc_id]
                    }
                }
            }
        return sd
