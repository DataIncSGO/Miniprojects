# Author: Selma Gomez Orr <selmagomezorrds@gmail.com> January 15, 2016

##########################################################################
## Imports
##########################################################################

import os
import requests, urllib2, gzip, urllib
import pandas as pd
import numpy as np
import json
import ujson
import dill

from sklearn.cross_validation import train_test_split as tts
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import f_regression
from sklearn.ensemble import RandomForestRegressor



##########################################################################
## Constants
##########################################################################

url = "http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_business.json.gz"

##########################################################################
## Program - Miniproject: ml Latitude Longitude
##########################################################################

#Download file
urllib.urlretrieve(url,'Reviews')

reviews_list = []
with gzip.open('Reviews', 'rb') as f:
    for line in f:
        review = ujson.loads(line)
        reviews_list.append(review)
          
            
df_reviews = pd.DataFrame(reviews_list)


#Identify columns for model.
X_var = ['latitude', 'longitude']
y_var = ['stars']

#Convert the dataframe into numpy arrays for use with sklearn
data = np.array(df_reviews[X_var])
target = np.array(df_reviews[y_var])
target = np.ravel(target)


#Fit the data to the Random Forest Regressor
clf = RandomForestRegressor(min_samples_leaf=200)
clf = clf.fit(data, target)


#Store the instance using dill.
with open('latlong_file','w') as f:
    dill.dump(clf,f)
    

