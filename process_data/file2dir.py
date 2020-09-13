import argparse
import os
import re

ARTICLE_FILENAME = "src.txt"
REFERENCE_SUM_FILENAME = "ref.txt"
SYSTEM_SUM_FILE_REGEX = "out(.*).txt"


# take docs and ref files with one line per doc, and save as one file per doc
# input_dir should have subdir for each model type and
def file_split(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for model_dir_name in os.listdir(input_dir):
        model_dir_path = os.path.join(input_dir, model_dir_name)
        if not os.path.isdir(model_dir_path):
            continue
        print(f"reading files in {model_dir_path}")
        # ensure the src and ref file paths all exist
        reference_summ_path = os.path.join(model_dir_path, REFERENCE_SUM_FILENAME)
        os.path.exists(reference_summ_path)
        # document_path = os.path.join(model_dir, ARTICLE_FILENAME)
        # if save_src_doc:
        #     os.path.exists(document_path)

        # find system summary paths
        system_summ_paths = [(os.path.join(model_dir_path, file), re.search(SYSTEM_SUM_FILE_REGEX, file).groups()[0])
                             for file in os.listdir(model_dir_path)
                             if re.search(SYSTEM_SUM_FILE_REGEX, file)]
        # make sure at least one system summary found
        assert len(system_summ_paths)>=1, "ensure at least one summary found"

        # create output sub-dir
        output_model_dir_path = os.path.join(output_dir, model_dir_name)
        os.mkdir(output_model_dir_path)
        # create sub-sub-dir for ref
        output_reference_sum_path = os.path.join(output_model_dir_path, os.path.basename(os.path.normpath(reference_summ_path)))
        os.mkdir(output_reference_sum_path)
        # create files in ref sub-sub-dir
        file2dir(dir_path=output_reference_sum_path, file_path=reference_summ_path)
        # create sub-sub-dir for outs
        for system_summ_path in [path for path,_ in system_summ_paths]:
            output_system_sum_path = os.path.join(output_model_dir_path, os.path.basename(os.path.normpath(system_summ_path)))
            os.mkdir(output_system_sum_path)
            # create files in out sub-sub-dir
            file2dir(file_path=system_summ_path, dir_path=output_system_sum_path)


def file2dir(file_path, dir_path):
    with open(file_path, 'r') as in_fp:
        for i,line in enumerate(in_fp):
            out_file_path = os.path.join(dir_path, f"{i}.txt")
            with open(out_file_path, 'w') as fp2:
                # TODO (maybe): some sentence splitting here? use NLTK punkt. Although ideally not needed as we should retain
                fp2.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', type=str, help=f"input dir", required=True)
    parser.add_argument('-od', type=str, help=f"output dir", required=True)
    args = parser.parse_args()
    file_split(input_dir=args.id, output_dir=args.od)
