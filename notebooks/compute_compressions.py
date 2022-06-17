import argparse

import pandas as pd
from smell_helpers import get_files, load_json


def get_compression(lengths):
    start_length = lengths[0]
    end_length = lengths[-1]
    return end_length / start_length


parser = argparse.ArgumentParser()
parser.add_argument("output_file")
parser.add_argument("input_folders", nargs="+")
args = parser.parse_args()

files = []
files_short = set()
for folder in args.input_folders:
    files.extend(
        [
            f"{folder}/{f}"
            for f in get_files(folder, full_path=False)
            if f not in files_short
        ]
    )
    new_files = get_files(folder, full_path=False)
    files_short.update(new_files)
    assert len(files) == len(files_short)
    print(f"After {folder}: {len(files)} files (of 1317)")

df = pd.DataFrame(
    index=[f.split("/")[-1][:-5] for f in files],
    columns=["year", "title", "n_steps", "start_length", "end_length", "compression"],
)
for idx, file in enumerate(files):
    if idx % 100 == 0:
        print(f"Processing file {idx}...")
    data = load_json(file)
    lengths = data["total_lengths"]
    compression = get_compression(lengths)
    idx = file.split("/")[-1][:-5]
    df.loc[idx] = [
        int(idx[-4:]),
        int(idx[:2]),
        len(lengths),
        lengths[0],
        lengths[-1],
        compression,
    ]
df.to_csv(args.output_file)
