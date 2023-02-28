import re
from pathlib import Path
from typing import List, Optional

import bs4
import requests


def test_url(url: str) -> Optional[str]:
    if not re.search(r'^https://ru.wikipedia.org/wiki/', url):  # noqa:WPS360 control text
        return None
    return re.sub(r'^https://ru.wikipedia.org/wiki/', '', url)  # noqa:WPS360 control text


def load_theme(url: str) -> Optional[str]:

    theme_name = test_url(url)
    if not theme_name:
        return None

    res = requests.get(url)
    res.raise_for_status()
    wiki = bs4.BeautifulSoup(res.text, 'html.parser')

    with open(f'bot/data/{theme_name}.txt', 'w', encoding='utf-8') as new_corpus:
        for row in wiki.select('p'):
            new_corpus.write(row.getText())

    return theme_name


def theme_list() -> List[str]:
    file_path = Path('bot/data')
    ext = r'*.txt'  # noqa:WPS360 control text
    return [corpus.stem for corpus in list(file_path.glob(ext))]
