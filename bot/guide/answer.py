import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bot.guide import corpusadmin


def create_tokens(user_response: str, theme_name: str) -> pd.DataFrame:
    base_corpus = corpusadmin.load_rule(theme_name)
    new_row = pd.DataFrame(columns=['text', 'token'])
    new_row.loc[0] = [user_response, corpusadmin.normalize_text(user_response)]
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


def prepare_text(text_list: list[str], user_response: str) -> str:
    text_list.reverse()
    text_list = [f'{num+1}. {word}' for num, word in enumerate(text_list)]
    text = '\n'.join(text_list)
    
    return f'Перечень подходящих вариантов по запросу "{user_response}":\n{text}'


def get_answer(user_response: str, theme_name: str) -> list[str]:
    text_df = create_tokens(user_response, theme_name)
    TfidfVec = TfidfVectorizer()  # Вызовем векторизатор TF-IDF
    tfidf = TfidfVec.fit_transform(text_df['token'])
    idx = best_index(tfidf)
    
    if idx[0] < 0:
        return 'Извините, я не нашел ответа ...'
    return prepare_text(
        text_df.loc[idx, 'text'].to_list(), user_response,
    )
