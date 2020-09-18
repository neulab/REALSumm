from __future__ import print_function, division

import numpy as np
from pycocoevalcap.eval import COCOEvalCap
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider

class Evaluator(object):

    def evaluate(self, reference, hypothesis):

        def bleu_scorer(reference, hypothesis):
            # =================================================
            # Compute scores
            # =================================================
            scorer = Bleu(4)
            method = ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]
            # print('computing %s score...' % (scorer.method()))

            score, scores = scorer.compute_score(reference, hypothesis)

            bleus = {}
            if type(method) == list:
                for sc, scs, m in zip(score, scores, method):
                    # print("%s: %0.3f" % (m, sc))
                    bleus[m] = sc
            else:
                # print("%s: %0.3f" % (method, score))
                bleus[method] = score

            return bleus

        def rouge_scorer(reference, hypothesis):
            # =================================================
            # Compute scores
            # =================================================
            scorer = Rouge()

            average_score, score = scorer.compute_score(reference, hypothesis)

            return average_score, score

        ## get BLEU scores
        # bleu_stats = bleu.get_bleu(preds,grounds)
        # blue_from_nltk = bleu.bleu_nltk(preds,grounds)
        # bleu_from_moses = bleu.get_bleu_moses(preds, grounds)
        roube_l, rouge_l_all = rouge_scorer(reference, hypothesis)
        # eval_from_cocoeval = bleu_scorer(grounds,preds)

        return roube_l, rouge_l_all