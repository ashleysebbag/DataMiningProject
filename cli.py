#!/usr/bin/env python
# coding:utf-8
"""
Name    : cli.py
Author  : Ashley_SEBBAG Elie_GHANASSIA
Contact : ashsebbag@gmail.com elieghan@yahoo.fr
Time    : 05/03/2021 17:22
Desc    : Command line interface of Meetup Scrapper
"""

import config as cfg
import argparse
import scrapper as scr
import DB as db
import sys

HELP_STRING = """Welcome to Meetup scraper!
You can use 2 parameters:
1. Which type of events you want to scrape.
2. How many events you want to scape.

Usage:
"cli.py --help" - display this message 
"cli.py 'type' n" - will scrape n type events near to you and push it in DB.

Examples:
"cli.py" - will scrape all Data Science events near to you and push it in DB.
"cli.py surf" - will scrape all surf events near to you and push it in DB.
"cli.py "fast food" 10" - will scrape 10 fast food events near to you and push it in DB.
"""


# instantiate parser object
parser = argparse.ArgumentParser()

# command line options
parser.add_argument('type', help='type of event', nargs='?', type=str, default=None)
parser.add_argument('limit', help='number of events to scrape', nargs='?', type=int, default=None)

args, unknown = parser.parse_known_args()


# def check_input():
#     if not isinstance(args.limit, int):
#         raise ValueError(f'Incorrect limit of event entered. Please enter a digit.')


def scrape(url, n=0):
    meetup = scr.Scrapper(url)
    meetup.event_urls()
    meetup.event_info(n)
    print('Events data load')
    meetup.attendees_info()
    print('Attendees data load')
    meetup.members_info()
    print('Members data load')
    meetup.organisers_info()
    print('Organisers data load')
    return meetup


def push_in_db(meetup):
    data = db.Database()
    data.populate_tables_organizers(meetup.organisers_df)
    data.populate_tables_members(meetup.members_df)
    data.populate_tables_events(meetup.event_df)
    data.populate_tables_attendee(meetup.attendees_df)


def check_input():
    """
    Checks if the user input is correct
    """
    if args.type is None or args.limit is None or len(args) < 2:
        raise IOError('Not enough input parameters!')
    if len(unknown) > 0:
        raise IOError('Not enough input parameters!')
    if not args.limit.isdigit() :
        raise IOError(f'The limit should be an integer {args.limit}')
    if args.limit <= 0:
        raise IOError(f'The limit should be positive {args.limit}')


def main():
    try:
        check_input()
    except Exception as e:
        print(e)
        sys.exit(1)

def main():
    if args.type is None:
        url = cfg.DEFAULT_MEETUP_URL

        if args.limit is None:
            meetup = scrape(url)
        elif args.limit >= 0:
            meetup = scrape(url, args.limit)

    if args.type:
        url = cfg.MEETUP_URL + cfg.FIND + args.type.replace(" ", "%20")
        if args.limit is None:
            meetup = scrape(url)
        if args.limit >= 0:
            meetup = scrape(url, args.limit)

    else:
        print(HELP_STRING)

    try:
        push_in_db(meetup)

    except Exception:
        print(HELP_STRING)


if __name__ == '__main__':
    main()
