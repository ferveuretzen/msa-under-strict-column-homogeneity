import os
import re
from pathlib import Path
from sch_msa.transform import align2merge, merged2aligned


def main():
    INPATH1 = "data/plain-text-bibles/kjv-bible-md/"
    INPATH2 = "data/plain-text-bibles/web-bible-md/"
    OUTPATH = "examples/"

    files1 = [file.name for file in Path(INPATH1).glob("*.md")]
    files2 = [file.name for file in Path(INPATH2).glob("*.md")]

    merged_files = align2merge(files1, files2)

    aligned1_files = merged2aligned(merged_files, files1, "")
    aligned2_files = merged2aligned(merged_files, files2, "")

    for merged_file in merged_files:
        if merged_file in aligned1_files and merged_file in aligned2_files:
            sequence1 = []
            sequence2 = []

            with open(INPATH1 + merged_file, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue

                    sequence1 += re.findall(r"\w+|[^\w\s]", line)[1:]  # separate special characters and sentence number

            with open(INPATH2 + merged_file, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue

                    sequence2 += re.findall(r"\w+|[^\w\s]", line)[1:]  # separate special characters and sentence number

            lower_sequence1 = [word.lower() for word in sequence1]
            lower_sequence2 = [word.lower() for word in sequence2]

            merged_bible = align2merge(lower_sequence1, lower_sequence2)

            aligned_bible1 = merged2aligned(merged_bible, lower_sequence1, "")
            aligned_bible2 = merged2aligned(merged_bible, lower_sequence2, "")

            for j, merged_word in enumerate(merged_bible):
                if aligned_bible1[j] == "":
                    aligned_bible1[j] = " " * len(merged_word)
                if aligned_bible2[j] == "":
                    aligned_bible2[j] = " " * len(merged_word)

            with open(os.path.splitext(OUTPATH + merged_file)[0] + ".out", "w") as fp:
                print(*aligned_bible1, file=fp)
                print(*aligned_bible2, file=fp)


if __name__ == "__main__":
    main()
