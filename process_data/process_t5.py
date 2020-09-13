import argparse
import json
import utils


def process_t5():
    srcf = open(args.out_src, 'w')
    reff = open(args.out_ref, 'w')
    decf = open(args.out_dec, 'w')

    sent_tokenizer = utils.get_sent_tokenizer(tokenizer='spacy')
    for i, line in enumerate(open(args.infile, 'r')):
        doc = json.loads(line.strip())

        src = utils.sent_list_to_tagged_str(utils.sent_tokenize(doc['article'], sent_tokenizer))
        ref = utils.sent_list_to_tagged_str(utils.sent_tokenize(doc['reference'], sent_tokenizer))
        dec = utils.sent_list_to_tagged_str(utils.sent_tokenize(doc['decoded'], sent_tokenizer))

        srcf.write(src + '\n')
        reff.write(ref + '\n')
        decf.write(dec + '\n')
        print(f"processed line {i}", end='\r')

    srcf.close()
    reff.close()
    decf.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-infile", required=True, help="input jsonl file")
    parser.add_argument("-out_src", required=True, help="out text file")
    parser.add_argument("-out_ref", required=True, help="out text file")
    parser.add_argument("-out_dec", required=True, help="out text file")
    args = parser.parse_args()

    process_t5()


# export dp=/projects/tir5/users/mbhandar/capstone/data/cnn_dm_collected_system_outputs; export type=cnndm_11B; python process_t5.py  -infile $dp/raw/abs/t5/$type.jsonl -out_src $dp/processed/abs/t5/$type.src.txt -out_ref $dp/processed/abs/t5/$type.ref.txt -out_dec $dp/processed/abs/t5/$type.dec.txt
