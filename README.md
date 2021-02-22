# DataMiningProject
Web scraping, Mysql, AWS, Visualization

# Website
We are using Meetup website to find the events in Netanya in the field of data science

https://www.meetup.com/find/?keywords=data%20science'


## Installation

Needs python installed in the OS


## Operating information

Meetup is a java page, all the elements are dynamic. 
It is therefore necessary to use chrome driver to operate the selenium. 
It is also important that the scraper does not load the page all at once because it must allow time for the page to load completely. 
We must therefore add pause times. 

## Usage

```terminal
python meetup_scrapping.py
```
returns elements of the website

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## Reference

https://github.com/ashleysebbag/DataMiningProject
