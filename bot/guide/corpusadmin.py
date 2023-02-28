import csv
import re
from typing import List, Tuple

import natasha as nt
import pandas as pd


def csv_write(data: List[Tuple[str, str]], theme_name: str) -> None:
    with open(f'bot/data/{theme_name}.csv', 'wt') as fp:
        writer = csv.writer(fp, delimiter='@')
        writer.writerow(['text', 'token'])
        writer.writerows(data)


def doc_handler(theme_name: str) -> None:  # noqa:WPS210,WPS213 сложность для освобождения памяти
    with open(f'bot/data/{theme_name}.txt', 'r') as verdict:
        verdict_text = verdict.read()

    segmenter = nt.Segmenter()
    morph_vocab = nt.MorphVocab()
    emb = nt.NewsEmbedding()
    morph_tagger = nt.NewsMorphTagger(emb)
    syntax_parser = nt.NewsSyntaxParser(emb)
    ner_tagger = nt.NewsNERTagger(emb)

    doc = nt.Doc(verdict_text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    old_text = []
    corpus = []
    for sent in doc.sents:
        old_text.append(sent.text)
        new_sent = []
        for token in sent.tokens:
            token.lemmatize(morph_vocab)
            new_word = re.sub(r'\b[а-я,a-z,\d]\b', '', token.lemma)
            new_word = re.sub(r'[^\w]', '', new_word)
            if new_word == '':
                continue
            new_sent.append(new_word.strip())
        lemme_sent = str(' '.join(new_sent)).strip()
        corpus.append((sent.text, lemme_sent))
    csv_write(corpus, theme_name)


def normalize_text(user_response: str) -> str:  # noqa:WPS210 сложность для освобождения памяти
    segmenter = nt.Segmenter()
    morph_vocab = nt.MorphVocab()
    emb = nt.NewsEmbedding()
    morph_tagger = nt.NewsMorphTagger(emb)
    syntax_parser = nt.NewsSyntaxParser(emb)
    ner_tagger = nt.NewsNERTagger(emb)

    doc = nt.Doc(user_response)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    new_text = []
    for sent in doc.sents:
        new_sent = []
        for token in sent.tokens:
            token.lemmatize(morph_vocab)
            new_word = re.sub(r'\b[а-я,a-z,\d]\b', '', token.lemma)
            new_word = re.sub(r'[^\w]', ' ', new_word)
            if new_word == '':
                continue
            new_sent.append(new_word.strip())
        new_text.append(' '.join(new_sent))
    return str(new_text[0])


def load_rule(theme_name: str) -> pd.DataFrame:
    return pd.read_csv(f'bot/data/{theme_name}.csv', index_col=False, delimiter='@')
