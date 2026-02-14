import glob

from functools import reduce
from sch_msa.transform import align2merge, merged2aligned


def load_tfa_into_dic(filepath: str) -> dict[str, list[str]]:
    sequence_dic = {}

    sequence = []
    seq_name = None

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if line is None:
                continue

            if line.startswith(">"):
                if seq_name is not None:
                    sequence_dic[seq_name] = list("".join(sequence))

                seq_name = line[1:]
                sequence = []
            else:
                sequence.append(line)

        if seq_name is not None:
            sequence_dic[seq_name] = list("".join(sequence))

    return sequence_dic


def main():
    OUT_PATH = "examples/aligned_balibase3.out"

    with open(OUT_PATH, "w") as fp:
        TFA_FOLDER_PATH = "data/BAliBASE3/bb3_release/"

        tfa_path_list = sorted(glob.glob(TFA_FOLDER_PATH + "*/*.tfa"))

        for tfa_path_name in tfa_path_list:
            print(tfa_path_name)
            print(tfa_path_name, file=fp)

            SEQ_NAME_MAX_LEN = 12

            sequence_dic = load_tfa_into_dic(tfa_path_name)

            sequences = []

            for seq_name, sequence in sequence_dic.items():
                print(seq_name.ljust(SEQ_NAME_MAX_LEN), "".join(sequence), file=fp)

                sequences.append(sequence)

            merged_sequence = reduce(align2merge, sequences)

            print(file=fp)
            print("merged".ljust(SEQ_NAME_MAX_LEN), "".join(merged_sequence), file=fp)

            for seq_name, sequence in sequence_dic.items():
                aligned_sequence = merged2aligned(merged_sequence, sequence, "-")

                print(seq_name.ljust(SEQ_NAME_MAX_LEN), "".join(aligned_sequence), file=fp)

            print(file=fp)


if __name__ == "__main__":
    main()
