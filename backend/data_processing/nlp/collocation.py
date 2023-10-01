from nltk import Text


def collocation(words: list[str], n: int, span: int = 2):
    """Returns n collocations from words each with length span."""
    return Text(words).collocation_list(n, span)
