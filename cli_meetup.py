#!/usr/bin/env python
# coding:utf-8
"""
Name    : project_scrapperV2.py
Author  : Ashley_SEBBAG Elie_GHANASSIA
Contact : ashsebbag@gmail.com elieghan@yahoo.fr
Time    : 05/03/2021 17:22
Desc    :
"""

import config as CFG
import argparse
import urllib.request
import logging
from scrapper import Scrapper

MEETUP_URL = CFG.DB_URL
FI = CFG.FIND

def main():
    """
    CLI of project_scrapperV2.py
    """

    # instantiate parser object
    parser = argparse.ArgumentParser()

    # command line options
    parser.add_argument('type', help='type of event', nargs='?', type=str, default=CFG.DB_TYPE)
    parser.add_argument("-w", "--verbose", help=" welcome to the meetup scraper",
                        action="store_true")

    # parse cli options
    args = parser.parse_args()

    # Get the url argument and add the keyword
    url_scrap = MEETUP_URL
    type_scrap = args.type
    keyword = type_scrap.replace(' ', '%20')
    url_scrap = CFG.DB_URL_MEETUP
    type_scrap = args.type
    keyword = type_scrap.replace(' ', '%20')

    meetup = Scrapper(url_scrap)
    event = meetup.event_urls()
    info = meetup.event_info(5)


if __name__ == '__main__':
    main()
