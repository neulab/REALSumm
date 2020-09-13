import pdb
import argparse
import os
import json
from utils import read_file, get_sent_tokenizer, get_word_tokenizer, get_chunks
from joblib import Parallel, delayed, parallel_backend


def write_to_presumm_format(chunk_idx, src_chunk, ref_chunk, split, presumm_out, output_name):
    assert len(src_chunk) == len(ref_chunk), \
        "src_chunk size {} but ref_chunk_size {}".format(len(src_chunk), len(ref_chunk))
    sent_tokenizer = get_sent_tokenizer(tokenizer='spacy')
    word_tokenizer = get_word_tokenizer(tokenizer='spacy')
    out = []
    for src, ref in zip(src_chunk, ref_chunk):
        out_src, out_ref = [], []
        src_tokenized = sent_tokenizer(src)
        ref_tokenized = sent_tokenizer(ref)

        src = [doc.text for doc in src_tokenized.sents]
        ref = [doc.text for doc in ref_tokenized.sents]

        for text in src:
            text_tokenized = word_tokenizer(text)
            tokens = [token.text for token in text_tokenized]
            out_src.append(tokens)

        for text in ref:
            text_tokenized = word_tokenizer(text)
            tokens = [token.text for token in text_tokenized]
            out_ref.append(tokens)

        out.append({
            'src': out_src,
            'tgt': out_ref
        })
    print("finished chunk {}".format(chunk_idx), " of size ", len(out))
    with open(os.path.join(presumm_out, output_name + ".{}.{}.json".format(split, chunk_idx)), 'w') as f:
        json.dump(out, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-src_fname", required=True, help="Src file to be processed. Each line is a doc.")
    parser.add_argument("-ref_fname", required=True, help="Ref file to be processed. Each line is a doc.")
    parser.add_argument("-presumm_out", required=True, help="Output folder to save files in")
    parser.add_argument("-output_name", default="cnndm_ext", help="Name of the json files that will be created.")
    parser.add_argument("-num_splits", type=int, required=True,
                        help="Number of splits to form of the input data. "
                             "Also equivalent to number of cpus to parallelize over")
    parser.add_argument("-split", required=True, choices=['train', 'valid', 'test'], help="train/valid/test data?")
    args = parser.parse_args()

    assert os.path.exists(args.src_fname), "file {} not found".format(args.src_fname)
    assert os.path.exists(args.ref_fname), "file {} not found".format(args.ref_fname)

    src_lines = read_file(args.src_fname)
    ref_lines = read_file(args.ref_fname)
    assert len(src_lines) == len(ref_lines), \
        "src has {} lines but ref has {} lines".format(len(src_lines), len(ref_lines))

    src_lines_chunked = get_chunks(src_lines, args.num_splits)
    ref_lines_chunked = get_chunks(ref_lines, args.num_splits)

    with parallel_backend('multiprocessing', n_jobs=args.num_splits):
        Parallel()(
                delayed(write_to_presumm_format)(chunk_idx, src_chunk, ref_chunk, args.split, args.presumm_out, args.output_name)
                for chunk_idx, (src_chunk, ref_chunk) in enumerate(zip(src_lines_chunked, ref_lines_chunked))
            )

"""
 # To run
    
    export BASE_DATA_PATH=/projects/tir5/users/aashfaq/Capstone/data/genetic/combined
    export DATA_DIR=$BASE_DATA_PATH/bertsum_data_train/
    mkdir $DATA_DIR
    python -m write_to_presumm_format -src_fname $BASE_DATA_PATH/train.ext -ref_fname $BASE_DATA_PATH/train.target -presumm_out $DATA_DIR -num_splits 20 -split train
    export DATA_DIR=$BASE_DATA_PATH/bertsum_data_test/
    mkdir $DATA_DIR
    python -m write_to_presumm_format -src_fname $BASE_DATA_PATH/val.ext -ref_fname $BASE_DATA_PATH/val.target -presumm_out $DATA_DIR -num_splits 1 -split valid
    python -m write_to_presumm_format -src_fname $BASE_DATA_PATH/test.ext -ref_fname $BASE_DATA_PATH/test.target -presumm_out $DATA_DIR -num_splits 1 -split test
"""

"""
export JSON_PATH=$BASE_DATA_PATH/bertsum_data_train/

export BASE_DATA_PATH=/projects/tir5/users/aashfaq/Capstone/data/genetic/opt_r1_r2_r_nobudget
export JSON_PATH=$BASE_DATA_PATH/bertsum_data_train/
export BERT_DATA_PATH=$BASE_DATA_PATH/bertsum_data_traint_pt/
mkdir $JSON_PATH
mkdir $BERT_DATA_PATH
python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 1 -log_file ./preprocess.log

export JSON_PATH=$BASE_DATA_PATH/bertsum_data_test/
export BERT_DATA_PATH=$BASE_DATA_PATH/bertsum_data_test_pt/
mkdir $BERT_DATA_PATH
python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 1 -log_file ./preprocess.log

"""

"""
Running to make pt files:
export BASE_DATA_PATH=/projects/tir5/users/aashfaq/Capstone/data/genetic/opt_r1_r
export JSON_PATH=$BASE_DATA_PATH/bertsum_data/
export BERT_DATA_PATH=$BASE_DATA_PATH/bertsum_pt_all_test/
export BERT_DATA_PATH_2=$BASE_DATA_PATH/bertsum_pt2/
mkdir $BERT_DATA_PATH_2
export JSON_PATH_TEST=$BASE_DATA_PATH/bertsum_data_test/
export BERT_DATA_PATH_TEST=$BASE_DATA_PATH/bertsum_pt_test/
mkdir $JSON_PATH_TEST
mkdir $BERT_DATA_PATH_TEST
# in bertsum folder
# python preprocess.py -mode format_to_lines -raw_path $JSON_PATH -save_path $BERT_DATA_PATH -n_cpus 1 -use_bert_basic_tokenizer false -map_path MAP_PATH
python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 1 -log_file ./preprocess.log

"""

"""

cat train.ext >> ../combined/train_comb.ext
cat test.ext >> ../combined/test.ext
cat val.ext >> ../combined/val.ext

cat train.target >> ../combined/train.target
cat val.target >> ../combined/val.target
cat test.target >> ../combined/test.target
"""