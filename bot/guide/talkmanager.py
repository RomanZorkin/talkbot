import re

from bot.guide import answer, corpusadmin, wikiload, user


def load_handler(theme_name):
    if not theme_name:
        return 'Ошибка url адреса, адрес должен быть вида:\n\n"https://ru.wikipedia.org/wiki/..."'
    try:
        corpusadmin.update_corpus(theme_name)
        return f'Тема {theme_name} успешно загружена. Для выбора темы и дальнейшей работы введите "choose: {theme_name}".\nВы также можете загрузить новую тему повторив "load: https://ru.wikipedia.org/wiki/..."'
    except ValueError:
        return 'Возможно указанный вами формат url не поддерживается, попробуйте загрузить другую страницу, постарайтесь чтобы в адресе url отсутствовали нечитаемые символы )([]}{'


def choose_handler(theme_name, uid):
    if not user.write(uid, theme_name):
        theme_list = wikiload.theme_list()
        theme_text = '\n'.join(theme_list)
        return f'Введенная тема "{theme_name}" отсутствует в справочнике. Можете выбрать одну из загруженных:\n{theme_text}\nВведите "choose: {theme_list[0]}"'
    return f'Теперь вы можете задать вопрос по теме "{theme_name}"'


def conversation(text: str, uid):

    if re.match(r'^load: ', text):
        return load_handler(wikiload.load_theme(re.sub(r'^load: ', '', text)))

    if re.match(r'^choose: ', text):
        return choose_handler(re.sub(r'^choose: ', '', text), uid)
 
    return answer.get_answer(text, user.read_theme(uid))
