# Author: Selma Gomez Orr <selmagomezorr@gmail.com> Copyright (C) January 5, 2016


##########################################################################
## Imports
##########################################################################

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pickle
import itertools
import networkx as nx
import pandas as pd
import numpy as np


##########################################################################
## Constants
##########################################################################

url = "http://www.newyorksocialdiary.com/party-pictures?page="
base_url = "http://www.newyorksocialdiary.com"
stop_date = datetime.strptime('Monday, December 1, 2014', '%A, %B %d, %Y')
#base_url_2 = http://www.newyorksocialdiary.com/party-pictures?page=1
match = "pictures"

##########################################################################
## Program 
##########################################################################

#Initialize lists
link_list=[]
date_list=[] 
valid_links=[]

#Obtain all the pages and check for valid captions.  First page skipped because of stop date.
for p in range(1,27):  
    response = requests.get(url+str(p))
    c = response.content
    soup = BeautifulSoup(c)

    test = soup.findAll(attrs={'class': 'field-content'})

    for link in test:
        link_string = str(link) 
        if re.search(match, link_string):
            href_string = str(link.next.get("href"))
            link_list.append(href_string)
        else:
            date_list.append(str(link.next))
        

#Only add urls for valid date range.        
for i in range(0,len(date_list)):
    date = datetime.strptime(date_list[i],'%A, %B %d, %Y')
    if date < stop_date:
        valid_links.append(link_list[i])

#Checkpoint value
print len(valid_links)

#Obtain raw captions for relevant tag and attribute.
raw_captions=[]
caps=[]
#for j in range(0,len(valid_links)):
for j in range(0,len(valid_links)):
    new_url=base_url + valid_links[j]
    response2 = requests.get(new_url)
    soup = BeautifulSoup(response2.content)
    caps1 = soup.select('.photocaption')
    caps2 = soup.select('font')
    caps=caps1+caps2
    for link in caps:
        if link.text != "":
            raw_captions.append(link.text)

#Checkpoint value
print len(raw_captions)

#Pickle result to avoid reprocessing data.
with open('CaptionsB','w') as f:
    pickle.dump(raw_captions,f)
    
#Load pickled results for processing.
captions = pickle.load(open('CaptionsB', 'r'))

#Eliminate lengthy captions.
valid_captions = []
for item in captions:
    if len(item)<250:
        valid_captions.append(item)
    if item=="":
        print "empty"

#Checkpoint value
print len(valid_captions) 

test_list = valid_captions
print len(test_list)

#Eliminate titles, nationality, special names.  Eliminate photographer names.
Title = ['President', 'president', 'Dr.','Mrs.', 'Mr.', 'Ms.','Baroness', 'Princess', 'Ambassador', 'Mayor', 'Curator','Director', 'General', 'consul General','Honorable']
Nationality =['French', 'German', 'Russian', 'British', 'Spanish']
Middle = ['de ', 'De ', 'von ', 'Von ']

for item in test_list:
    if "Photographs by" in item:
        test_list.remove(item)
for i in range(0, len(test_list)):
    for title in Title:
        if title in test_list[i]:
            test_list[i]=test_list[i].replace(title, "")
    for nat in Nationality:
        if nat in test_list[i]:
            test_list[i]=test_list[i].replace(nat, "")
    for mid in Middle:
        if mid in test_list[i]:
            test_list[i]=test_list[i].replace(mid, "")    

#Checkpoint value            
print len(test_list) 

#Create all the possible pairs for each set of photo captions.
combinations_list=[]
for j in range(0,len(revised_list)):
    results = [x for x in itertools.combinations(revised_list[j], 2)]
    if results != []:
        combinations_list+=results

#Checkpoint value
print len(combinations_list)


#Create Multi-graph
G=nx.Graph()
G.add_edges_from(combinations_list)

#Obtain dictionary of degrees for each person.
listing_dict = dict(nx.degree(G))

#Make a Dataframe of values
df = pd.DataFrame([[key,value] for key,value in listing_dict.iteritems()],columns=["Name","Degrees"])

#Get top 100
top_df = df.sort(['Degrees'], ascending=[False])[:100]

#Check values
print top_df.describe()


