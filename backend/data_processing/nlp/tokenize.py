from nltk import word_tokenize


def tokenize(text: str) -> list[str]:
    """Returns a list of words tokenized into their smallest unit of meaning."""
    return word_tokenize(text)
