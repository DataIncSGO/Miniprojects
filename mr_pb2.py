# Author: Selma Gomez Orr <selmagomezorrds@gmail.com> January 22, 2016

##########################################################################
## Imports
##########################################################################

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import heapq

from lxml import etree
from StringIO import StringIO


##########################################################################
## Constants
##########################################################################

WORD_RE = re.compile(r"\w+")

##########################################################################
## Modules
##########################################################################


class MRSimpleText(MRJob):    
    
    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_1_init,
                   mapper=self.mapper_1,
                   mapper_final=self.mapper_1_final,
                   reducer=self.reducer_1),
            MRStep(mapper_init=self.mapper_2_init,
                    mapper=self.mapper_2,
                    mapper_final=self.mapper_2_final,
                    reducer_init=self.reducer_2_init,
                    reducer=self.reducer_2,
                    reducer_final=self.reducer_2_final)
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
            for word in WORD_RE.findall(self.d[entry][1]):
                yield word.lower(), 1  
       
    def reducer_1(self, word, counts):
        yield word, sum(counts)
        
    def mapper_2_init(self):
        self.h=[]
        
    def mapper_2(self, word, counts):   
        heapq.heappush(self.h, (counts, word))
      

    def mapper_2_final(self):
        top_N = heapq.nlargest(100, self.h)
        for elem in top_N:
            yield None, (elem[1], elem[0])
    
    def reducer_2_init(self):
        self.g=[]
            
    def reducer_2(self, _, pair):
        for value in pair:
            heapq.heappush(self.g, value)
        
    def reducer_2_final(self):
        top_N_final = heapq.nlargest(100, self.g)
        for item in top_N_final:
            yield item[1], item[0]
           
        
        
##########################################################################
## Program - Miniprojects: mr_Simple_100
##########################################################################


if __name__== "__main__":

    MRSimpleText.run()

