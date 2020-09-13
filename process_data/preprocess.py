import argparse
import json
import pdb
from utils import read_file, tokenize_file, retain_first_n_sent
import os
from tqdm import tqdm
# from ..utils import tokenize_file
from .realign_all import get_content
sen_start = " <t> "
sen_end = " </t> "


def process_arxiv(fname):
    pass


def process_pubmed(fname):
    docs = read_file(fname, each_line='json', print_patience=1000)

### process abisee's ptr gen cnn-dm output
### in_dir:  contains files for each doc
### out_file: one file, one line per doc
def process_ptrgen(in_dir, out_file):
    with open(out_file, 'w') as out_fp:
        for fname in tqdm(sorted(os.listdir(in_dir))):
            s = ""
            with open(os.path.join(in_dir, fname), 'r') as in_fp:
                for line in in_fp:
                    s = s + (sen_start + line.strip() + sen_end)
                s = s + "\n"
            out_fp.write(s)

# takes the yang presumm output format( jsonl) and converts into src, ref files
def get_dataset_from_jsonl(file_name, out_dir):
    json_list = get_content(file_name).split('\n')
    # pdb.set_trace()
    dict_list = [json.loads(line) for line in json_list]

    src = [d['article'] for d in dict_list]
    ref = [d['reference'] for d in dict_list]
    # out = {i: d['decoded'] for i, d in enumerate(dict_list)}

    src_save_path = os.path.join(out_dir, 'src.txt')
    ref_save_path = os.path.join(out_dir, 'ref.txt')

    with open(src_save_path, 'w') as fp:
        for line in src:
            fp.write(line+"\n")
    with open(ref_save_path, 'w') as fp:
        for line in ref:
            fp.write(line+"\n")
    print(f"saved data from {file_name} to {src_save_path} and {ref_save_path}")

def process_files_in_dir(in_dir, out_dir, dataset_type):
    if dataset_type=="ptr-gen":
        for dir in os.listdir(in_dir):
            dir_path = os.path.join(in_dir, dir)
            if not os.path.isdir(dir_path):
                continue
            print(f"processing {dir_path}")
            out_file = os.path.join(out_dir, dir)
            process_ptrgen(in_dir=dir_path, out_file=out_file)


def process_files_q_to_t(in_dir, out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    for in_file in os.listdir(in_dir):
        in_file_path = os.path.join(in_dir, in_file)
        if not os.path.isfile(in_file_path):
            continue
        out_file_path = os.path.join(out_dir, in_file)
        with open(in_file_path, 'r') as in_fp, open(out_file_path, 'w') as out_fp:
            for in_line in in_fp:
                out_line = sen_start + in_line.strip().replace("<q>", (sen_end + sen_start)) + sen_end + "\n"
                out_fp.write(out_line)

def remove_dups(in_dir, out_dir):
    for in_file in os.listdir(in_dir):
        in_file_path = os.path.join(in_dir, in_file)
        out_file_path = os.path.join(out_dir, in_file)
        with open(in_file_path, 'r') as ifp, open(out_file_path, 'w') as ofp:
            in_lines = [line.strip() for line in ifp.read().split('\n')]
            lines_set = set(in_lines)
            print(f"doc {in_file_path}: had lines :{len(in_lines)} , after removing dups: {len(lines_set)}")
            out_lines = "\n".join(list(lines_set))
            ofp.write(out_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_path", type=str, help="file or dir to process")
    parser.add_argument("--dataset", type=str, help="supported options: arxiv/pubmed")
    parser. add_argument("--out_path", type=str, help="output file or dir")
    args = parser.parse_args()

    if args.dataset == 'arxiv':
        process_arxiv(args.fname)
    elif args.dataset == 'pubmed':
        process_pubmed(args.fname)
    elif args.dataset == 'out-ptr-gen':
        process_files_in_dir(args.in_path, args.out_path, args.dataset)
    elif args.dataset == 'q_to_t': # change sentence separator from <q> to </t> <t>
        process_files_q_to_t(args.in_path, args.out_path)
    elif args.dataset == 'sentence_tokenize':
        assert os.path.isfile(args.in_path), "in_path and out_path should be files"
        tokenize_file(args.in_path, args.out_path, remove_existing_tags=False)
    elif args.dataset == 'first_sent':
        assert os.path.isfile(args.in_path), "in_path and out_path should be files"
        retain_first_n_sent(args.in_path, args.out_path, 1)
    elif args.dataset == 'sentence_tokenize_ret':
        assert os.path.isfile(args.in_path), "in_path and out_path should be files"
        tokenize_file(args.in_path, args.out_path, remove_existing_tags=True)
    elif args.dataset == 'extract_jsonl':
        assert os.path.isfile(args.in_path)
        assert os.path.isdir(args.out_path)
        get_dataset_from_jsonl(args.in_path, args.out_path)
    elif args.dataset == 'remove_dups':
        assert os.path.isdir(args.in_path)
        assert os.path.isdir(args.out_path)
        remove_dups(args.in_path, args.out_path)
    else:
        raise NotImplementedError("dataset {} not supported".format(args.dataset))