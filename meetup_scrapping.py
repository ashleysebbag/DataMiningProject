#!/usr/bin/env python
# coding:utf-8
"""
Name    : meetup_scrapping.py
Author  : Ashley_SEBBAG, Elie_GHANASSIA
Contact : ashsebbag@gmail.com, elieghan@yahoo.fr
Time    : 13/02/2021 17:06
Desc    :
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


driver = webdriver.Chrome()
driver.get('https://www.meetup.com/find/?keywords=data%20science')

delay = 40 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'span')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

content = driver.page_source

# element = driver.find_element_by_css_selector("#hireme")
# html = driver.execute_script("return arguments[0].outerHTML;", element)
# print(html)
soup = BeautifulSoup(content, 'lxml')
print(soup)
