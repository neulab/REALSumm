"""
Loads TAC data provided by Peyrard and outputs a directory tac_system_summaries containing
src.txt, ref.txt and out_[num].txt.
Additionally, we also store the mapping id: doc_id
"""
import argparse
import json
import logging
import os
import utils
from utils import logger, init_logger


def load_tac_json_files():
    sd = {}
    for fname in args.tac_files:
        sd.update(json.load(open(fname)))
    logger.info(f"loaded {len(sd)} TAC documents")
    return sd


def get_num_sys_outs(sd):
    """
    :param sd: dict optained from TAC json files provided by Peyrard
    :return: Max number of system outputs for a doc
    """
    num_sys_outs = 0
    for data in sd.values():
        n = 0
        for sys_summ in data['annotations']:
            # Some summaries are written by humans with character summ_id
            if sys_summ['summ_id'].isnumeric():
                n += 1
        num_sys_outs = max(num_sys_outs, n)
    return num_sys_outs


def get_clean_text(text_list):
    """
    :param text_list: a list of strings
    :return: string - tokenized and with sent tags
    """
    text_list = [txt for txt in text_list if len(txt.strip()) > 0]
    text_list = [' '.join(utils.word_tokenize(txt, tokenizer)) for txt in text_list]
    text = utils.sent_list_to_tagged_str(text_list)
    return text


def convert_to_txt_files(sd):
    """
    :param sd: dict optained from TAC json files provided by Peyrard
    :return: None, creates reqd folder
    """
    num_sys_outs = get_num_sys_outs(sd)
    logger.info(f"Found maximum {num_sys_outs} total system outputs.")
    sys_path = os.path.join(args.out_dir, 'tac_system_summaries')
    try:
        os.mkdir(sys_path)
    except FileExistsError:
        pass
    src_fp = open(os.path.join(sys_path, 'src.txt'), 'w')
    ref_fp = open(os.path.join(sys_path, 'ref.txt'), 'w')
    out_fps = [open(os.path.join(sys_path, f'out_{idx}.txt'), 'w') for idx in range(num_sys_outs)]
    doc_num2topic = {}
    for doc_num, topic in enumerate(sd):
        logger.info(f"processing topic {topic}")
        doc_num2topic[doc_num] = topic
        data = sd[topic]
        src = ' '.join([get_clean_text(doc) for doc in data['documents']])
        ref = args.ref_sep.join([get_clean_text(doc[1]) for doc in data['references']])
        src_fp.write(src + '\n')
        ref_fp.write(ref + '\n')

        sys_out = data['annotations']
        for i in range(num_sys_outs):
            if i >= len(sys_out) or not sys_out[i]['summ_id'].isnumeric():
                # since some docs have less system summaries, mark the extra ones as duplicates
                out_txt = "### DUPLICATE ###"
            else:
                out_txt = get_clean_text(sys_out[i]['text'])

            out_fps[i].write(out_txt + '\n')

    json.dump(doc_num2topic, open(os.path.join(args.out_dir, 'doc_num2topic.json'), 'w'))
    src_fp.close()
    ref_fp.close()
    for fp in out_fps:
        fp.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-tac_files', nargs='+', required=True, help="Path to json files.")
    parser.add_argument('-out_dir', required=True, help='path to output folder')
    parser.add_argument('-ref_sep', default=' ||sep|| ')
    parser.add_argument('-log_file', default='../../logs/preprocess_tac.log')
    args = parser.parse_args()

    assert os.path.exists(args.out_dir), f"{args.out_dir} does not exist"

    logger = init_logger(args.log_file, log_file_level=logging.INFO)
    tokenizer = utils.get_word_tokenizer(tokenizer='spacy')
    sd = load_tac_json_files()
    convert_to_txt_files(sd)
