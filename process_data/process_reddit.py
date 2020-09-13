import pdb
import os
from sklearn.model_selection import train_test_split
import argparse


def listdir_fullpath(d):
    for f in os.listdir(d):
        yield os.path.join(d, f)


def get_all_summaries(folder_paths, subfolder='extractive'):
    all_summaries = {}
    for folder_path in folder_paths:
        summaries = read_summaries(os.path.join(folder_path, subfolder))
        for key in summaries:
            all_summaries[key] = summaries[key]
    return all_summaries


def read_summaries(folder_path):
    doc_paths = listdir_fullpath(folder_path)
    summ = {}
    for doc_name in doc_paths:
        full_name = doc_name.split('/')[-1]
        name = '.'.join(full_name.split('.')[:-1])
        end = full_name.split('.')[-1]
        if name not in summ:
            summ[name] = {}
        summ[name][end] = ' '.join(open(doc_name, encoding='utf-8', errors='ignore').read().split('\n'))
    return summ


def read_source_docs(folder_path):
    doc_paths = listdir_fullpath(folder_path)
    name2text = {}
    for doc in doc_paths:
        name = doc.split('/')[-1]
        name = '.'.join(name.split('.')[:-1])
        with open(doc, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().split('\n')
            text = ' '.join(text)
            name2text[name] = text
    return name2text


def write_aligned_data(name2src, ext_summs, abs_summs, out_folder, kind='union', train_val_test='0.8,0.1,0.1'):
    src, ext, abs = [], [], []
    for name in name2src:
        if name in ext_summs and name in abs_summs:
            if kind in ext_summs[name]:
                stext = name2src[name]
                etext = ext_summs[name][kind]
                atext = abs_summs[name]['abstractive']
                if len(stext) > 0 and len(etext) > 0 and len(atext) > 0:
                    src.append(name2src[name])
                    ext.append(ext_summs[name][kind])
                    abs.append(abs_summs[name]['abstractive'])

    train_size, val_size, test_size = [float(size) for size in train_val_test.split(',')]
    src_train_val, src_test, ext_train_val, ext_test, abs_train_val, abs_test = train_test_split(
        src, ext, abs, test_size=test_size
    )
    src_train, src_val, ext_train, ext_val, abs_train, abs_val = train_test_split(
        src_train_val, ext_train_val, abs_train_val, test_size=val_size
    )

    with open(os.path.join(out_folder, kind, 'src_train.txt'), 'w') as f:
        f.write('\n'.join(src_train))
    with open(os.path.join(out_folder, kind, 'ext_train.txt'), 'w') as f:
        f.write('\n'.join(ext_train))
    with open(os.path.join(out_folder, kind, 'abs_train.txt'), 'w') as f:
        f.write('\n'.join(abs_train))
    with open(os.path.join(out_folder, kind, 'src_val.txt'), 'w') as f:
        f.write('\n'.join(src_val))
    with open(os.path.join(out_folder, kind, 'ext_val.txt'), 'w') as f:
        f.write('\n'.join(ext_val))
    with open(os.path.join(out_folder, kind, 'abs_val.txt'), 'w') as f:
        f.write('\n'.join(abs_val))
    with open(os.path.join(out_folder, kind, 'src_test.txt'), 'w') as f:
        f.write('\n'.join(src_test))
    with open(os.path.join(out_folder, kind, 'ext_test.txt'), 'w') as f:
        f.write('\n'.join(ext_test))
    with open(os.path.join(out_folder, kind, 'abs_test.txt'), 'w') as f:
        f.write('\n'.join(abs_test))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-kind", default='union', help="union/majority/intersect")
    args = parser.parse_args()

    SRC_LEN = 476
    source_docs_path = "../../data/reddit/narrative"
    name2src = read_source_docs(source_docs_path)
    assert (len(name2src) == SRC_LEN)
    ext_summs = get_all_summaries(
        ["../../data/reddit/annotator_a", "../../data/reddit/annotator_b",
         "../../data/reddit/annotator_c", "../../data/reddit/annotator_d"]
    )
    abs_summs = get_all_summaries(
        ["../../data/reddit/annotator_a", "../../data/reddit/annotator_b",
         "../../data/reddit/annotator_c", "../../data/reddit/annotator_d"],
        subfolder='abstractive'
    )
    write_aligned_data(name2src, ext_summs, abs_summs, "../../data/reddit/processed", kind=args.kind)
