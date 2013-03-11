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
    if len(nameArray) > 2:
        print 'WIERD NAME'
        print fullName
    return nameArray[0], nameArray[1]

def getBills(billsHref):
    billsList = []
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
                billDescription = billDescriptionTd.find('span').get_text()
                billRssFeed = 'http://apps.leg.wa.gov/billinfo/SummaryRss.aspx?bill='+billNumber+'&year=2013'
                billsList.append([billNumber,billDescription,billRssFeed])
                
            except:
                print 'fail'
            
        return billsList
    except:
        return

    
def getPersonInfo(partyHref):
    
    data = data_from_http(partyHref)
    soup = BeautifulSoup(data)
    
    committeesList=[]
    committees = soup.find(id='PageContent').contents[0].find_next_sibling('div').find_all('td')[1].find_all('a')
    for committee in committees:
        if committee is not committees[-1]: #last link is a link to hi rez photo
             committeesList.append([base+committee['href'],committee.string])
    
    party = soup.find(id='ctl00_PlaceHolderMain_lblParty').string
    district = soup.find(id='ctl00_PlaceHolderMain_hlDistrict').string
    districtNumber = re.findall(r'\d+', district)
    try:
        contactLink = soup.find(id='ctl00_PlaceHolderMain_hlEmail')['href']
    except:
        contactLink = ''
    phone = soup.find(id='ctl00_PlaceHolderMain_hlDistrict').parent.find('table').get_text()
    #regex to grab phone
    phone = re.findall(r'\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}', phone)
    website = soup.find(id='ctl00_PlaceHolderMain_hlHomePage')['href']
    imgUrl = soup.find(id='ctl00_PlaceHolderMain_imgPhoto')['src']
    billSponsorshipUrl = soup.find(id='ctl00_PlaceHolderMain_hlBillSponsorship')['href']
    return party, districtNumber[0], phone[0], website,contactLink,committeesList,imgUrl,billSponsorshipUrl

def getPersonImg(imgUrl,imgName):
    imgFolder = '../../scraped-images/'
    f = open(imgFolder+imgName+'.jpg','wb')
    f.write(requests.get(imgUrl).content)
    f.close()
    



base = 'http://www.leg.wa.gov'
houseHref = base +'/House/Representatives/Pages/default.aspx'

data = data_from_http(houseHref)
soup = BeautifulSoup(data)

table = soup.find(id='ctl00_PlaceHolderMain_dlMembers').find_all('a')
for a in table:
    if a == table[33]: #test only get firstperson
    #if a == a:    
        name = a.string
        
        href= base+a['href']
        firstName, lastName = nameArray(name)
        
        #gets variables for each legislator
        party,districtNumber,phone,website,contactLink,committeesList,imgUrl,billSponsorshipUrl = getPersonInfo(href)
       
        billsList = getBills(base+billSponsorshipUrl)
        email = firstName+'.'+lastName+'@leg.wa.gov'       
        position = 'State House'
        getPersonImg(imgUrl,firstName+'_'+lastName) #downloads images, only use on first run
        finalImgUrl = 'static/img/'+firstName+'_'+lastName+'.jpg'
        
#         print name
        print 'party: ' + party
#         print 'districtNumber: ' + districtNumber
#         print 'position: ' + position
#         print 'phone: ' + phone
#         print 'website: ' + website
#         print 'contactLink: ' + contactLink
#         print 'img url: ' + finalImgUrl
#         print committeesList
        print billsList
        




       
 
