import os

import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from memory_profiler import profile
@profile
def tokens(corpus_name):
    newcorpus = PlaintextCorpusReader('', f'bot/data/{corpus_name}.txt')
    data = newcorpus.raw(newcorpus.fileids())
    return nltk.sent_tokenize(data)

@profile
def norm_frame(corpus_name):
    return {'text': tokens(corpus_name)}
    #return pd.DataFrame(tokens(corpus_name), columns=['text'])


def load_from_env():
    return os.environ['APITOKEN']
