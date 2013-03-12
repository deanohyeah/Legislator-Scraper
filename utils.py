import requests
from bs4 import BeautifulSoup
import re
import os
import sys

class ScrapeLeg:
    def __init__(self,href,base,position):
        self.href= href
        self.base = base
        self.position = position

    def scrapeIt(self):
        data = self.data_from_http(senateHref)
        soup = BeautifulSoup(data)
        
        politicians = soup.find(id='ctl00_PlaceHolderMain_dlMembers').find_all('a')
        for politician in politicians:
            if politician == politicians[33]: #test only get firstperson
            #if a == a:    
                name = politician.string
                
                self.href= base+politician['href']
                self.firstName, self.lastName = self.nameArray(name)
                
                #gets variables for each legislator
                personInfo = self.getPersonInfo(self.href)
                self.party = personInfo[0]
                self.districtNumber = personInfo[1]
                self.phone = personInfo[2]
                self.website = personInfo[3]
                self.contactLink = personInfo[4]
                self.committeesList = personInfo[5]
                self.imgUrl = personInfo[6]
                self.billSponsorshipUrl = personInfo[7]
                
                self.billsList = self.getBills(base+self.billSponsorshipUrl)
                self.email = self.firstName+'.'+self.lastName+'@leg.wa.gov'       
                
                self.getPersonImg(self.imgUrl,self.firstName+'_'+self.lastName) #downloads images, only use on first run
                self.finalImgUrl = 'static/img/'+self.firstName+'_'+self.lastName+'.jpg'
                
                self.printVars()
                
    def printVars(self):
#         print name
        print 'fist name: ' + self.firstName
        print 'last name: ' + self.lastName
        print 'party: ' + self.party
        print 'districtNumber: ' + self.districtNumber
        print 'position: ' + self.position
        print 'phone: ' + self.phone
        print 'website: ' + self.website
        print 'contactLink: ' + self.contactLink
        print 'email: ' + self.email
        print 'img url: ' + self.finalImgUrl
       #  print self.committeesList
#         print self.billsList
            
    #helper functions
    def data_from_http(self,href):
        try:
            r = requests.get(href)
            data = r.text
            return data
        except:
            print "can't get \n"+href
    
    def nameArray(self,fullName):
        nameArray = fullName.split(' ', 1 )
        if len(nameArray) > 2:
            print 'WIERD NAME'
            print fullName
        return nameArray[0], nameArray[1]
    
    def getBills(self,billsHref):
        billsList = []
        data = self.data_from_http(billsHref)
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
    
        
    def getPersonInfo(self,partyHref):
        
        data = self.data_from_http(partyHref)
        soup = BeautifulSoup(data)
        
        committeesList=[]
        committees = soup.find(id='PageContent').contents[0].find_next_sibling('div').find_all('td')[1].find_all('a')
        for committee in committees:
            if committee is not committees[-1]: #last link is a link to hi rez photo
                 committeesList.append([base+committee['href'],committee.string])
        
        party = soup.find(id='ctl00_PlaceHolderMain_lblParty').string
        party = party.strip('()')
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
        return [party, districtNumber[0], phone[0], website,contactLink,committeesList,imgUrl,billSponsorshipUrl]
    
    def getPersonImg(self,imgUrl,imgName):
        imgFolder = '../../scraped-images/'
        f = open(imgFolder+imgName+'.jpg','wb')
        f.write(requests.get(imgUrl).content)
        f.close()
        
base = 'http://www.leg.wa.gov'
houseHref = base +'/House/Representatives/Pages/default.aspx'

senateHref = base +'/Senate/Senators/Pages/default.aspx'
position = 'State House'

house = ScrapeLeg(houseHref,base,'State House')
house.scrapeIt()

senate = ScrapeLeg(senateHref,base,'State Senate')
senate.scrapeIt()



       
 
