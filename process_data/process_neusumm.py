import utils
import argparse
from os.path import join as join


def tokenize(line):
    sents = line.split("##SENT##")
    sents = [sent.strip() for sent in sents]
    return utils.sent_list_to_tagged_str(sents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ref", required=True, help="path to ref file")
    parser.add_argument("-out", required=True, help="path to out file")
    parser.add_argument("-out_dir", required=True, help="path to output dir: processed/bart")
    args = parser.parse_args()

    ref = utils.read_file(args.ref)
    out = utils.read_file(args.out)
    out = [line.split('\t')[1].strip() for line in out]
    assert len(ref) == len(out)

    ref = [tokenize(line) for line in ref]
    sent_tokenizer = utils.get_sent_tokenizer(tokenizer='spacy')
    out = [utils.sent_list_to_tagged_str(utils.sent_tokenize(line, sent_tokenizer))
           for line in out]
    assert len(out) == len(ref)

    with open(join(args.out_dir, "ref.txt"), 'w') as f:
        f.write('\n'.join(ref) + '\n')

    with open(join(args.out_dir, "out.txt"), 'w') as f:
        f.write('\n'.join(out) + '\n')
