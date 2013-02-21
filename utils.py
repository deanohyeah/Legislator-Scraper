import requests
from bs4 import BeautifulSoup


def data_from_http(href):

    try:
        r = requests.get(href)
        data = r.text
        return data
    except:
        print "can't get \n"+href
        print 'using '+ temp_file_name
        return open(temp_file_name)

def nameArray(fullName):
    nameArray = fullName.split(' ', 1 )
    return nameArray[0], nameArray[1]

def getBills(billsHref):
    bills = []
    data = data_from_http(billsHref)
    soup = BeautifulSoup(data)
    
    table = soup.find(id='ctl00_PlaceHolderMain_dgSponsoredBills').find_all('tr')
    #find each td in the row. add to the array. Return the array
        


politicians = {} #object to hold all of our scraped people

base = 'http://www.leg.wa.gov'

href = base +'/House/Representatives/Pages/default.aspx'

billsQuery = href+'?m='

data = data_from_http(href)

soup = BeautifulSoup(data)
table = soup.find(id='ctl00_PlaceHolderMain_dlMembers').find_all('a')

for a in table:

    name = a.string
    print a.string
    href= a['href']
    print a['href']
    firstName, lastName = nameArray('hello john')
    
    billsHref = billsQuery+lastName
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