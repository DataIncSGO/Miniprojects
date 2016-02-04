# Author: Selma Gomez Orr <selmagomezorrds@gmail.com> January 18, 2016

##########################################################################
## Imports
##########################################################################

from mrjob.job import MRJob
from mrjob.step import MRStep
import requests
import re
import heapq


##########################################################################
## Constants
##########################################################################

WORD_RE = re.compile(r"\w+")

##########################################################################
## Modules
##########################################################################


class MRSimplePlain(MRJob):    
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper_1,
                   reducer=self.reducer_1),
            MRStep(mapper_init=self.mapper_2_init,
                    mapper=self.mapper_2,
                    mapper_final=self.mapper_2_final,
                    reducer_init=self.reducer_2_init,
                    reducer=self.reducer_2,
                    reducer_final=self.reducer_2_final)
        ]

    
    def mapper_1(self, _, data_file):
        for word in WORD_RE.findall(data_file):
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

    MRSimplePlain.run()

