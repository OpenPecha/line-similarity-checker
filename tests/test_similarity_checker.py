from line_similarity_checker.similarity_checker import check_line_similarity


def test_similarity_checker():
    """normalization score: 0.0 is least similar and 1.0 is most similar"""
    """when normalized = False, score is number of edits required to make two lines same"""
    """editing can be i)insertion ii)deletion iii)substitution iv)transposition(swapping)"""

    line1 = "ང་བོད་པ་ཡིན།"
    line2 = "ང་བོད་པ་ཡིན།"
    """lines are same, so score is 0 and normalized score is 1.0"""
    assert check_line_similarity(line1, line2, normalized=False) == 0
    assert check_line_similarity(line1, line2, normalized=True) == 1.0

    line1 = "ང་བོད་པ་ཡིན་"
    line2 = "ང་བོད་པ་ཡིན།"
    """only last character is different, so score is 1 and normalized score very high"""
    assert check_line_similarity(line1, line2, normalized=False) == 1.0
    assert check_line_similarity(line1, line2, normalized=True) == 0.9166666666666666

    line1 = "ང་བོད་པ་ཡིན།"
    line2 = "རྒྱ་གར་ནི་ས་ཆ་ཧ་ཅང་སྐྱིད་པོ་ཞིག་ཡིན།"
    """lines are very different, so score is 26 and normalized score is very low"""
    assert check_line_similarity(line1, line2, normalized=False) == 26.0
    assert check_line_similarity(line1, line2, normalized=True) == 0.2777777777777778


test_similarity_checker()
