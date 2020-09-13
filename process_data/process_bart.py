"""
Also use this to process bart/semsim/ptr_gen
"""
import utils
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ref", required=True, help="path to ref file")
    parser.add_argument("-out", nargs='+', required=True, help="path to out file")
    parser.add_argument("-out_dir", required=True, help="path to output dir: processed/bart")
    args = parser.parse_args()

    utils.tokenize_file(args.ref, os.path.join(args.out_dir, "ref.txt"))
    for i, file in enumerate(args.out):
        utils.tokenize_file(file, os.path.join(args.out_dir, f"out_{i}.txt"))
