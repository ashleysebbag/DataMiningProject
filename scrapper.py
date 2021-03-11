# !/usr/bin/env python
# coding:utf-8
"""
Name    : scrapper.py
Author  : Ashley_SEBBAG Elie_GHANASSIA
Contact : ashsebbag@gmail.com elieghan@yahoo.fr
Time    : 05/03/2021 17:22
Desc    : Meetup Scrapper
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import config as cfg
import pandas as pd
import time
import re

MEETUP_URL = cfg.MEETUP_URL


class Scrapper:
    def __init__(self, web_page):
        self.web_page = web_page
        self.driver = webdriver.Chrome()
        self.nb_event = 0

        # Urls
        self.event_list = []
        self.attendees_url = []
        self.organizers_url = []
        self.members_url = []

        # DataFrames
        self.event_df = pd.DataFrame()
        self.attendees_df = pd.DataFrame()
        self.members_df = pd.DataFrame()
        self.organisers_df = pd.DataFrame()

    def event_urls(self):
        """
        This function returns event urls.

        Returns:
            event_urls (list): List of event urls.
        """
        event_list = []

        self.driver.get(self.web_page)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'css-1jy1jkx'))
            show_more = EC.element_to_be_clickable((By.CLASS_NAME, "css-kpa5y4"))

            WebDriverWait(self.driver, 5).until(element_present)
            # while True:
            #     try:
            #         WebDriverWait(self.driver, 3).until(show_more).click()
            #         time.sleep(5)
            #     except WebDriverException:
            #         break
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        content = self.driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        for event_link in soup.find_all('a', class_='css-2ne5m0'):
            event_list.append(event_link['href'])

        self.event_list = event_list
        self.nb_event = len(event_list)

    def event_info(self, n=0):
        if n == 0 or n >= len(self.event_list):
            n = len(self.event_list)
        else:
            self.event_list = self.event_list[:n]

        # initiate data storage
        titles = []
        times = []
        hosts = []
        organizer_url_id = []
        addresses = []
        details = []
        attendees_num = []
        for event_url in self.event_list:
            self.driver.get(event_url)
            content = self.driver.page_source
            soup = BeautifulSoup(content, 'lxml')

            organizer_url_id.append(MEETUP_URL + soup.find_all('a', class_='event-group')[0]['href'])
            titles.append(soup.find_all('h1', class_='pageHead-headline text--pageTitle')[0].text)
            times.append(soup.find_all('time')[0]['datetime'])
            hosts.append(soup.find_all('span', class_='text--bold event-hosts-info-no-link')[0].text)
            addresses.append(soup.find_all('p', class_='wrap--singleLine--truncate')[0].text)
            details.append(soup.find_all('div', class_='event-description runningText')[0].text)
            attendees_num.append(int(re.findall('[0-9]+', soup.find_all('h3',
                                                                        class_='attendees-sample-total text--sectionTitle text--bold padding--bottom')[
                0].text)[0]))
            self.attendees_url.append(MEETUP_URL + soup.find_all('a', class_='attendees-sample-link link')[0]['href'])
            self.organizers_url = self.organizers_url + list(set(organizer_url_id) - set(self.organizers_url))

        # Store data into pandas dataframe
        self.event_df = pd.DataFrame({
            'event_identifier': ['event_' + x.split('/')[-1] for x in self.event_list[:n]],
            'organizer_identifier': ['org_' + x.split('/')[-1] for x in organizer_url_id],
            'title': titles,
            'time': times,
            'host': hosts,
            'address': addresses,
            'details': details,
            'attendees_num': attendees_num
        })

    def attendees_info(self):

        events_attendees = []
        for attendee_url in self.attendees_url:
            tmp_attendees = []
            self.driver.get(attendee_url)
            time.sleep(3)
            content = self.driver.page_source
            soup = BeautifulSoup(content, 'lxml')
            for attendee in soup.find_all('a', class_="", href=True):
                member_link = MEETUP_URL + '/' + '/'.join(attendee['href'][:-8].split('/')[-3:])
                if 'members' in attendee['href'] and member_link not in tmp_attendees:
                    tmp_attendees.append(member_link)
                    self.members_url = self.members_url + list(set(tmp_attendees) - set(self.members_url))

            events_attendees.append(tmp_attendees)

        att_dict = dict(zip(self.event_list, events_attendees))

        self.attendees_df = pd.DataFrame({
            'event_identifier': ['event_' + x.split('/')[-1] for x in self.event_list],
            'member_identifier': [['member_' + x.split('/')[-2] for x in group] for group in events_attendees]
        })
        self.attendees_df = self.attendees_df.explode('member_identifier')

    def members_info(self):

        member_name = []
        city = []
        country = []
        member_since = []
        meetup_num = []
        for member_link in self.members_url:
            self.driver.get(member_link)
            content = self.driver.page_source
            soup = BeautifulSoup(content, 'lxml')

            member_name.append(soup.find_all('span', class_='memName fn')[0].text)
            city.append(soup.find_all('span', class_='locality')[0].text)
            country.append(soup.find_all('span', class_='display-none country-name')[0].text)
            member_since.append(soup.find_all('p')[1].text)
            try:
                meetup_num.append(
                    int(re.findall('[0-9]+', soup.find_all('h2', class_='text--display3 flush--bottom')[0].text)[0]))
            except IndexError:
                meetup_num.append(0)

        self.members_df = pd.DataFrame({
            'member_identifier': ['member_' + x.split('/')[-2] for x in self.members_url],
            'member_name': member_name,
            'city': city,
            'country': country,
            'member_since': member_since,
            'meetup_num': meetup_num
        })

    def organisers_info(self):

        organizer_name = []
        city = []
        country = []
        members_num = []

        for organiser in self.organizers_url:
            self.driver.get(organiser)
            content = self.driver.page_source
            soup = BeautifulSoup(content, 'lxml')

            organizer_name.append(soup.find_all('a', class_='groupHomeHeader-groupNameLink')[0].text)
            city.append(soup.find_all('a', class_='groupHomeHeaderInfo-cityLink')[0].text.split(',')[0])
            country.append(soup.find_all('a', class_='groupHomeHeaderInfo-cityLink')[0].text.split(',')[1])
            try:
                members_num.append(
                    int(soup.find_all('a', class_='groupHomeHeaderInfo-memberLink')[0].text.split(' ')[0].replace(',', '')))
            except ValueError:
                fic = soup.find_all('a', class_='groupHomeHeaderInfo-memberLink')[0].text.split(' ')[0].replace(',', '')
                fic = re.sub('[^0-9]','', fic)
                members_num.append(fic)

        self.organisers_df = pd.DataFrame({
            'organizer_identifier': ['org_' + x.split('/')[-1] for x in self.organizers_url],
            'organizer_name': organizer_name,
            'city': city,
            'country': country,
            'members_num': members_num
        })


def main():
    url = 'https://www.meetup.com/find/?keywords=data%20science'
    meetup = Scrapper(url)
    meetup.event_urls()
    meetup.event_info(n=1)
    meetup.attendees_info()
    meetup.members_info()
    meetup.organisers_info()


if __name__ == '__main__':
    main()
