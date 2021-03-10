#!/usr/bin/env python
# coding:utf-8
"""
Name    : DB.py.py
Author  : Ashley_SEBBAG
Contact : ashsebbag@gmail.com
Time    : 09/03/2021 22:36
Desc    :
"""

import pymysql
import config as cfg
import logging
import sys
import re
import pandas as pd
import numpy as np
import scrapper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter('%(asctime)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

# Create a file handler and add it to logger.
file_handler = logging.FileHandler('web_scraper.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Database:
    def __init__(self):
        self.db_name = cfg.DATABASE_NAME
        self.con, self.cur = self.connect_db()
        self.con, self.cur = self.create_db()
        self.create_tables()

    def connect_db(self):
        con = pymysql.connect(host='localhost', user='root',
                              password=cfg.PASSWORD_DB_SERVER, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        return con, cur

    def create_db(self):
        query = f'CREATE DATABASE IF NOT EXISTS {self.db_name}'
        self.cur.execute(query)

        con = pymysql.connect(host='localhost', user='root', password=cfg.PASSWORD_DB_SERVER,
                              database=self.db_name, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()

        return con, cur

    def create_tables(self):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Organizers (
                            organizer_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                            organizer_identifier varchar(100),
                            organizer_name varchar(255),
                            city varchar(100),
                            country varchar(100),
                            member_num int
                            );
                            """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Members (
                            member_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                            member_identifier varchar(100),
                            member_name varchar(255),
                            city varchar(255),
                            country varchar(255),
                            member_since datetime,
                            meetup_num int
                            );
                            """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Events (
                            event_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                            event_identifier varchar(100),
                            organizer_id int,
                            title varchar(255),
                            times datetime,
                            host varchar(255),
                            address varchar(255),
                            details varchar(255),
                            attendees_num int
                            );
                            """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Attendees (
                            attendee_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
                            event_id int,
                            member_id int
                            );
                            """)

        self.cur.execute("""ALTER TABLE Events
                            ADD FOREIGN KEY(organizer_id) 
                            REFERENCES Organizers(organizer_id);
                            """)

        self.cur.execute("""ALTER TABLE Attendees
                            ADD FOREIGN KEY (event_id)
                            REFERENCES Events (event_id);
                            """)

        self.cur.execute("""ALTER TABLE Attendees
                            ADD FOREIGN KEY (member_id) 
                            REFERENCES Members (member_id);
                            """)

    def populate_tables_organizers(self, data):

        for index, row_df in data.iterrows():
            unique_identifier = row_df['organizer_identifier']

            self.cur.execute(f"""SELECT organizer_identifier as unique_identifier 
                                 FROM Organizers WHERE organizer_identifier="{unique_identifier}";""")
            is_duplicate = self.cur.fetchone()

            if is_duplicate:
                organizer_id = is_duplicate['unique_identifier']
            else:
                organizer_id = []

            if unique_identifier in organizer_id:
                print(organizer_id)
                continue

            else:
                query = fr"""INSERT INTO Organizers (organizer_identifier, organizer_name, city, country, member_num) 
                                    VALUES (%s, %s, %s, %s, %s);"""

                self.cur.execute(query, (unique_identifier, row_df['organizer_name'],
                                         row_df['city'], row_df['country'], row_df['members_num']))

            self.con.commit()


def main():
    url = 'https://www.meetup.com/find/?keywords=data%20science'
    meetup = scrapper.Scrapper(url)
    meetup.event_urls()
    meetup.event_info(n=1)
    meetup.attendees_info()
    meetup.members_info()
    meetup.organisers_info()

    data = Database()

    data.populate_tables_organizers(meetup.organisers_df)


if __name__ == '__main__':
    main()
