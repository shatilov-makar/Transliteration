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
path = 'Parsing\\robaeer.pdf'


def to_csv(arr):
    df = pd.DataFrame(arr)
    df.to_csv(f'sobir test.csv', sep=',')


def pers_data():
    reader = PdfReader(path)
    result = ''
    for page in reader.pages[1::]:
        text = page.extract_text()
        result += text  # + '\n\n'
        #result += text
    # segments = text.split(' \n ')  # strip() потом для каждого
   # to_dict = []
   # for i, segment in enumerate(segments):
    #    to_dict.append({'Number': i, 'segment': segment.strip()})
    print(result)
    # return result


data = pers_data()

to_csv(data)
# print(segments[11])
#pers_data = pers_data()
# to_csv(pers_data)
