# Author: Selma Gomez Orr <selmagomezorrds@gmail.com> January 24, 2016

##########################################################################
## Imports
##########################################################################

from mrjob.job import MRJob
from mrjob.step import MRStep
import heapq

from lxml import etree
from StringIO import StringIO

import mwparserfromhell as mw

import math
from sets import Set


##########################################################################
## Constants
##########################################################################


##########################################################################
## Modules
##########################################################################

class MRDoubleLinks(MRJob):    

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_1_init,
                   mapper=self.mapper_1,
                   mapper_final=self.mapper_1_final,
                   reducer=self.reducer_1),
            
            MRStep(reducer=self.reducer_2),
            
            MRStep(reducer_init=self.reducer_3_init,
                   reducer=self.reducer_3,
                   reducer_final=self.reducer_3_final)                      
        ]    
    

    def mapper_1_init(self):
        self.m = ""
        self.d = {}
  
        
    def mapper_1(self, _, line):
        if "<page>" in line:
            self.m = ""
        if "</page>" not in line:
            self.m+=line 
        else:
            self.m+=line
            self.m = self.m.lstrip()
            if self.m[0:5]=="<page":
                root = etree.fromstring(self.m)
                title = root.findtext('title')
                date = root.getchildren()[3].findtext('timestamp')
                text = root.getchildren()[3].findtext('text')
                if text != None:
                    if title not in self.d:
                        self.d[title] = [date, text]
                    else:
                        if date > self.d[title][0]:
                            self.d[title]=[date, text]
                self.m = ""
            
    def mapper_1_final(self):
        
        #For each text entry of text, generate a unique list of links.
        for entry in self.d:
            working_text = self.d[entry][1]
            
            links_list = []
            
            #Parse the text and obtain the list of links.
            try:
                wikicode = mw.parse(working_text)
                links_list = wikicode.filter_wikilinks()
            except:
                pass
            
            #Initialize values
            article_links = 0
            
            #Initialize the list that will contain the clean titles of the links.
            links_title = []
            
            #If links are found, add them to the list of links then clean the format.
            if links_list != []:
                for link in links_list:
                    links_title.append(link.title)
                for h in range(0, len(links_title)):
                    links_title[h]=links_title[h].strip().lower()
                    
                #Create a set of the link titles to ensure only unique values, then return to list form.
                title_set = Set(links_title)
                title_list = list(title_set)
  
                #Remove article links for support sites.
                for item in title_list:
                    if ':' in item:
                        title_list.remove(item)
 
                #Get the number links in this reduced list.
                article_links=len(title_list)
        
                #Set the weight factor for each remaining link.
                weight = (10. + article_links)**-1
                
                #Get the title of the article and format as the link titles.
                article_title = entry.strip().lower()
                
                #Emit a tuple with weight
                if ':' not in article_title:
                    for name in title_list:
                        yield name, (article_title, name, weight)
                        yield article_title, (article_title, name, weight)
   
    
    def reducer_1(self, index, value_tup):     
        initiator = []
        connector = []
        for tup in value_tup:
            v_tup = tup
            if index == v_tup[0]:
                connector.append(v_tup)
            else:
                initiator.append(v_tup)                   
        for initial in initiator:
            for connect in connector:
                if initial[0] != connect[1]:
                    yield (initial[0], connect[1]), initial[2]*connect[2]
                
                
    def reducer_2(self, title_pair, weighting):
        sum_weights = 0
        for wt in weighting:
            w = wt
            sum_weights += w
        yield None, (sum_weights, title_pair)
    
     
    def reducer_3_init(self):
        self.h = []
            
    def reducer_3(self, _, pair):
        for thing in pair:
            heapq.heappush(self.h, thing)
            self.h = heapq.nlargest(100, self.h)
        
    def reducer_3_final(self):
        for answer in self.h:
            yield answer[1], answer[0]
        
        
        
##########################################################################
## Program - Miniprojects: mr_Double_100
##########################################################################

if __name__== "__main__":

    MRDoubleLinks.run()
