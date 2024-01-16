from fastDamerauLevenshtein import damerauLevenshtein


def check_line_similarity(first_line, second_line, normalized=True):
    """
    Check similarity between two lines
    :param first_line: first line
    :param second_line: second line
    """
    return damerauLevenshtein(first_line, second_line, similarity=normalized)
