![image](https://user-images.githubusercontent.com/78728544/110751840-16b53880-824d-11eb-88cc-99b95077fa42.png)
# _DataMiningProject_
Web scraping, Mysql, AWS, Visualization

## Description

Web Scraping is a technique employed to extract large amounts of data from websites whereby the data is extracted and saved to a local repository.

The project consists of scraping a website in order to create a database from which we can use artificial intelligence algorithms.

The program runs from a CLI where it is possible to specifiy what type of event to scrape.


## Website

We are using Meetup website to find the events in Netanya in the field of data science

[link to Meetup!](https://www.meetup.com)

However, the scraper can be used on any website. 

## Installation

The Scraper requires certain packages to run and all must be installed via the requirements.txt file.
`pip3 --user install requirements.txt`
After installion of requirements.txt, file in the config.py update the mysql user and password.

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

10/03/2020 

The code creates a databased where all information is stored.


## Database
<img width="1070" alt="Screenshot 2021-03-11 at 09 36 02" src="https://user-images.githubusercontent.com/78728544/110751965-419f8c80-824d-11eb-8851-297080f00f14.png">


## Usage

```terminal
python meetup_scrapping.py type loacation
```

type : type of event, default = 'Machine Learning'

location : location of the event, default = 'Netanya'

Returns elements of the website

Creates a database

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## Reference

https://github.com/ashleysebbag/DataMiningProject
