# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.PhantomJS('')
url_link = "http://news.sina.com.cn/"
driver.get(url_link)
data = driver.title
print data

# import sys
# import requests
# reload(sys)
# from bs4 import BeautifulSoup
# # sys.setdefaultencoding('uft-8')
# resp=requests.get('http://news.sina.com.cn/')
# resp.encoding = 'utf-8'
#
# bs = BeautifulSoup(resp.text)
#
# links = bs.find_all('a')
# for link in links:
#     print link.get('href')
# # for link in soup.find_all('a'):
# #     print(link.get('href'))
# #     # http://example.com/elsie


htmlcontend =resp.text

print type(htmlcontend)
with open('news.html','w') as html:
    html.writelines(htmlcontend.encode('utf-8'))
