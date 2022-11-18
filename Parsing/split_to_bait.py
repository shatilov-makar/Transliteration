from cmath import nan
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def extract_baits():
    orig = pd.read_csv('rumi_results_clean\\rumi 6 new.csv', sep=',')
    orig = orig.dropna()
    cleaned_set = []
    for i, row in orig[1::].iterrows():
        tj_rows = row['text_tj'].split('\n')
        pers_rows = row['text_pers'].split('\n')
        if (len(tj_rows) == len(pers_rows)):
            for i, row in enumerate(tj_rows[::2]):
                tj_bait = tj_rows[i].strip()+'\n' + tj_rows[i+1].strip()
                pers_bait = pers_rows[i].strip() + '\n' + \
                    pers_rows[i+1].strip()
                cleaned_set.append({'tj': tj_bait, 'pers': pers_bait})

# extract_baits()


#df = pd.DataFrame(cleaned_set)
#df.to_csv('rumi_baits_6.csv', sep=',')

df = pd.read_csv('Parsing\\beits_1.csv', sep=",", index_col=False)
print(df.info())
