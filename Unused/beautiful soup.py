#!/usr/local/bin/python
###Sorts through all the websites for terms


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import cgitb
import os
cgitb.enable()


all_sites = []#list will store all URLs for news sites
siteTerms = {} #save a dictionary with id for the website and value is another dictionary with the terms

#asks user for new web address
def addurl():
    website = input('http://')
    siteName= input('Please uniquely identify the site (i.e. "nytimes"): ')
    website = 'http://' + website
    all_sites.append(website)
    return [website,siteName]

#determines if text is visible on website.
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return ""
    elif re.match('<!--.*-->', str(element)):
        return ""
    return element

def getHomePageText(URL):
    soup = BeautifulSoup(urlopen(URL).read())
 #   siteText = soup.NavigableString()
    siteLinks = soup.find_all('a')
    print(siteLinks.get('content'))
 #   visible_texts = filter(visible, siteText)
##    print(",".join(visible_texts))
    #return ",".join(visible_texts)

    
def saveTerms(string): #returns a list of words
    wordList = []
    wordList = re.findall(r'(romney|Romney|obama|Obama)+', string) #takes just the words
    return wordList

##def sentenceOfTerm(string):
##    sentences = []
##    sentences = re.findall(r'

#produces a dictionary of terms and their number of uses
def countTerms(someList):
    terms = {}
    for word in someList:
        word = str(word).lower() #keeps all the words lowercase
        if word not in terms:
            terms[word] = 1
        else:
            terms[word] += 1
    sortedTerms = sorted(terms)
##    print("\n'term': count")
    for i in sortedTerms:
        print(i+": "+str(terms[i]))
    return terms

#
def formatJSON(someSite,someDict):
    jsonObj = {someSite:someDict}
    if not os.path.exists('../json files'):
        os.makedirs('../json files')#adds folder one level up to save json files if it doesn't already exist
    jsonFile = open('../json files/'+someSite+'.json','w')#saves file outside of github repo
    json.dump(jsonObj,jsonFile)
    jsonFile.close()
    return jsonObj

def get(name, term):
    return siteTerms[name][term]

def main():
    #instructions
    print("""
    WEBSITE WORD COUNTER
    -Supply a website, and a name
    -Get a JSON file with word counts saved under that name
    -use get('website name','someWord') to retrieve a count of uses of someWord on the website.
    """)
    
    URL = addurl()
    print(URL);
    siteID= URL[1]
    siteTerms[siteID] = countTerms(saveTerms(getHomePageText(URL[0])))
    formatJSON(siteID,siteTerms[siteID])
    #print(siteTerms[siteID])



if __name__ == "__main__": main()

