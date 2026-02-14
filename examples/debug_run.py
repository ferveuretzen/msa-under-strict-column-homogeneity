from sch_msa.transform import align2merge, merged2aligned
from functools import reduce


def main() -> None:
    inseq1 = ["A", "B", "C", "D", "E", "F"]
    inseq2 = ["A", "C", "E", "F", "B", "D"]
    inseq3 = ["A", "D", "E", "F", "B"]

    merged_seq = reduce(align2merge, [inseq1, inseq2, inseq3])

    outseq1 = merged2aligned(merged_seq, inseq1, "-")
    outseq2 = merged2aligned(merged_seq, inseq2, "-")
    outseq3 = merged2aligned(merged_seq, inseq3, "-")

    print("mergedseq", merged_seq)

    print("outseq1 =", outseq1)
    print("outseq2 =", outseq2)
    print("outseq3 =", outseq3)


if __name__ == "__main__":
    main()
