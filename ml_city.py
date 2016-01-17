# Author: Selma Gomez Orr <selmagomezorrds@gmail.com> January 15, 2016

##########################################################################
## Imports
##########################################################################

import requests, urllib2, gzip, urllib
import pandas as pd
import numpy as np
import json
import ujson
import dill


##########################################################################
## Constants
##########################################################################

url = "http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_business.json.gz"


##########################################################################
## Program - Miniproject: ml City Model
##########################################################################


#Download file
urllib.urlretrieve(url,'Reviews')

reviews_list = []
with gzip.open('Reviews', 'rb') as f:
    for line in f.readlines():
        review = ujson.loads(line)
        reviews_list.append(review)

            
#Compute the mean by city, flatten the dataframe, and rename the columns.          
city_stats = df_reviews.groupby('city', as_index=False).agg({'stars': [np.mean]})
city_stats.columns = city_stats.columns.get_level_values(1)
city_stats.columns=['city','mean' ]

#Get the average of all the ratings for use for cities without a listing.
star_mean=city_stats.mean(axis=0)
AVG = float(star_mean)

#Put the data in the required format for the estimator.
estimator_dict = city_stats.set_index('city').to_dict()
estimator_dict = estimator_dict['mean']
estimator_dict['Other']=AVG

#Create the estimator.
class Estimator(object):
    def __init__(self, dict):
        self.dict = dict
    def predict(self, record):
        est_city = record['city']
        if est_city in self.dict:
            prediction = self.dict[est_city]
        else:
            prediction = self.dict['Other']
        return prediction
    
estimator = Estimator(estimator_dict)


#Store the instance using dill.
with open('est_file','w') as f:
    dill.dump(estimator,f)
    
    
    


