import argparse
import json
from utils import read_file
import os
from tqdm import tqdm
# from ..utils import tokenize_file
from .realign_all import get_content
sen_start = " <t> "
sen_end = " </t> "

from all_metrics.get_rouge_pyrouge import get_rouge


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
    parser.add_argument("--in1", type=str, help="file to process")
    parser.add_argument("--in2", type=str, help="file to process")
    parser.add_argument("--out1", type=str, help="file to process")
    parser.add_argument("--out2", type=str, help="file to process")
    parser.add_argument("--thresh", type=float, help="r-2 threshold")
    args = parser.parse_args()

    lines_kept = 0
    lines_read = 0

    with open(args.in1, "r") as if1, open(args.in2, "r") as if2, \
        open(args.out1, "w") as of1, open(args.out2, "w") as of2:
        for s1, s2 in zip(if1, if2):
            if lines_read%1000==0:
                print(f"kept {lines_kept} / {lines_read}", end="\r")
            lines_read += 1
            s1 = s1.strip()
            s2 = s2.strip()
            if len(s1)==0 or len(s2)==0:
                continue
            score = get_rouge(s1, s2, rouge_type="rouge-2", max_n=2, metric_to_get="rouge-n")
            if score > args.thresh:
                of1.write(s1+"\n")
                of2.write(s2+"\n")
                lines_kept += 1
