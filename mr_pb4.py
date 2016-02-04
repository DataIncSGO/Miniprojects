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

##########################################################################
## Constants
##########################################################################

n_grams = [1,2,3]

##########################################################################
## Modules
##########################################################################

class MREntropy(MRJob):    
    
    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_1_init,
                   mapper=self.mapper_1,
                   mapper_final=self.mapper_1_final,
                   combiner=self.combiner_1,
                   reducer=self.reducer_1),
            MRStep(reducer=self.reducer_2)
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
        for entry in self.d:
            working_text = self.d[entry][1]
            wikicode = mw.parse(working_text)
            new_text = " ".join(" ".join(fragment.value.split())
                for fragment in wikicode.filter_text())
            b = new_text
            for n in n_grams:
                grams = [b[i:i+n] for i in range(len(b)-n+1)]
                for chars in grams:
                    yield (n, chars), 1
            #new_text = new_text.split()
            #for n in n_grams:
                #for b in new_text:
                    #grams = [b[i:i+n] for i in range(len(b)-n+1)]
                    #for chars in grams:
                        #yield (n, chars), 1
            
            
    def combiner_1(self, pair, count):
        yield pair, sum(count)
       
    def reducer_1(self, pair, counts):
        n_i = sum(counts)
        val_i = n_i*(math.log(n_i,2))
        yield (pair[0],'N'), n_i
        yield (pair[0],'term_sum'), val_i
           
    
    def reducer_2(self, type, in_value):
        yield type, sum(in_value)
        
       
        
##########################################################################
## Program - Miniprojects: mr_Simple_100
##########################################################################

if __name__== "__main__":

    MREntropy.run()
