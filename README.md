Legislator-Scraper
==================

Scrapes Representatives and legislators along with bills they sponsor

**Usage**
- Define the base url

`base = 'http://www.leg.wa.gov'`

- Define the url for either house or senate

`houseHref = base +'/House/Representatives/Pages/default.aspx'`

`senateHref = base +'/Senate/Senators/Pages/default.aspx'`
- Defind the position(this is for django implementation)
`position = 'State House'`

- Instantiate the scraper
`house = ScrapeLeg(houseHref,base,'State House')`
- Get scraping!
`house.scrapeIt()`


