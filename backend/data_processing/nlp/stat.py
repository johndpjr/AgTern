from nltk import FreqDist


def freq_most_common(words: list[str], n: int = None) -> list[tuple[str, int]]:
    """Returns a list of n most common elements.
    Counts all elements when n is None.
    """
    fdist = FreqDist(words)
    return fdist.most_common(n)
