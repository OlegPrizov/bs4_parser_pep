import logging
import re
from urllib.parse import urljoin
from collections import defaultdict

import requests_cache
from tqdm import tqdm

from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEPS_URL, DOWNLOADS_DIR
from configs import configure_argument_parser, configure_logging
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, making_soup

DOWNLOAD_MESSAGE = 'Архив был загружен и сохранён: {archive_path}'
DIFFERENT_STATUSES_MESSAGE = (
    'Несовпадающий статус: {link}\n'
    'Статус в карточке: {status}\n'
    'Ожидаемые статусы: {pre_status}'
)
ARGUMENTS_MESSAGE = 'Аргументы командной строки: {args}'
CONNECTION_ERROR_MESSAGE = 'По адресу {url} ничего не нашлось.'


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = making_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = making_soup(session, version_link)
        results.append((
            version_link,
            find_tag(soup, 'h1').text,
            find_tag(soup, 'dl').text.replace('\n', ' ')
        ))
    return results


def latest_versions(session):
    soup = making_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = making_soup(session, downloads_url)
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag,
        'a',
        {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_MESSAGE.format(archive_path=archive_path))


def pep(session):
    soup = making_soup(session, PEPS_URL)
    section_tag = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    results = defaultdict(int)
    log_messages = []
    for tr_tag in tqdm(tr_tags):
        try:
            pre_status = EXPECTED_STATUS.get(find_tag(tr_tag, 'td').text[1:])
            link = urljoin(
                PEPS_URL,
                find_tag(tr_tag, 'a')['href']
            )
            soup = making_soup(session, link)
            dl_tag = find_tag(
                soup,
                'dl',
                {'class': 'rfc2822 field-list simple'}
            )
            status = dl_tag.select_one(':-soup-contains("Status") + dd').string
            if status not in pre_status:
                log_messages.append(
                    DIFFERENT_STATUSES_MESSAGE.format(
                        link=link,
                        status=status,
                        pre_status=pre_status
                    ))
            results[status] += 1
        except ConnectionError:
            log_messages.append(CONNECTION_ERROR_MESSAGE.format(url=link))
    list(map(logging.info, log_messages))
    return (
        [('Статус', 'Количество')]
        + sorted(results.items())
        + [('Всего', sum(results.values()))]
    )


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    try:
        configure_logging()
        logging.info('Парсер запущен!')
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(ARGUMENTS_MESSAGE.format(args=args))
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as exception:
        logging.exception(exception)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
