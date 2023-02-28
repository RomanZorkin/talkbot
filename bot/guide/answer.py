from typing import List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bot.guide import corpusadmin


def create_tokens(user_response: str, theme_name: str) -> pd.DataFrame:
    base_corpus = corpusadmin.load_rule(theme_name)
    norm_response = corpusadmin.normalize_text(user_response)
    new_row = pd.DataFrame(columns=['text', 'token'])
    new_row.loc[0] = [user_response, norm_response]
    return pd.concat([base_corpus, new_row], ignore_index=True)


def best_index(tfidf):
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-6:-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        return [-1]
    return idx


def prepare_text(text_list: List[str], user_response: str) -> str:
    text_list.reverse()

    num_list = []
    for num, word in enumerate(text_list):
        num_list.append('{0}. {1}'.format(num + 1, word))

    text = '\n'.join(num_list)
    return f'Перечень подходящих вариантов по запросу "{user_response}":\n{text}'


def get_answer(user_response: str, theme_name: str) -> str:
    text_df = create_tokens(user_response, theme_name).dropna()
    tfidf_vec = TfidfVectorizer()
    tfidf = tfidf_vec.fit_transform(text_df['token'])
    idx = best_index(tfidf)

    if idx[0] < 0:
        del text_df, tfidf_vec, tfidf  # noqa:WPS420 free up memory
        return 'Извините, я не нашел ответа ...'
    answer = prepare_text(text_df.loc[idx, 'text'].to_list(), user_response)
    del text_df, tfidf_vec, tfidf  # noqa:WPS420 free up memory
    return answer
