import os
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def scrape_sub_page(url, save_name, skip_exisintg=False):
    print(url)

    if(os.path.isfile(save_name) and skip_exisintg):
        print('file already exists. Skip')
        return

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')
    main_table = table[6]

    rows = main_table.find_all('tr')
    row_header = rows[0]
    col = row_header.find_all('td')
    col = [ele.text.strip() for ele in col]

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    data = np.array(data)
    df = pd.DataFrame(data=data[1:,1:], index=None, columns=data[0, 1:])
    df.to_csv(save_name)


def scrape_main_page(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')
    main_table = table[2]
    rows = main_table.find_all('tr')

    row_header = rows[0]
    col = row_header.find_all('td')
    col = [ele.text.strip() for ele in col]

    # get the main table data
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    # save main table to csv
    data = np.array(data)
    df = pd.DataFrame(data=data[1:-1,1:], index=None, columns=data[0, 1:])
    df.to_csv('checkee_main_table.csv')

    # get url for the sub pages
    url_set = []
    for row in rows[1:-1]:
        url = row.find('a').get('href')
        url_set.append(url)

    return url_set
    

base_url = "https://www.checkee.info/"

url_set = scrape_main_page(base_url)

for url in url_set:
    save_name = 'data/checkee_' + url.split('=')[-1] + '.csv'
    scrape_sub_page(base_url + url, save_name)
