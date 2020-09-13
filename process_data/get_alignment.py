import utils
import argparse
import re
import random
import json
from joblib import Parallel, parallel_backend, delayed


def find_matching(src_as, idx, doc, length, max_attempts):
    """
    Matching algorithm: find a matching span amongst alpha numeric characters only.
    If found in only one - success. Keep trying till found.
    :param src_as: dict of id: article
    :param doc: a document to match
    :return: idx of matching doc in src_as
    """
    # find only alpha-numeric characters in both
    doc = re.sub(r'\W+', '', doc.lower())
    match_found = 0
    attempts = 0
    match_idx = -1
    while match_found != 1:
        match_found = 0
        match_idx = -1
        st = random.randint(0, len(doc))
        to_match = doc[st: st + args.length]
        attempts += 1
        for idx_as, doc_as in src_as.items():
            # find only alpha-numeric characters in both
            matched = to_match in doc_as
            if matched:
                match_found += 1
                match_idx = idx_as
                if match_found > 1:
                    break
        if attempts > max_attempts:
            match_idx = -1
            print("could not match doc {}".format(idx))
            break

    return idx, match_idx


def match(src_as, src_other, length, max_attempts, n_jobs=16):
    """
    Assumes input is abigail see's src articles
    :param src_as: dict of id: article
    :param src_other: dict of id:article to realign with src_as
    :return: mapping from old idx to new
    """

    src_as_modified = {idx: re.sub(r'\W+', '', doc.lower()) for idx, doc in src_as.items()}

    with parallel_backend('multiprocessing', n_jobs=n_jobs):
        matchings = Parallel()(
            delayed(find_matching)(src_as_modified, idx, doc, length, max_attempts)
            for idx, doc in src_other.items()
        )
    matchings = {idx: match_idx for idx, match_idx in matchings}
    assert (len(matchings) == len(src_other))
    return matchings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ref", required=True, help="Reference file")
    parser.add_argument("-out", required=True, help="This file will be aligned with reference")
    parser.add_argument("-matching_path", required=True, help="matching dict will be stored here")
    parser.add_argument("-length", type=int, default=30, help="match a string of this length")
    parser.add_argument("-max_attempts", type=int, default=10, help="try to match these many times")
    parser.add_argument("-n_jobs", type=int, default=16, help="parallelize over")
    args = parser.parse_args()

    ref = utils.read_file(args.ref)
    out = utils.read_file(args.out)
    # Assumes files are tokenized
    ref = [' '.join(utils.get_sents_from_tags(line, sent_start_tag='<t>', sent_end_tag='</t>')) for line in ref]
    out = [' '.join(utils.get_sents_from_tags(line, sent_start_tag='<t>', sent_end_tag='</t>')) for line in out]

    ref = {idx: line for idx, line in enumerate(ref)}
    out = {idx: line for idx, line in enumerate(out)}
    matchings = match(ref, out, length=args.length, max_attempts=args.max_attempts, n_jobs=args.n_jobs)

    json.dump(matchings, open(args.matching_path, 'w'))
