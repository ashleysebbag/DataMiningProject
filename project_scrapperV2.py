#!/usr/bin/env python
# coding:utf-8
"""
Name    : project_scrapperV2.py
Author  : Ashley_SEBBAG
Contact : ashsebbag@gmail.com
Time    : 05/03/2021 17:22
Desc    :
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time

MEETUP_URL = 'https://www.meetup.com'


class Scrapper:
    def __init__(self, web_page):
        self.web_page = web_page
        # self.event_list = event_urls(web_page)

    def event_urls(self):
        """
        This function returns event urls.

        Returns:
            event_urls (list): List of event urls.
        """
        event_list = []
        driver = webdriver.Chrome()

        driver.get(self.web_page)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'css-1jy1jkx'))
            show_more = EC.element_to_be_clickable((By.CLASS_NAME, "css-kpa5y4"))

            WebDriverWait(driver, 5).until(element_present)
            while True:
                try:
                    WebDriverWait(driver, 3).until(show_more).click()
                    time.sleep(5)
                except WebDriverException:
                    break
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        for event_link in soup.find_all('a', class_='css-2ne5m0'):
            event_list.append(event_link['href'])
        return event_list

    def attendees_link(driver, attendees_url):
        driver.get(attendees_url)
        time.sleep(3)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        attendees_links = []

        for attendee in soup.find_all('a', class_="", href=True):
            if 'members' in attendee['href'] and MEETUP_URL + attendee['href'] not in attendees_links:
                attendees_links.append(MEETUP_URL + attendee['href'][:-8])

        return attendees_links

    def event_info(event_list, n=len(event_list)):
        n_event_list = [x for index, x in enumerate(event_list) if index < n]

        driver = webdriver.Chrome()

        # initiate data storage
        titles = []
        times = []
        hosts = []
        organizers = []
        addresses = []
        details = []
        n_attendees = []

        member_links = []

        for event_url in n_event_list:
            attendees_links = []
            driver.get(event_url)
            content = driver.page_source
            soup = BeautifulSoup(content, 'lxml')

            titles.append(soup.find_all('h1', class_='pageHead-headline text--pageTitle')[0].text)
            times.append(soup.find_all('time')[0]['datetime'])
            hosts.append(soup.find_all('span', class_='text--bold event-hosts-info-no-link')[0].text)
            addresses.append(soup.find_all('p', class_='wrap--singleLine--truncate')[0].text)
            details.append(soup.find_all('div', class_='event-description runningText')[0].text)
            organizers.append(soup.find_all('span', class_='text--bold text--small display--inlineBlock')[0].text)
            n_attendees.append(int(re.findall('[0-9]+', soup.find_all('h3', class_='attendees-sample-total text--sectionTitle text--bold padding--bottom')[0].text)[0]))

            attendees_url = MEETUP_URL + soup.find_all('a', class_='attendees-sample-link link')[0]['href']
            attendees_links = attendees_link(driver, attendees_url)
            member_links = member_links + list(set(attendees_links) - set(member_links))

        return member_links


def main():
    url = 'https://www.meetup.com/find/?keywords=data%20science'
    meetup = Scrapper(url)
    print(len(meetup.event_urls()))


if __name__ == '__main__':
    main()
