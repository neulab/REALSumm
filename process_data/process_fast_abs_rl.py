"""
Also use this to process two-stage-rl
"""
import pdb
import utils
import argparse
from os.path import join as join


def remove_empty(ls):
    """
    Each empty line denotes the start of a new input
    :param ls: a list of strings
    :return: a list of string with no new line in each string
    """
    cand = []
    out = []
    for i, line in enumerate(ls):
        print(f"removing empty line {i}", end='\r')
        if len(line.strip()) == 0:
            if len(cand) > 0:
                out.append(utils.sent_list_to_tagged_str(cand))
                cand = []
            continue
        else:
            cand.append(line)
    if len(cand) > 0:
        out.append(utils.sent_list_to_tagged_str(cand))
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ref", required=True, help="path to ref file")
    parser.add_argument("-out", required=True, nargs='+', help="path to out file(s)")
    parser.add_argument("-out_dir", required=True, help="path to output dir: processed/bart")
    args = parser.parse_args()

    ref = utils.read_file(args.ref)
    outs = [utils.read_file(out) for out in args.out]

    ref = remove_empty(ref)
    outs = [remove_empty(out) for out in outs]
    for out in outs:
        assert len(out) == len(ref)

    with open(join(args.out_dir, "ref.txt"), 'w') as f:
        f.write('\n'.join(ref) + '\n')

    for i, out in enumerate(outs):
        with open(join(args.out_dir, f"out_{i}.txt"), 'w') as f:
            f.write('\n'.join(out) + '\n')
