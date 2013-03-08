import requests
from bs4 import BeautifulSoup
import re
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

#helper functions
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
    
    try:
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
                billDescription = billDescriptionTd.find('span').get_text()
                print billDescription
            except:
                print 'fail'
    except:
        return

def getParty(partyHref):
    
    data = data_from_http(partyHref)
    soup = BeautifulSoup(data)
    
    committeesList=[]
    committees = soup.find(id='PageContent').contents[0].find_next_sibling('div').find_all('td')[1].find_all('a')
    for committee in committees:
        if committee is not committees[-1]:
             committeesList.append([committee['href'],committee.string])
    
    party = soup.find(id='ctl00_PlaceHolderMain_lblParty').string
    district = soup.find(id='ctl00_PlaceHolderMain_hlDistrict').string
    districtNumber = re.findall(r'\d+', district)
    contactLink = soup.find(id='ctl00_PlaceHolderMain_hlEmail')['href'] 
    phone = soup.find(id='ctl00_PlaceHolderMain_hlDistrict').parent.find('table').get_text()
    phone = re.findall(r'\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}', phone)
    website = soup.find(id='ctl00_PlaceHolderMain_hlHomePage')['href']

    return party, districtNumber[0], phone[0], website,contactLink,committeesList
        
senateHref='http://www.leg.wa.gov/Senate/Senators/Pages/default.aspx'


base = 'http://www.leg.wa.gov'
houseHref = base +'/House/Representatives/Pages/default.aspx'
billsQuery = base + '/house/Representatives/Pages/BillSponsorship.aspx?m='


data = data_from_http(houseHref)
soup = BeautifulSoup(data)

table = soup.find(id='ctl00_PlaceHolderMain_dlMembers').find_all('a')
for a in table:
    if a == table[8]: #test only get firstperson
        
#         #vars needed for each party
#         name
#         abbreviation
#         order
#         #vars needed for each district
#         type 
#         number
#         #vars needed for each position
#         title
#         statewide
#         slug
#         rss_category
#         district
#         #vars needed for each vandidate
#         first_name
#         last_name
#         img_url
#         party
#         phone
        
        
        
        name = a.string
        print name
        href= base+a['href']
        #print a['href']
        firstName, lastName = nameArray(name)
        
        billsHref = billsQuery+lastName
        print billsHref
        #bills = getBills(billsHref)
        party,districtNumber,phone,website,contactLink,committeesList = getParty(href)
        position = 'State House: '
        print 'party: ' + party
        print 'districtNumber: ' + districtNumber
        print 'position: ' + position
        print 'phone: ' + phone
        print 'website: ' + website
        print 'contactLink: ' + contactLink
        




       
 
