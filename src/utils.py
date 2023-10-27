from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

ERROR_MESSAGE_RESPONSE = 'Возникла ошибка при загрузке страницы {url}'
ERROR_MESSAGE_TAG = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise ConnectionError(ERROR_MESSAGE_TAG.format(url=url))


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=({} if attrs is None else attrs))
    if searched_tag is None:
        raise ParserFindTagException(
            ERROR_MESSAGE_TAG.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def making_soup(session, url, features='lxml'):
    response = get_response(session, url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, features=features)
