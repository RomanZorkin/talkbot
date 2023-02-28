import re

from memory_profiler import profile

from bot.guide import answer, corpusadmin, user, wikiload


def theme_list():
    themes = wikiload.theme_list()
    num_list = []
    for num, word in enumerate(wikiload.theme_list()):
        num_list.append('{0}. {1}'.format(num + 1, word))

    text = '\n'.join(num_list)
    return f'Перечень перечень существующих тем:\n{text}\n\nПример:\nВведите "choose: {themes[0]}"'


@profile
def load_handler(theme_name):
    if not theme_name:
        return 'Ошибка url адреса, адрес должен быть вида:\n\n"https://ru.wikipedia.org/wiki/..."'
    try:
        corpusadmin.doc_handler(theme_name)
        return f'Тема {theme_name} успешно загружена. Для выбора темы и дальнейшей работы введите "choose: {theme_name}".\nВы также можете загрузить новую тему повторив "load: https://ru.wikipedia.org/wiki/..."'
    except ValueError:
        return 'Возможно указанный вами формат url не поддерживается, попробуйте загрузить другую страницу, постарайтесь чтобы в адресе url отсутствовали нечитаемые символы )([]}{'


def choose_handler(theme_name, uid):
    if not user.write(uid, theme_name):
        themes = wikiload.theme_list()
        theme_text = '\n'.join(themes)
        return f'Введенная тема "{theme_name}" отсутствует в справочнике. Можете выбрать одну из загруженных:\n{theme_text}\nВведите "choose: {themes[0]}"'
    return f'Теперь вы можете задать вопрос по теме "{theme_name}"'


def conversation(text: str, uid):
    if re.match(r'^load: ', text):  # noqa:WPS360 control text
        return load_handler(wikiload.load_theme(re.sub(r'^load: ', '', text)))  # noqa:WPS360
    if re.match(r'^choose: ', text):  # noqa:WPS360 control text
        return choose_handler(re.sub(r'^choose: ', '', text), uid)  # noqa:WPS360 control text
    user_theme = user.read_theme(uid)
    if not user_theme:
        return 'Возможно вы не выбрали или не загрузили необходимую тематику'
    return answer.get_answer(text, user_theme)
