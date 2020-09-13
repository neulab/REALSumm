"""
deprecated. Use get_alignment + realign
reads all files - source, gold and ouput. Aligns them and stores them in a common format
"""
import os
import re
import random
import pdb
import argparse
import json
from joblib import Parallel, delayed, parallel_backend


def listdir_fullpath(d):
    for f in os.listdir(d):
        yield os.path.join(d, f)


def get_content(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        return f.read().strip()


def get_chunks(ls, sz):
    """
    divides a list ls into chunks of size n
    :param ls: a list
    :param sz size of chunk
    :return: a generator of chunks
    """
    for i in range(0, len(ls), sz):
        yield ls[i: i+sz]


def read_abisee(folder_name):
    """
    Sub-folders: articles, baseline, pointer-gen, pointer-gen-cov, reference
    """

    def read_folder(sub_folder):
        file2txt = {}
        for i, fname in enumerate(listdir_fullpath(sub_folder)):
            txt = get_content(fname)
            file2txt[int(fname.split('/')[-1].split('_')[0])] = txt
            if i % 100 == 0:
                print("read {} files".format(i), end='\r')
        return file2txt

    src_path = os.path.join(folder_name, 'src.txt')
    ref_path = os.path.join(folder_name, 'ref.txt')
    baseline_path = os.path.join(folder_name, 'out_baseline.txt')
    pointer_gen_path = os.path.join(folder_name, 'out_pointer-gen.txt')
    pointer_gen_cov_path = os.path.join(folder_name, 'out_pointer-gen-cov.txt')

    print(f"hopefully {src_path} exists")
    print("reading articles")
    if os.path.exists(src_path):
        src = get_content(src_path).split('\n')
        src = {i: doc for i, doc in enumerate(src)}
    else:
        src = read_folder("{}/test_output/articles".format(folder_name))

    print("reading references")
    if os.path.exists(ref_path):
        ref = get_content(ref_path).split('\n')
        ref = {i: doc for i, doc in enumerate(ref)}
    else:
        ref = read_folder("{}/test_output/reference".format(folder_name))

    print("reading baseline output")
    if os.path.exists(baseline_path):
        baseline = get_content(baseline_path).split('\n')
        baseline = {i: doc for i, doc in enumerate(baseline)}
    else:
        baseline = read_folder("{}/test_output/baseline".format(folder_name))

    print(f"reading pointer-gen output. hopefully {pointer_gen_path} exists")
    if os.path.exists(pointer_gen_path):
        pointer_gen = get_content(pointer_gen_path).split('\n')
        pointer_gen = {i: doc for i, doc in enumerate(pointer_gen)}
    else:
        pointer_gen = read_folder("{}/test_output/pointer-gen".format(folder_name))

    print("reading pointer-gen-cov output")
    if os.path.exists(pointer_gen_cov_path):
        pointer_gen_cov = get_content(pointer_gen_cov_path).split('\n')
        pointer_gen_cov = {i: doc for i, doc in enumerate(pointer_gen_cov)}
    else:
        pointer_gen_cov = read_folder("{}/test_output/pointer-gen-cov".format(folder_name))

    assert (len(src) == len(baseline) == len(pointer_gen) == len(pointer_gen_cov) == len(ref))
    assert (set(src.keys()) == set(ref.keys()) == set(baseline.keys()) == set(

        pointer_gen.keys()) == pointer_gen_cov.keys())
    return src, ref, baseline, pointer_gen, pointer_gen_cov


def read_bottom_up(folder_name):
    src_dict, ref_dict, out_dict = {}, {}, {}
    src = get_content(
        "{}/input_bottom-up-summary-cnndm_shuffled_test/test.txt.src.tagged.shuf.400words".format(folder_name)).split(
        '\n')
    ref = get_content(
        "{}/input_bottom-up-summary-cnndm_shuffled_test/test.txt.tgt.tagged.shuf.noslash".format(folder_name)).split(
        '\n')
    out = get_content("{}/output_bottom_up_cnndm_015_threshold.out".format(folder_name)).split('\n')
    assert (len(src) == len(ref) == len(out))
    for i in range(len(src)):
        src_dict[i] = src[i]
        ref_dict[i] = ref[i]
        out_dict[i] = out[i]

    print("bottom up size: {}".format(len(src)))
    return (src_dict, ref_dict, out_dict)


def read_fast_abs(folder_name):
    pass


def read_processed_file(src_path: str = None, ref_path: str = None, out_path: str = None) -> tuple:
    """
    Reads processed files with one doc per line.
    :param src_path: source docs in each line
    :param ref_path: target summaries in each line
    :param out_path: output summaries in each line
    :return: dicts for each src, ref and out key is line number, value is string
    """
    src_dict, ref_dict, out_dict = None, None, None
    if src_path:
        src = get_content(src_path).split('\n')
        src_dict = {i: doc for i, doc in enumerate(src)}
        print("num source docs read: {}".format(len(src)))
    if ref_path:
        ref = get_content(ref_path).split('\n')
        ref_dict = {i: doc for i, doc in enumerate(ref)}
        print("num ref docs read: {}".format(len(ref)))
    if out_path:
        out = get_content(out_path).split('\n')
        out_dict = {i: doc for i, doc in enumerate(out)}
        print("num out docs read: {}".format(len(out)))

    return src_dict, ref_dict, out_dict


def read_msft_unilm(folder_name):
    pass


def read_yang_presum(folder_name):
    abs_json = get_content(folder_name + "/CNNDM_BertSumAbs.jsonl").split('\n')
    ext_abs_json = get_content(folder_name + "/CNNDM_BertSumExtAbs.jsonl").split('\n')
    trans_abs_json = get_content(folder_name + "/CNNDM_TransformerAbs.jsonl").split('\n')
    abs_json = [json.loads(line) for line in abs_json]
    ext_abs_json = [json.loads(line) for line in ext_abs_json]
    trans_abs_json = [json.loads(line) for line in trans_abs_json]

    src_yp = {i: doc['article'] for i, doc in enumerate(abs_json)}
    ref_yp = {i: doc['reference'] for i, doc in enumerate(abs_json)}
    out_abs = {i: doc['decoded'] for i, doc in enumerate(abs_json)}
    src_ext_abs = {i: doc['article'] for i, doc in enumerate(ext_abs_json)}
    out_ext_abs = {i: doc['decoded'] for i, doc in enumerate(ext_abs_json)}
    src_trans_abs = {i: doc['article'] for i, doc in enumerate(trans_abs_json)}
    out_trans_abs = {i: doc['decoded'] for i, doc in enumerate(trans_abs_json)}
    assert (len(src_yp) == len(ref_yp) == len(out_abs) == len(out_ext_abs) == len(out_trans_abs))
    return src_yp, ref_yp, out_abs, (src_ext_abs, out_ext_abs), (src_trans_abs, out_trans_abs)


def find_matching(src_as, doc_chunk, match_exactly=False, ignore_sent_tags=False):
    """
    Matching algorithm: find a matching span amongst alpha numeric characters only.
    If found in only one - success. Keep trying till found.
    :param src_as: dict of id: article
    :param doc: a document to match
    :return: idx of matching doc in src_as
    """
    matching = []
    for tup in doc_chunk:
        # find only alpha-numeric characters in both
        doc_idx, doc = tup
        doc = re.sub(r'\W+', '', doc.lower())
        if ignore_sent_tags:
            doc = re.sub('<t>', '', doc)
            doc = re.sub('<\\t>', '', doc)
            doc = re.sub('<q>', '', doc)
        match_found = 0
        attempts = 0
        match_idx = -1
        while match_found != 1:
            match_found = 0
            match_idx = -1
            if not match_exactly:
                st = random.randint(0, len(doc) - args.length)
            attempts += 1
            for idx_as, doc_as in src_as.items():
                # find only alpha-numeric characters in both
                if not match_exactly:
                    matched = doc[st: st + args.length] in doc_as
                else:
                    matched = (doc == doc_as)
                if matched:
                    match_found += 1
                    match_idx = idx_as
                    if match_found > 1:
                        break
            if attempts > args.attempts:
                match_idx = -1
                print("could not match doc {}".format(doc_idx))
                break
        matching.append((doc_idx, match_idx))
    return matching


def write_to_disk(docs, outfile, mapping=None, default_str="### NO MATCH FOUND ###"):
    if outfile is None:
        print("outfile is None. Ignoring call to write to disk.")
        return
    new_docs = {}
    if mapping:
        for idx, doc in docs.items():
            if mapping[idx] == -1:
                # can't align some document
                continue
            else:
                new_docs[mapping[idx]] = doc
    else:
        new_docs = docs
    with open(outfile, 'w') as f:
        for i in range(len(docs)):
            if i in new_docs:
                str_to_write = new_docs[i].replace('\n', '')
            else:
                str_to_write = default_str
            f.write(str_to_write + '\n')


def match(src_as, src_other, match_exactly=False, ignore_sent_tags=False):
    """
    Assumes input is abigail see's src articles
    :param src_as: dict of id: article
    :param src_other: dict of id:article to realign with src_as
    :return: mapping from old idx to new
    """

    idx_other2idx_as = {}
    src_as_modified = {idx: re.sub(r'\W+', '', doc.lower()) for idx, doc in src_as.items()}
    chunk_sz = len(src_other) // args.n_jobs
    chunks = list(get_chunks(list(sorted(src_other.items(), key=lambda x: x[0])), chunk_sz))
    with parallel_backend('multiprocessing', n_jobs=args.n_jobs):
        matchings = Parallel()(
            delayed(find_matching)(src_as_modified, doc_chunk, match_exactly, ignore_sent_tags)
            for doc_chunk in chunks
        )
    matchings = [el for ls in matchings for el in ls]
    assert (len(matchings) == len(src_other))
    for match in matchings:
        doc_idx, match_idx = match
        idx_other2idx_as[doc_idx] = match_idx
    assert (len(idx_other2idx_as) == len(src_other))
    return idx_other2idx_as


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-data_path", type=str, default="../data/all_outputs",
                        help="folder containing model output folder")
    parser.add_argument("-n_jobs", type=int, required=True, help="number of cpus")
    parser.add_argument("-length", type=int, default=50, help="substring length to match")
    parser.add_argument("-attempts", type=int, default=50, help="number of attempts to try")
    parser.add_argument("-dataset", required=True, help="supported: abisee / bottom_up / yang_presum / processed_file")
    parser.add_argument("-out_input_path", default=None,
                        help="file path from which to read out.txt file to be realigned. "
                             "Only needed for -dataset = processed_file")
    parser.add_argument("-ref_input_path", default=None, help="target docs of summaries to align. "
                                                              "Only needed for -dataset = processed_file")
    parser.add_argument("-src_input_path", default=None, help="source docs of summaries to align, "
                                                              "Only needed for -dataset = processed_file")
    parser.add_argument("-align_docs", default=None, help="src/ref which docs to align with abisee. "
                                                          "Only needed for -dataset = processed_file")
    parser.add_argument("-match_exactly", action='store_true', help="match docs exactly to realign")
    args = parser.parse_args()

    # sanity check args.data_path
    assert os.path.isdir(args.data_path), f"should have valid directory for -data_path. received dir {args.data_path}"

    GOLDEN_ALIGNMENT = os.path.join(args.data_path, 'abisee_ptr_generator')
    assert os.path.isdir(GOLDEN_ALIGNMENT), f"should have valid GOLDEN_ALIGNMENT directory. received {GOLDEN_ALIGNMENT}"

    print("reading abisee")
    src_as, ref_as, baseline_as, pointer_gen, pointer_gen_cov = read_abisee(GOLDEN_ALIGNMENT)

    if args.dataset == 'abisee':
        write_to_disk(src_as, os.path.join(args.data_path, 'abisee_ptr_generator/src.txt'))
        write_to_disk(ref_as, os.path.join(args.data_path, 'abisee_ptr_generator/ref.txt'))
        write_to_disk(baseline_as, os.path.join(args.data_path, 'abisee_ptr_generator/out_baseline.txt'))
        write_to_disk(pointer_gen, os.path.join(args.data_path, 'abisee_ptr_generator/out_pointer_gen.txt'))
        write_to_disk(pointer_gen_cov, os.path.join(args.data_path, 'abisee_ptr_generator/out_pointer_gen_cov.txt'))

    # 'processed_file' means that the file already has one line per doc, and thus is already in the right format
    # thus it is a 'processed' file. It only needs re-ordering of lines for alignment.
    elif args.dataset == 'processed_file':
        if args.src_input_path:
            src_input_path = args.src_input_path
            assert os.path.exists(src_input_path) and os.path.isfile(src_input_path), f"expected a file {src_input_path}"
            src_output_path = src_input_path + ".aligned"
        if args.ref_input_path:
            ref_input_path = args.ref_input_path
            assert os.path.exists(ref_input_path) and os.path.isfile(ref_input_path), f"expected a file {ref_input_path}"
            ref_output_path = ref_input_path + ".aligned"
        if args.out_input_path:
            out_input_path = args.out_input_path
            assert os.path.exists(out_input_path) and os.path.isfile(out_input_path), "file_name should be an existing file"
            out_output_path = out_input_path + ".aligned"

        src_pf, ref_pf, out_pf = read_processed_file(src_input_path, ref_input_path, out_input_path)
        if args.align_docs == 'src':
            mapping = match(src_as, src_pf, match_exactly=args.match_exactly, ignore_sent_tags=True)
        elif args.align_docs == 'ref':
            mapping = match(ref_as, ref_pf, match_exactly=args.match_exactly, ignore_sent_tags=True)
        else:
            raise NotImplementedError("args.align = {} not supported".format(args.align))
        print(f"finished mapping with {sum([1 for key in mapping if mapping[key] == -1])} docs unmatched "
              f"(out of {len(mapping)}). "
              f"Now writing to file...")

        write_to_disk(src_pf, src_output_path, mapping)
        write_to_disk(ref_pf, ref_output_path, mapping)
        write_to_disk(out_pf, out_output_path, mapping)
        
        # TO run
        # python realign_all.py -n_jobs 1 -dataset processed_file -src_input_path ../data/cnn_dm/full_data/test.source \
        # -ref_input_path ../data/cnn_dm/full_data/test.target -out_input_path ../data/cnn_dm/full_data/test.hypo \
        # -align_docs src -data_path ../data/cnn_dm/abisee_out_downloaded_processed/ -length 20 -attempts 100

    elif args.dataset == 'bottom_up':
        print("starting bottom up")
        src_bu, ref_bu, out_bu = read_bottom_up(os.path.join(args.data_path, 'bottom-up-summary-cnndm_shuffled_test'))
        mapping = match(src_as, src_bu)
        print("finished bottom up")
        write_to_disk(src_bu, os.path.join(args.data_path, 'bottom-up-summary-cnndm_shuffled_test/src.txt'), mapping)
        write_to_disk(ref_bu, os.path.join(args.data_path, 'bottom-up-summary-cnndm_shuffled_test/ref.txt'), mapping)
        write_to_disk(out_bu, os.path.join(args.data_path, 'bottom-up-summary-cnndm_shuffled_test/out.txt'), mapping)

    elif args.dataset == 'yang_presum':
        print("starting yang presum")
        src_yp, ref_yp, out_abs, (src_ext_abs, out_ext_abs), (src_trans_abs, out_trans_abs) = \
            read_yang_presum("../data/all_outputs/yang_presumm_outputs")
        mapping = match(src_as, src_yp)
        write_to_disk(src_yp, os.path.join(args.data_path, 'yang_presumm_outputs/src.txt'), mapping)
        write_to_disk(ref_yp, os.path.join(args.data_path, 'yang_presumm_outputs/ref.txt'), mapping)
        write_to_disk(out_abs, os.path.join(args.data_path, 'yang_presumm_outputs/out_abs.txt'), mapping)
        mapping = match(src_as, src_ext_abs)
        write_to_disk(out_ext_abs, os.path.join(args.data_path, 'yang_presumm_outputs/out_ext_abs.txt'), mapping)
        mapping = match(src_as, src_trans_abs)
        write_to_disk(out_trans_abs, os.path.join(args.data_path, 'yang_presumm_outputs/out_trans_abs.txt'), mapping)

    else:
        raise NotImplementedError("dataset {} not supported yet".format(args.dataset))

    print("finished alignment")
