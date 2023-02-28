import pandas as pd

import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader


def tokens(corpus_name):
    newcorpus = PlaintextCorpusReader('', f'data/{corpus_name}.txt')
    data = newcorpus.raw(newcorpus.fileids())
    return nltk.sent_tokenize(data)


def norm_frame(corpus_name):
    return pd.DataFrame(tokens(corpus_name), columns=['text'])

