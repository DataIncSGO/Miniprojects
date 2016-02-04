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
import numpy as np
import random


##########################################################################
## Constants
##########################################################################



##########################################################################
## Modules
##########################################################################

class MRSimpleLinks(MRJob):    
    

    def mapper_init(self):
        self.m = ""
        self.d = {}
        self.e = 0
  
        
    def mapper(self, _, line):
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
                if text == None:
                    self.e += 1
                self.m = ""
            
    def mapper_final(self):
        for entry in self.d:
            working_text = self.d[entry][1]
            wikicode = mw.parse(working_text)
            links_list = wikicode.filter_wikilinks()
            article_links = 0
            links_title = []
            if links_list != []:
                for link in links_list:
                    links_title.append(link.title)
                for h in range(0, len(links_title)):
                    links_title[h]=links_title[h].strip().lower()
                title_set = Set(links_title)
                article_links=len(title_set)
            yield "a", article_links
            yield "s", article_links*article_links
            yield "n", 1
        for k in range(0, self.e):
            yield "a", 1
            yield "s", 1
            yield "n", 1

            
   
    def reducer(self, type, link_count): 
        sum_links = 0
        res_count = 0
        res_list = []
        random_selection = random.sample(range(1, 188417), 2000)
        for value in link_count:
            v = value
            sum_links += v
            if res_count in random_selection:
                res_list.append(v)
            res_count += 1    
        arr = np.array(res_list)
        pfifty = np.percentile(arr, 50)
        pfive = np.percentile(arr, 5)
        ptwofive = np.percentile(arr, 25)
        psevfive = np.percentile(arr, 75)
        pninefive = np.percentile(arr, 95)
        yield type, sum_links
        yield type, res_count
        yield type, len(res_list)
        yield type, (50, pfifty)
        yield type, (5, pfive)
        yield type, (25, ptwofive)
        yield type, (75, psevfive)
        yield type, (95, pninefive)
    

               
  
  
        
##########################################################################
## Program - Miniprojects: mr_Simple_100
##########################################################################

if __name__== "__main__":

    MRSimpleLinks.run()
