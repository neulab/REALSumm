import utils
import argparse
import re
import random
import json
from joblib import Parallel, parallel_backend, delayed


def write_to_disk(docs, outfile, matching=None, default_str="### NO MATCH FOUND ###"):
    if outfile is None:
        print("outfile is None. Ignoring call to write to disk.")
        return
    new_docs = {}
    if matching:
        for idx, doc in docs.items():
            if matching[idx] == -1:
                # can't align some document
                continue
            else:
                new_docs[matching[idx]] = doc
    else:
        new_docs = docs
    with open(outfile, 'w') as f:
        for i in range(len(docs)):
            if i in new_docs:
                str_to_write = new_docs[i].replace('\n', '')
            else:
                str_to_write = default_str
            f.write(str_to_write + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", required=True, help="file to realign")
    parser.add_argument("-op", required=True, help="Output here")
    parser.add_argument("-matching_path", required=True, help="matching dict will be picked from here")
    args = parser.parse_args()

    lines = utils.read_file(args.ip)
    lines = {idx: line for idx, line in enumerate(lines)}
    matching = json.load(open(args.matching_path))
    matching = {int(key): value for key, value in matching.items()}
    write_to_disk(lines, args.op, matching=matching)

