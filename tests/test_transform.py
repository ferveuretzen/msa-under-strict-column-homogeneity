import pytest

from sch_msa.transform import align2merge, merged2aligned
from pydantic import ValidationError
from functools import reduce, partial


def test_align2merge_very_basic_case():
    inseq1 = ["A", "B", "C", "D", "E", "F"]
    inseq2 = ["A", "C", "E", "F", "B", "D"]
    inseq3 = ["A", "D", "E", "F", "B"]

    merged = reduce(align2merge, [inseq1, inseq2, inseq3])

    assert isinstance(merged, list)
    assert merged == ["A", "B", "C", "D", "E", "F", "B", "D"]


def test_align2merge_compfunc():
    inseq1 = ["A", "B", "C", "D", "E", "F"]
    inseq2 = ["a", "c", "e", "f", "b", "d"]
    inseq3 = ["a", "d", "e", "f", "b"]

    def compare_in_uppercase(x, y):
        return str(x).upper() == str(y).upper()

    align2merge4me = partial(align2merge, compfunc=compare_in_uppercase)

    merged = reduce(align2merge4me, [inseq1, inseq2, inseq3])
    merged = [s.upper() for s in merged]

    assert isinstance(merged, list)
    assert merged == ["A", "B", "C", "D", "E", "F", "B", "D"]


def test_align2merge_paramerters_type_error():
    with pytest.raises(ValidationError):
        align2merge("not a list", [])  # type: ignore
        align2merge([], "not a list")  # type: ignore
        align2merge([], [], 0)  # type: ignore
        align2merge([])  # type: ignore


def test_merged2aligned_very_basic_case():
    inseq1 = ["A", "B", "C", "D", "E", "F"]
    inseq2 = ["A", "C", "E", "F", "B", "D"]
    inseq3 = ["A", "D", "E", "F", "B"]
    merged = ["A", "B", "C", "D", "E", "F", "B", "D"]

    aligned = merged2aligned(merged, inseq1, "-")

    assert isinstance(aligned, list)
    assert aligned == ["A", "B", "C", "D", "E", "F"]

    aligned = merged2aligned(merged, inseq2, "-")

    assert isinstance(aligned, list)
    assert aligned == ["A", "-", "C", "-", "E", "F", "B", "D"]

    aligned = merged2aligned(merged, inseq3, "-")

    assert isinstance(aligned, list)
    assert aligned == ["A", "-", "-", "D", "E", "F", "B"]


def test_merged2aligned_compfunc():
    inseq1 = ["a", "b", "c", "d", "e", "f"]
    inseq2 = ["a", "c", "e", "f", "b", "d"]
    inseq3 = ["a", "d", "e", "f", "b"]
    merged = ["A", "B", "C", "D", "E", "F", "B", "D"]

    def compare_in_uppercase(x, y):
        return str(x).upper() == str(y).upper()

    aligned = merged2aligned(merged, inseq1, "-", compare_in_uppercase)

    assert isinstance(aligned, list)
    assert aligned == ["a", "b", "c", "d", "e", "f"]

    aligned = merged2aligned(merged, inseq2, "-", compare_in_uppercase)

    assert isinstance(aligned, list)
    assert aligned == ["a", "-", "c", "-", "e", "f", "b", "d"]

    aligned = merged2aligned(merged, inseq3, "-", compare_in_uppercase)

    assert isinstance(aligned, list)
    assert aligned == ["a", "-", "-", "d", "e", "f", "b"]


def test_merged2aligned_paramerters_type_error():
    with pytest.raises(ValidationError):
        merged2aligned("not a list", [], "-")  # type: ignore
        merged2aligned([], "not a list", "-")  # type: ignore
        merged2aligned([], [], 0)  # type: ignore
        merged2aligned([])  # type: ignore
