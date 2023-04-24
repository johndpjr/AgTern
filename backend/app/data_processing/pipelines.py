from .nlp import filter, freq_most_common, tokenize


def get_keywords(text: str, k: int = 5) -> str:
    """Returns a comma-separated string of k words ascending in frequency."""

    words = filter(tokenize(text))
    common_words = [word for word, _ in freq_most_common(words, k)]
    return ",".join(common_words)
