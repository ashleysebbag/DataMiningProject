# DataMiningProject
Web scraping, Mysql, AWS, Visualization

## Description

Web Scraping is a technique employed to extract large amounts of data from websites whereby the data is extracted and saved to a local repository.
The project consists of scraping a website in order to create a database from which we can use artificial intelligence algorithms.

## Website

We are using Meetup website to find the events in Netanya in the field of data science

https://www.meetup.com/find/?keywords=data%20science'

However, the scraper can be used on any website. 

## Installation

Needs python installed in the OS

## Operating information

26/02/2020

Meetup is a java page, all the elements are dynamic. 
It is therefore necessary to use chrome driver to operate the selenium. 
It is also important that the scraper does not load the page all at once because it must allow time for the page to load completely. 
We must therefore add pause times. 

06/03/2020 

Argparse is used to initiate a CLI.
The code isencapsulated into classes in order to follow OOP principles
All the default values are stored in a configuration file named 'config.py'.

## Usage

```terminal
python meetup_scrapping.py
```

Returns elements of the website

Rreates a database

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## Reference

https://github.com/ashleysebbag/DataMiningProject
