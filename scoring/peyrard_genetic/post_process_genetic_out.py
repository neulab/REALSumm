import pdb
import os
import argparse
from joblib import Parallel, delayed, parallel_backend
from utils import listdir_fullpath, read_file, get_sents_from_tags


def read_out_file(idx, fname, expected_length=None):
    # doc format is out_doc_{number}_{metric}_{score}
    doc_num = int(fname.split('/')[-1].split('_')[2])
    with open(fname) as f:
        lines = [line.strip() for line in f]
        if expected_length:
            assert (len(lines) == expected_length)
        print("finished reading file {}".format(idx))
        return doc_num, lines


def remove_duplicates(idx, generations):
    """
    Deduplicates the generations but messes up the order.
    :param generations: list of text sent separated by <t> and </t>
    :return: list of text separated by <t> and </t>
    """
    unique_gens = set()
    for i, gen in enumerate(generations):
        gen_sents = get_sents_from_tags(gen, sent_start_tag='<t>', sent_end_tag='</t>')
        gen_sents = tuple(sorted(gen_sents))
        if gen_sents in unique_gens:
            generations[i] = "### DUPLICATE ###"
        unique_gens.add(tuple(gen_sents))

    return generations


def write_to_files(all_summaries, output_fnames):
    """
    writes generated, deduplicated outputs and coresponding references.
    :param all_summaries:
    :param output_fnames:
    :param ref_fnames:
    :return:
    """
    open_files = [open(fname, 'w') for fname in output_fnames]
    for i, summary in enumerate(all_summaries):
        for f, summ in zip(open_files, summary):
            f.write(summ + "\n")
        print("finished writing file {}".format(i), end='\r')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n_jobs", type=int, required=True)
    parser.add_argument("-num_summaries", type=int, required=True)
    parser.add_argument("-in_dir", type=str, required=True)
    parser.add_argument("-out_dir", type=str, required=True)
    args = parser.parse_args()

    assert os.path.isdir(args.in_dir)
    assert os.path.isdir(args.out_dir)

    # Read summary files in parallel
    input_fnames = listdir_fullpath(args.in_dir)
    with parallel_backend('multiprocessing', n_jobs=args.n_jobs):
        all_summaries = Parallel()(
            delayed(read_out_file)(idx, fname)
            for idx, fname in enumerate(input_fnames)
        )
    # sort summaries according to document number
    all_summaries = sorted(all_summaries, key=lambda x: x[0])
    all_summaries = [tup[1] for tup in all_summaries]
    with parallel_backend('multiprocessing', n_jobs=args.n_jobs):
        unique_summaries = Parallel()(
            delayed(remove_duplicates)(idx, summaries)
            for idx, summaries in enumerate(all_summaries)
        )

    output_fnames = [args.out_dir + "/out_{}.txt".format(i) for i in range(args.num_summaries)]
    write_to_files(unique_summaries, output_fnames)

