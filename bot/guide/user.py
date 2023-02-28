from bot.guide import wikiload


def start(uid: int):
    with open(f'bot/users/{uid}.txt', 'w') as config:
        config.write('')


def write(uid: int, theme_name: str):
    if theme_name not in wikiload.theme_list():
        return False
    with open(f'bot/users/{uid}.txt', 'w') as config:
        config.write(theme_name)
    return True


def read_theme(uid: int):
    try:
        with open(f'bot/users/{uid}.txt', 'r') as config:
            return config.read()
    except FileNotFoundError:
        return None
