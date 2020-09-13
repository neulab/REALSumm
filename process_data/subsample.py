import pdb
import utils
import argparse
import json
from os.path import join as join


def subsample(files, small_indices):
    small_files = [[file[idx] for idx in small_indices] for file in files]
    return small_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-files', nargs='+', required=True, help="files to subsample. they will remain aligned")
    parser.add_argument('-small_indices', required=True, help="path of the indices to pick")
    parser.add_argument('-out_dir', required=True, help="Path to output folder")
    args = parser.parse_args()

    files = [utils.read_file(fname) for fname in args.files]
    for file in files:
        assert len(file) == len(files[0])

    small_indices = json.load(open(args.small_indices))
    small_files = subsample(files, small_indices)
    for file in small_files:
        assert len(file) == len(small_files[0])

    for i, fname in enumerate(args.files):
        new_fname = join(args.out_dir, fname.split('/')[-1])
        with open(new_fname, 'w') as f:
            f.write('\n'.join(small_files[i]) + '\n')
