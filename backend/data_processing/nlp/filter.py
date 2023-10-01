from nltk import download
from nltk.corpus import stopwords

download("stopwords")
EN_STOPWORDS = set(stopwords.words("english"))


def filter(words: list[str]):
    """Returns a list of words that are not found in the english stopwords set."""
    return [
        word for word in words if word.casefold() not in EN_STOPWORDS and word.isalnum()
    ]
