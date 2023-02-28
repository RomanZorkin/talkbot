import os

import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from memory_profiler import profile


def load_from_env():
    return os.environ['APITOKEN']
