import requests
from bs4 import BeautifulSoup


def data_from_http(href):

    try:
        r = requests.get(href)
        data = r.text
        return data
    except:
        print "can't get \n"+href


def nameArray(fullName):
    nameArray = fullName.split(' ', 1 )
    return nameArray[0], nameArray[1]

def getBills(billsHref):
    bills = []
    data = data_from_http(billsHref)
    soup = BeautifulSoup(data)
    
    soup = soup.find(id='ctl00_PlaceHolderMain_dgSponsoredBills').findAll('tr')
    #skips first header row
    itersoup = iter(soup)
    next(itersoup)
    
    for tr in itersoup:
        billNumberTd = tr.findAll('td')[0]
        billDescriptionTd = tr.findAll('td')[1]
        try:  
            billNumber = billNumberTd.find('a').string
            print billNumber
            billDescription = billDescriptionTd.find('span').string
            print billDescription
        except:
            print 'fail'

       
        
    #find each td in the row. add to the array. Return the array
        


politicians = {} #object to hold all of our scraped people

base = 'http://www.leg.wa.gov'

href = base +'/House/Representatives/Pages/default.aspx'

billsQuery = 'http://www.leg.wa.gov/house/Representatives/Pages/BillSponsorship.aspx?m='

data = data_from_http(href)

soup = BeautifulSoup(data)
table = soup.find(id='ctl00_PlaceHolderMain_dlMembers').find_all('a')

for a in table:
    if a == table[0]: #test only get firstperson
        
        name = a.string
        print a.string
        href= a['href']
        print a['href']
        firstName, lastName = nameArray(name)
        
        billsHref = billsQuery+lastName
        print billsHref
        bills = getBills(billsHref)
    
    
    
    
#     r = representatives(
#         self.name,
#         self.position,
#         self.party,
#         self.info,
#         self.bills,
#     )
# get or create the rep
# r.bills = self.bills /* redefines the bills
    








class representatives(object):

    def __init__(self, name, position, party, info, bills):
        self.name = name
        self.position = position
        self.party = party
        self.info = info 
        self.bills = bills 

    def __unicode__(self):
        return "%s" % (self.name)

    def __repr__(self):
        # TODO
        return self.__unicode__()