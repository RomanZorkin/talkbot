from bot.guide import wikiload


def start(uid: int | str):    
    with open(f'users/{uid}.txt', 'w') as config:
        config.write('')
    

def write(uid: str, theme_name: str):
    if theme_name not in wikiload.theme_list():
        return False
    with open(f'users/{uid}.txt', 'w') as config:
        config.write(theme_name)
    return True


def read_theme(uid: str):
    with open(f'users/{uid}.txt', 'r') as config:
        return config.read()