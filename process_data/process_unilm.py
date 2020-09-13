import utils
import argparse
from os.path import join as join


def tokenize(line):
    sents = line.split(args.sep)
    sents = [sent.strip() for sent in sents]
    # unilm has subword splitting with ##
    sents = [sent.replace(' ##', '') for sent in sents]
    return utils.sent_list_to_tagged_str(sents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ref", required=True, help="path to ref file")
    parser.add_argument("-out", nargs='+', required=True, help="path to out file")
    parser.add_argument("-out_dir", required=True, help="path to output dir: processed/bart")
    parser.add_argument("-sep", default=" [X_SEP] ", help="sentence separator. <q> for presumm")
    args = parser.parse_args()

    ref = utils.read_file(args.ref)
    outs = [utils.read_file(out) for out in args.out]

    for out in outs:
        assert len(out) == len(ref)

    ref = [tokenize(line) for line in ref]
    outs = [[tokenize(line) for line in out] for out in outs]

    for out in outs:
        assert len(out) == len(ref)

    with open(join(args.out_dir, "ref.txt"), 'w') as f:
        f.write('\n'.join(ref) + '\n')

    for i, out in enumerate(outs):
        with open(join(args.out_dir, f"out_{i}.txt"), 'w') as f:
            f.write('\n'.join(out) + '\n')
