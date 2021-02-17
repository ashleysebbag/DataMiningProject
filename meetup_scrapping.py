#!/usr/bin/env python
# coding:utf-8
"""
Name    : meetup_scrapping.py
Author  : Ashley_SEBBAG
Contact : ashsebbag@gmail.com
Time    : 13/02/2021 17:06
Desc    :
"""

from selenium import webdriver
from bs4 import BeautifulSoup


driver = webdriver.Chrome()

driver.get('https://www.meetup.com/find/?keywords=data%20science')
content = driver.page_source
soup = BeautifulSoup(content, 'lxml')
print(soup)