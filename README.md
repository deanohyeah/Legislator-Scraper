Washington State Legislator Scraper
==================

Scrapes house Representatives and Senators along with bills they sponsor from 
`http://www.leg.wa.gov/Senate/Senators/Pages/default.aspx` and `http://www.leg.wa.gov/house/representatives/Pages/default.aspx`


**Usage**
- Install dependencies (requests, beautifulsoup, lxml)`pip install -r requirments.txt`
- Define the base url `base = 'http://www.leg.wa.gov'`
- Define the url for either house or senate `houseHref = base +'/House/Representatives/Pages/default.aspx'`

`senateHref = base +'/Senate/Senators/Pages/default.aspx'`
- Define the position(this is for django implementation)
`position = 'State House'`

- Instantiate the scraper
`house = ScrapeLeg(houseHref,base,'State House')`
- Get scraping!
`house.scrapeIt()`


