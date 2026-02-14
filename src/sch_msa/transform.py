import itertools
import numpy as np

from pydantic import validate_call


@validate_call
def align2merge(sequence1: list, sequence2: list) -> list:
    n_seq1 = len(sequence1)
    n_seq2 = len(sequence2)

    # make dp table

    dp_table = np.zeros((n_seq1 + 1, n_seq2 + 1), dtype=np.int32)
    dp_match = np.equal.outer(sequence1, sequence2)

    for x, y in itertools.product(range(n_seq1), range(n_seq2)):
        if dp_match[x, y]:
            dp_table[x + 1, y + 1] = dp_table[x, y] + 1
        else:
            dp_table[x + 1, y + 1] = max(dp_table[x, y + 1], dp_table[x + 1, y])

    # align sequences under strict column homogeneity

    seq1 = []
    seq2 = []

    x = n_seq1
    y = n_seq2

    while x > 0 and y > 0:
        if dp_match[x - 1, y - 1]:
            seq1.append(sequence1[x - 1])
            seq2.append(sequence2[y - 1])
            x -= 1
            y -= 1
            continue

        if dp_table[x - 1, y] > dp_table[x, y - 1]:
            seq1.append(sequence1[x - 1])
            seq2.append("")
            x -= 1
        else:
            seq1.append("")
            seq2.append(sequence2[y - 1])
            y -= 1

    while x > 0:
        seq1.append(sequence1[x - 1])
        seq2.append("")
        x -= 1
    while y > 0:
        seq1.append("")
        seq2.append(sequence2[y - 1])
        y -= 1

    # merge two sequences

    merged_seq = []

    for j in range(len(seq1)):
        if seq1[j] != "":
            merged_seq.append(seq1[j])
        else:
            merged_seq.append(seq2[j])

    return merged_seq[::-1]  # reverse merged sequence


@validate_call
def merged2aligned(merged_sequence: list, original_sequence: list, gap_charactor) -> list:
    aligned_seq = []

    p, n_seq = 0, len(original_sequence)

    for mseq in merged_sequence:
        if p < n_seq:
            if original_sequence[p] == mseq:
                aligned_seq.append(mseq)
                p += 1
            else:
                aligned_seq.append(gap_charactor)
        else:
            break

    return aligned_seq
