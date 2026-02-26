import os
import string
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

_nltk_data_dir = os.environ.get("NLTK_DATA", "/tmp/nltk_data")
if _nltk_data_dir not in nltk.data.path:
    nltk.data.path.insert(0, _nltk_data_dir)


def _ensure_nltk_resource(resource_path: str, download_name: str) -> None:
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(download_name, quiet=True, download_dir=_nltk_data_dir)


_ensure_nltk_resource("corpora/stopwords", "stopwords")
_ensure_nltk_resource("corpora/wordnet", "wordnet")
_ensure_nltk_resource("corpora/omw-1.4", "omw-1.4")


@lru_cache(maxsize=1)
def _stop_words() -> set[str]:
    return set(stopwords.words("english"))


@lru_cache(maxsize=1)
def _lemmatizer() -> WordNetLemmatizer:
    return WordNetLemmatizer()


def preprocess_text(text: str, lemmatize: bool = True) -> str:
    text = str(text)

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = "".join([char for char in text if not char.isdigit()])

    stop_words = _stop_words()
    text = " ".join([word for word in text.split() if word not in stop_words])

    if lemmatize:
        lemmatizer = _lemmatizer()
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    return text
