
from pickle import TRUE
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


INIT = 'initial fragment'
FINAL = 'final fragment'
JOIN = 'join fragments'

part_n = 1
fragment_n = 1

tj_parts = ({INIT: 2, FINAL: 174}, {INIT: 1, FINAL: 115}, {INIT: 2, FINAL: 230}, {
    INIT: 2, FINAL: 141}, {INIT: 1, FINAL: 178}, {INIT: 1, FINAL: 141})

#tj_parts = ({INIT: 2, FINAL: 6}, {INIT: 1, FINAL: 6})

pers_parts = ({INIT: 1, FINAL: 173}, {INIT: 1, FINAL: 116, JOIN: [5, 6]}, {INIT: 1, FINAL: 229}, {
    INIT: 1, FINAL: 140}, {INIT: 1, FINAL: 179, JOIN: [122, 123]}, {INIT: 1, FINAL: 141}
)


# tj_parts = ({INIT: 2, FINAL: 3}, {INIT: 1, FINAL: 10}, {INIT: 2, FINAL: 230}, {
#   INIT: 2, FINAL: 141}, {INIT: 1, FINAL: 178}, {INIT: 1, FINAL: 141})

# pers_parts = ({INIT: 1, FINAL: 2}, {INIT: 1, FINAL: 11, JOIN: [5, 6]}, {INIT: 1, FINAL: 229}, {
#   INIT: 1, FINAL: 140}, {INIT: 1, FINAL: 179, JOIN: [122, 123]}, {INIT: 1, FINAL: 141}
# )

#url_tj = 'http://termcom.tj/index.php?menu=bases&page=mavlono_masnavi_1&sod=0&limit=3&lang=rus'
#response = requests.get(url_tj)
#soup = BeautifulSoup(response.text, 'lxml')
#title = ''
#poetry = ''
#content = soup.find_all('td', class_='body_txt')[-1]
#title = content.find('h1').text
# content.select('span')[0].extract()
# content.select('form')[0].extract()
#poetry = content.get_text('\n').replace(title, '').strip()
#title = soup.find_all('h1')[-1]
#poetry = soup.find_all('p')[-1]

# print(title)
# print(poetry)

#url_pers = 'https://ganjoor.net/moulavi/masnavi/daftar1/sh1'
#response = requests.get(url_pers)
#soup = BeautifulSoup(response.text, 'lxml')
#title = soup.find_all('h2')[-1]
# print(title.text)
# poetry = [str.get_text()
#          for str in soup.find_all('article')[-1].find_all('p')]
# print('\n'.join(poetry))


corpus = pd.DataFrame(columns=['book_title',
                               'title_tj', 'title_pers', 'text_tj', 'text_pers'])


def get_lxml(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url)
    return BeautifulSoup(response.text, 'lxml')


def first_part(part):
    arr = []
    print(part[INIT], part[FINAL])
    for fragment in range(part[INIT], part[FINAL]):
        print(fragment)
        title, poetry = tj_data(part, fragment)
        title_pers, poetry_pers = pert_text(fragment-1)
        arr.append({'book_title': f'rumi {1} {fragment}',
                    'title_tj': title, 'title_pers': title_pers, 'text_tj': poetry, 'text_pers': poetry_pers})
    to_csv(arr, 1)


def pers_data(fragment, i):
    url_pers = f'https://ganjoor.net/moulavi/masnavi/daftar{i+1}/sh{fragment}'
    soup_pers = get_lxml(url_pers)
    title_pers = soup_pers.find_all('h2')[-1].text.strip()
    poetry_pers = [str.get_text()
                   for str in soup_pers.find_all('article')[-1].find_all('p')]
    poetry_pers = '\n'.join(poetry_pers)
    return title_pers, poetry_pers


def tj_data(part, fragment, i):
    url = f'http://termcom.tj/index.php?menu=bases&page=mavlono_masnavi_{i+1}&sod=0&limit={fragment}'
    soup = get_lxml(url)
    title = ''
    poetry = ''
    content = ''
    if (fragment != part[INIT]):
        content = soup.find_all('td', class_='body_txt')[-1]
        content.select('form')[0].extract()
        content.select('span')[0].extract()
        title = content.find('h1').text
        poetry = content.get_text('\n').replace(title, '').strip()
    else:
        content = 'content'  # soup.find_all('p')[-1]
        # content.select('span')[0].extract()
        #poetry = content.get_text('\n').strip()
    return title, poetry


def parse():
    # for i in range(5,7):
    i = 5
    arr = []
    t = ''
    for fragment in range(tj_parts[i][INIT], tj_parts[i][FINAL]):
        print(fragment)
        tj_title, tj_poetry = tj_data(tj_parts[i], fragment, i)
        title_pers = ''
        poetry_pers = ''
        if (i == 0 or i == 2 or i == 3):
            title_pers, poetry_pers = pers_data(fragment-1, i)
        elif (i == 1 or i == 4):
            if (fragment < pers_parts[i][JOIN][0]):
                title_pers, poetry_pers = pers_data(fragment, i)
            elif (fragment == pers_parts[i][JOIN][0]):
                title_pers, poetry_pers = pers_data(fragment, i)
                p1, p2 = pers_data(fragment + 1, i)
                poetry_pers = '\n'.join([poetry_pers, p2])
            else:
                title_pers, poetry_pers = pers_data(fragment + 1, i)
        else:
            title_pers, poetry_pers = pers_data(fragment, i)
        arr.append({'book_title': f'rumi {i+1} {fragment}',
                    'title_tj': tj_title, 'title_pers': title_pers, 'text_tj': tj_poetry, 'text_pers': poetry_pers})
    to_csv(arr, i)


def to_csv(arr, i):
    df = pd.DataFrame(arr)
    df.to_csv(f'rumi {i + 1}.csv', sep=',')


def parse_tj():
    for i, part in enumerate(tj_parts):
        arr = []
        print(part[INIT], part[FINAL])
        for fragment in range(part[INIT], part[FINAL]):
            print(fragment)
            url = f'http://termcom.tj/index.php?menu=bases&page=mavlono_masnavi_{i+1}&sod=0&limit={fragment}'
            soup = get_lxml(url)
            title = ''
            poetry = ''
            content = ''
            if (fragment != part[INIT]):
                content = soup.find_all('td', class_='body_txt')[-1]
                content.select('form')[0].extract()
                content.select('span')[0].extract()
                title = content.find('h1').text
                poetry = content.get_text('\n').replace(title, '').strip()
            else:
                content = soup.find_all('p')[-1]
                content.select('span')[0].extract()
                poetry = content.get_text('\n').strip()
            arr.append({'book_title': f'rumi {i+1} {fragment}',
                        'title_tj': title, 'title_pers': None, 'text_tj': poetry, 'text_pers': None})
        to_csv(arr, i)


parse()
