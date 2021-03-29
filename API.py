

#!/usr/bin/env python

# coding:utf-8

"""

Name    : API.py

Author  : Ashley_SEBBAG Elie Ghanassia

Contact : ashsebbag@gmail.com elieghan@yahoo.fr

Time    : 27/03/2021 17:09

Desc    :

"""


import pandas as pd

import DB as db

import config as cfg

import requests



def get_country(data):

    sql = f"SELECT country FROM Organizers"

    df = pd.read_sql(sql, data.con)

    df['country'] = df['country'].str.strip()

    country_list = list(set(df['country'].to_list()))

    return country_list


def get_country_info(country_list):


    countries = pd.DataFrame()

    for country in country_list:

        try:

            resp = requests.get(cfg.API_URL + country)

            txt = resp.json()

            tmp = pd.DataFrame(txt)

        except Exception:

            pass


        countries = countries.append(tmp, ignore_index=True)

    return countries


def enrich_data(data, countries):


    data.cur.execute("""CREATE TABLE IF NOT EXISTS Countries (

                                        country_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,

                                        name varchar(100),

                                        alpha2Code varchar(100),

                                        alpha3Code varchar(100),

                                        capital varchar(100),

                                        region varchar(100),

                                        subregion varchar(100),

                                        population int,

                                        demonym varchar(100),

                                        area varchar(100),

                                        timezones varchar(100)

                                        );

                                        """)

    # data.cur.execute("""ALTER TABLE Countries

    #                             ADD FOREIGN KEY(name)

    #                             REFERENCES Organizers(country);

    #                             """)



    for index, row_df in countries.iterrows():

        # print(row_df)

        unique_identifier = row_df['name']



        data.cur.execute(f"""SELECT name as unique_identifier 

                             FROM Countries WHERE name="{unique_identifier}";""")

        is_duplicate = data.cur.fetchone()



        if is_duplicate:

            country_name = is_duplicate['unique_identifier']

        else:

            country_name = []



        if unique_identifier in country_name:

            continue



        else:

            query = fr"""INSERT INTO Countries (name, alpha2Code, alpha3Code, capital, region, subregion, population,

                                                demonym, area, timezones) 

                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""



            data.cur.execute(query, (unique_identifier, row_df['alpha2Code'], row_df['alpha3Code'], row_df['capital'],

                                     row_df['region'], row_df['subregion'], row_df['population'], row_df['demonym'],

                                     row_df['area'], row_df['timezones']))



        data.con.commit()





def main():

    data = db.Database()

    country_list = get_country(data)

    country_table = get_country_info(country_list)

    print(country_table.columns)

    enrich_data(data, country_table)



if __name__ == '__main__':

    main()