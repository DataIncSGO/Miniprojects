# Author: Selma Gomez Orr <selmagomezorrds@gmail.com> January 15, 2016

##########################################################################
## Imports
##########################################################################

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

##########################################################################
## Constants
##########################################################################

url = "http://www.newyorksocialdiary.com/party-pictures?page="
base_url = "http://www.newyorksocialdiary.com"
stop_date = datetime.strptime('Monday, December 1, 2014', '%A, %B %d, %Y')
#base_url_2 = http://www.newyorksocialdiary.com/party-pictures?page=1
match = "pictures"

##########################################################################
## Program - Miniproject: Graph Redo
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
        

#Get only those captions within the established date range.
for i in range(0,len(date_list)):
    date = datetime.strptime(date_list[i],'%A, %B %d, %Y')
    if date < stop_date:
        valid_links.append(link_list[i])
        
        
#Select those tags and attributes which correspond to a photo caption.
raw_captions=[]
caps=[]

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
            
#For convenience pickle the data object.
import pickle

with open('CaptionsB','w') as f:
    pickle.dump(raw_captions,f)
    
#For convenience of time, work with the pickled object.
import pickle
captions = pickle.load(open('CaptionsB', 'r'))


#Eliminate those captions with excessively long length.
valid_captions = []
for item in captions:
    if len(item)<250:
        valid_captions.append(item)
        
#Eliminate some common words.
test_list = valid_captions
print len(test_list)

Title = ['President', 'president','Board Member','Sir','Honoree', 'Prima ballerina' ,'Trustee','Gala ', 'Event ', 'Girl Scout', 'Special Surgery', 'Dr.','Mrs.', 'Mr.', 'Ms.','Baroness', 'Princess', 'Ambassador','Commissioner', 'Police', 'Lung','Against', 'Foundation', 'Uniting','Mayor', 'Curator','Director', 'General', 'consul General','Honorable']
Nationality =['French', 'German', 'Russian', 'British', 'Spanish', "New York", 'France', 'Embassy', 'American']
Middle = ['Legal', 'Justice', 'friend', 'friends', 'guests', 'Jr. ','Co-men ','Co-man ', 'PhD', 'MD', 'CEO', 'Guest','M.D.', 'Jr.', 'Host','Co-Chairs','Co-Chairmen', 'Chairs', 'Chair','Chairman', 'Chairmen', '-Chairmen']
Common = ['Award', 'The', 'Steering Committee','his wife','man of','of the' ,'Actor','Actress', 'Playwright', 'Broadway', ' her husband ' ,'Have', 'Dream','Committee', 'Company','Dance', 'Cocktail', 'School', 'Annual', 'Gala', 'National', 'Fund', 'Kettering','Education', 'Humanitarian', 'Family', 'Museum','Historic','Natural History','Memorial']

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
    for common in Common:
        if common in test_list[i]:
            test_list[i]=test_list[i].replace(common,"")
            
#Split each caption entry on commas.
revised_list=[]
for y in test_list:
    revised_list.append(y.split(","))

#Take care of 'with' in caption by splitting into two strings.
for foto_element in revised_list:
    for t in range(0, len(foto_element)):
        if ' with ' in foto_element[t]:
            hold = foto_element[t].split('with')
            foto_element[t]=hold[0]
            foto_element.append(hold[1])


#Take care of 'and' in caption.  Three cases: before name, betweeen names married, and between names.
for foto_caption in revised_list:
    for s in range(0, len(foto_caption)):
        if ' and ' in foto_caption[s]:
            temp = foto_caption[s].split()
            if temp[0] == 'and':
                foto_caption[s] = " ".join(temp[1:])
            else:
                if temp[1] == 'and':
                    foto_caption[s] = " ".join(temp[2:])
                    foto_caption.append(" ".join([temp[0], temp[-1]]))
                else:
                    if temp[2] == 'and':
                        foto_caption[s] = " ".join(temp[3:])
                        foto_caption.append(" ".join(temp[0:2]))
                    else:
                        if len(temp)>4:
                            if temp[3]== 'and':
                                foto_caption[s] = " ".join(temp[4:])
                                foto_caption.append(" ".join(temp[0:3]))
                                                                                           
