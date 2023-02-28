import re
import string

import natasha as nt
import pandas as pd
import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader


def tokens(corpus_name):
    newcorpus = PlaintextCorpusReader('', f'bot/data/{corpus_name}.txt')
    data = newcorpus.raw(newcorpus.fileids())
    return nltk.sent_tokenize(data)


def norm_frame(corpus_name):
    return {'text': tokens(corpus_name)}


def make_doc(word_token):
    segmenter = nt.Segmenter()
    emb = nt.NewsEmbedding()
    morph_tagger = nt.NewsMorphTagger(emb)
    ner_tagger = nt.NewsNERTagger(emb)
    doc = nt.Doc(word_token)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)
    return doc


def norm_tokens(text):
    text = re.sub(r'[^\w]', ' ', text.lower())
    text = re.sub(r'\b[а-я,a-z,\d]\b', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    word_token = text.replace('—', '')

    morph_vocab = nt.MorphVocab()
    doc = make_doc(word_token)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    res_dict = {_.text: _.lemma for _ in doc.tokens}.copy()
    answer = [res_dict[word] for word in res_dict].copy()
    new_text = ' '.join(answer)

    return new_text


def update_corpus(theme_name: str):
    sent_dict = norm_frame(theme_name).copy()
    base_df = pd.DataFrame(sent_dict)
    base_df['token'] = base_df['text'].apply(norm_tokens)
    base_df.to_csv(f'bot/data/{theme_name}.csv', index=False, sep='@')


def load_rule(theme_name: str) -> pd.DataFrame:
    return pd.read_csv(f'bot/data/{theme_name}.csv', index_col=False, delimiter='@')
