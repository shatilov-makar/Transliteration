from pickle import TRUE
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from turtle import color
import matplotlib.pyplot as plt
import math
import numpy as np
from numpy import load
import re
from PyPDF2 import PdfReader


def get_lxml(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url)
    return BeautifulSoup(response.text, 'lxml')


def pers_data():
    to_dict = []
    for i in range(1, 129):
        url_pers = f'https://ganjoor.net/roodaki/baghimande/sh{i}'
        print(i)
        soup_pers = get_lxml(url_pers)
        poetry_pers = [str.get_text()
                       for str in soup_pers.find_all('article')[-1].find_all('p')]
        poetry_pers = '\n'.join(poetry_pers)
        to_dict.append({'Number': i, 'segment': poetry_pers})
    return to_dict


def tj_data():
    reader = PdfReader(
        "C://Users//shati//Downloads//eb9a9b92-6d22-48b5-98e8-aeabeffac622.pdf")
    result = ''
    for page in reader.pages[1::]:
        text = page.extract_text()
        result += re.sub(r"www.sattor.com  \d+", "\n", text)
    segments = re.split(r"--\d+['—', '--']", text)  # strip() потом для каждого
    to_dict = []
    for i, segment in enumerate(segments):
        to_dict.append({'Number': i, 'segment': segment.strip()})
    return result


def to_csv(arr):
    df = pd.DataFrame(arr)
    df.to_csv(f'roodaki pers text only.csv', sep=',')


#tj_data = tj_data()
# to_csv(data)
# print(segments[11])
#pers_data = pers_data()
# to_csv(pers_data)

tj_orig = pd.read_csv('roodaki full.csv', sep=';', index_col=False)
del (tj_orig['Column1'])
tj_orig.to_csv(f'roodaki;full.csv', sep=',', index=False)
