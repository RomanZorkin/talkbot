import re
import string

import natasha as nt
import nltk
import pandas as pd
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

from bot import config


def norm_tokens(text):
    #Инициализируем вспомогательные объекты библиотеки natasha
    segmenter = nt.Segmenter()
    morph_vocab = nt.MorphVocab()
    emb = nt.NewsEmbedding()
    morph_tagger = nt.NewsMorphTagger(emb)
    ner_tagger = nt.NewsNERTagger(emb)

    #Убираем знаки пунктуации из текста
    text = re.sub(r'[^\w]', ' ', text.lower())
    text = re.sub(r'\b[а-я,a-z,\d]\b', ' ',  text)
    word_token = text.translate(str.maketrans('', '', string.punctuation)).replace('—', '')

    #Преобразуем очищенный текст в объект Doc и
    doc = nt.Doc(word_token)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    #Приводим каждое слово к его изначальной форме
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    resDict = {_.text: _.lemma for _ in doc.tokens}

    return [resDict[i] for i in resDict]


def normalize_text(text: str) -> list[str]:
    return ' '.join(norm_tokens(text))


def update_corpus(theme_name: str):
    base_df = config.norm_frame(theme_name)
    base_df['token'] = base_df['text'].apply(normalize_text)
    base_df.to_csv(f'data/{theme_name}.csv', index=False, sep='@')


def load_rule(theme_name: str) -> pd.DataFrame:
    return pd.read_csv(f'data/{theme_name}.csv', index_col=False, delimiter='@')
