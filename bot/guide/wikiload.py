import re
import requests
from pathlib import Path

import bs4


def test_url(url: str):
    if not re.search(r'^https://ru.wikipedia.org/wiki/', url):
        return None
    return re.sub(r'^https://ru.wikipedia.org/wiki/', '', url)


def load_theme(url: str):

    theme_name = test_url(url)
    if not theme_name:
        return None

    res = requests.get(url)
    res.raise_for_status()
    wiki = bs4.BeautifulSoup(res.text, 'html.parser')

    with open(f'data/{theme_name}.txt', 'w', encoding='utf-8') as f:
        for i in wiki.select('p'):
            f.write(i.getText())

    return theme_name


def theme_list():
    file_path = Path('data')
    ext = r'*.txt'
    return [corpus.stem for corpus in list(file_path.glob(ext))]