#Get rid of empty spaces at start of name.               
for clean_caption in revised_list:
    for r in range(0, len(clean_caption)):
        if clean_caption[r] != "" and clean_caption[r][0] == " ":
            clean_caption[r] = clean_caption[r][1:]
            
            
#Take care of long sentences by taking the first two names.
for foto_item in revised_list:
    for u in range(0, len(foto_item)):
        special = foto_item[u].split()
        if len(special)>4:
            foto_item[u]=special[0]+ " " + special[1]

#Remove empty lists.
for picture in revised_list:
    if picture == []:
        revised_list.remove(picture)
        
#Remove odd characters.

for foto_check in revised_list:
    for item in foto_check:
        if item == " ":
            foto_check.remove(item)
        if item == "  ":
            foto_check.remove(item)
        if item == "s":
            foto_check.remove(item)
        if item == 'a ':
            foto_check.remove(item)
            
            #if picture_item[v] == "  ":
                #picture_item.remove(picture_item[v])
            #if picture_item[v] == 's':
                #picture_item.remove(picture_item[v])

for foto_check2 in revised_list:
    for item2 in foto_check2:
        if item2 == '':
            foto_check2.remove(item2)
            
          
#Use itertools to create all of the combinations between people in the same foto.
import itertools

combinations_list=[]
for j in range(0,len(revised_list)):
    results = [x for x in itertools.combinations(revised_list[j], 2)]
    if results != []:
        combinations_list+=results
        
#Create graph to map all of the connections.
import networkx as nx
G=nx.Graph()
G.add_edges_from(combinations_list)

#Get information about the number of pictures for individuals.
listing_dict = dict(nx.degree(G))
listing = list(nx.degree(G))

#Create a dataframe of the information.
import pandas as pd
import numpy as np


df = pd.DataFrame([[key,value] for key,value in listing_dict.iteritems()],columns=["Name","Degrees"])

#Sort the list for top 100 people with connections.
top_df = df.sort(['Degrees'], ascending=[False])[:100]
top_df = top_df.reset_index(drop=True)


#Initialize the answer tuple for question one.
ANSWER1 = []
#Get the required values for the answer tuple.
for i in top_df.index:
    tup1=(top_df.iloc[i,0], top_df.iloc[i,1])
    ANSWER1.append(tup1)
print ANSWER1


#Obtain the pagerank information.
pr_dict = nx.pagerank_scipy(G, alpha=0.85)

pr_df = pd.DataFrame([[key,value] for key,value in pr_dict.iteritems()],columns=["Name","Rank"])


#Sort the list according to top ranks.
top_pr_df = pr_df.sort(['Rank'], ascending=[False])[:100]
top_pr_df = top_pr_df.reset_index(drop=True)


#Initialize the tuple for the second question.
ANSWER2 = []
#Get the required values for the answer tuple.
for i in top_pr_df.index:
    tup2=(top_pr_df.iloc[i,0], top_pr_df.iloc[i,1])
    ANSWER2.append(tup2)
print ANSWER2

#Create a multigraph for the connections.
import networkx as nx

M=nx.MultiGraph()
M.add_edges_from(combinations_list)

#Create a dictionary with all the connection pairs
friend_dict={}
for pair in combinations_list:
    edge_wt = M.number_of_edges(*pair)
    friend_dict[pair]=edge_wt

#Create a dataframe with the people pairs.
friend_df = pd.DataFrame([[key,value] for key,value in friend_dict.iteritems()],columns=["Pair","Num"])

#Get the top 200 because of the mirror connections of the pairs.
top_friends_df = friend_df.sort(['Num'], ascending=[False])[:200]
top_friends_df = top_friends_df.reset_index(drop=True)


#Initialize the tuple for question  three.  
ANSWER3 = []
check = 0
#Get the required values for the answer tuple. Eliminate mirror pairs
for i in top_friends_df.index:
    tup3=(top_friends_df.iloc[i,0], top_friends_df.iloc[i,1])
    pair = top_friends_df.iloc[i,0]
    rev_pair = (pair[1],pair[0])
    tup3_rev=(rev_pair, top_friends_df.iloc[i,1])
    if tup3_rev not in ANSWER3 and check<100:
        ANSWER3.append(tup3)
        check+=1
        
print len(ANSWER3)
print ANSWER3



