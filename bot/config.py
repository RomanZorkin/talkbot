import os

import nltk
import pandas as pd
from nltk.corpus.reader.plaintext import PlaintextCorpusReader


def tokens(corpus_name):
    newcorpus = PlaintextCorpusReader('', f'bot/data/{corpus_name}.txt')
    data = newcorpus.raw(newcorpus.fileids())
    return nltk.sent_tokenize(data)


def norm_frame(corpus_name):
    return pd.DataFrame(tokens(corpus_name), columns=['text'])


def load_from_env():
    return os.environ['APITOKEN']
