# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 17:05:01 2020

@author: iima
"""
import pandas as pd
import requests
import time
import random
from bs4 import BeautifulSoup


# 主網頁=====================
# 組合URL
# 代理
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
      (KHTML, like Gecko) Element Browser 5.0', \
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
      'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
       Version/6.0 Mobile/10A5355d Safari/8536.25', \
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
       Chrome/28.0.1468.0 Safari/537.36', \
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

# 主頁面爬蟲
def main_page_crawler(url, payload):
    # 請求
    res = requests.get(url, params=payload)
    # 解析
    soup = BeautifulSoup(res.text, "html.parser")
    search_text = soup.find_all("a", class_='hlTitle_scroll') # 剝一層
    
    # 紀錄
    doc_title = []
    doc_url = []
    for ss in search_text:
        doc_title.append(ss.text)
        doc_url.append(ss['href'])
    
    # sleep
    time.sleep(1)
    
    return doc_title, doc_url

# 子頁面爬蟲
def sub_crawler(url, user_agent, sub_url):
    # 請求
    res = requests.get(url.replace('qryresultlst.aspx?', '')+sub_url, user_agent)
    # 解析
    soup = BeautifulSoup(res.text, "html.parser")
    search_text = soup.find('div', class_="int-table").text
    
    # sleep
    time.sleep(1)
    
    return search_text

# main==============
# 主網址
url = "https://law.judicial.gov.tw/FJUD/qryresultlst.aspx?"
# 參數
ty = 'JUDBOOK'
q = '7a56f5a4cdd68d79ef3ef694271416a5'
gy = 'jcourt'
ot = 'in'
page_list = range(1, 25)
gc_list = ['TPC', 'TPS', 'TPH', 'IPC', 'TCH', 'TNH', 'KSH', 
      'HLH', 'TPD', 'SLD', 'PCD', 'ILD', 'KLD', 'TYD', 
      'SCD', 'MLD', 'TCD', 'CHD', 'NTD', 'ULD', 'CYD', 
      'TND', 'KSD', 'CTD', 'HLD', 'TTD', 'PTD', 'PHD']
sort_list = ['DS', 'DB', 'LG', 'LB']
# 開爬
doc_titles = []
doc_urls = []
for page in page_list:
    for gc in gc_list:
        for sort in sort_list:
            # time cost = 25*28*4 = 2800 times
            user_agent = user_agents[random.randint(0, 6)]
            payload = {'ty': ty, 'q': q, 'gy': gy, 'ot': ot,
                       'page': page, 'gc': gc, 'sort': sort,
                       'user_agent': user_agent}
            doc_title, doc_url = main_page_crawler(url, payload)
            doc_titles.extend(doc_title)
            doc_urls.extend(doc_url)
doc = pd.DataFrame({'title': doc_titles, 'url': doc_urls})
doc = doc.drop_duplicates('title')
doc.to_csv(r'E:\Github\laws\data\判決書_主.csv', index=False)

# 子網頁
# 組合url
url = 'https://law.judicial.gov.tw/FJUD/'
# 子頁面
doc = pd.read_csv(r'E:\Github\laws\data\判決書_主.csv')
# 爬
doc_contents = []
for i in range(doc.shape[0]):
    # time cost = 26471/60/60 = 7.35 hr
    sub_url = doc['url'][i]
    user_agent = user_agents[random.randint(0, 6)]
    doc_content = sub_crawler(url, user_agent, sub_url)
    doc_contents.append(doc_content)
doc['content'] = doc_contents
#doc.iloc[0, 2]
doc.to_excel(r'E:\Github\laws\data\判決書.xlsx', index=False)

