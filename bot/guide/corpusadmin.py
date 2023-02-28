import re
import string

import natasha as nt
import pandas as pd
from memory_profiler import profile

from bot import config


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
    res_dict = {_.text: _.lemma for _ in doc.tokens}

    return [res_dict[word] for word in res_dict]


def normalize_text(text: str) -> list[str]:
    return ' '.join(norm_tokens(text))


@profile
def update_corpus(theme_name: str):
    base_df = pd.DataFrame(config.norm_frame(theme_name))
    base_df['token'] = base_df['text'].apply(normalize_text)
    base_df.to_csv(f'bot/data/{theme_name}.csv', index=False, sep='@')
    del base_df


def load_rule(theme_name: str) -> pd.DataFrame:
    return pd.read_csv(f'bot/data/{theme_name}.csv', index_col=False, delimiter='@')
