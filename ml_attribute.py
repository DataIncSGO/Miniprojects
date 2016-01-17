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
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
from sklearn.pipeline import Pipeline

##########################################################################
## Constants
##########################################################################

url = "http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_business.json.gz"


##########################################################################
## Program - Miniproject: ml Attribute Model
##########################################################################

#Download file
urllib.urlretrieve(url,'Reviews')

reviews_list = []
with gzip.open('Reviews', 'rb') as f:
    for line in f:
        review = ujson.loads(line)
        reviews_list.append(review)
        
#Get data and target from dataframe and convert to format for sklearn.
df_reviews = pd.DataFrame(reviews_list)
target = np.array(df_reviews['stars'])
target = np.ravel(target)
print len(target)

#Transform the data.
data = []

for review in reviews_list:
    attr_rec={}
    for item in review['attributes']:
        if type(review['attributes'][item])!= dict:
            if type(review['attributes'][item])==int:
                attr_rec[item]=review['attributes'][item]
            if review['attributes'][item]== True:
                attr_rec[item]=1
            if review['attributes'][item]==False:
                attr_rec[item]=0
            if type(review['attributes'][item])==unicode and review['attributes'][item]!='no':
                attr_rec[item+'_'+ review['attributes'][item]]=1
        else:
            for element in review['attributes'][item]:
                if type(review['attributes'][item][element])==int:
                    attr_rec[item + '_' + element]=review['attributes'][item][element]
                if review['attributes'][item][element]== True:
                    attr_rec[item + '_' + element]=1
                if review['attributes'][item][element]==False:
                    attr_rec[item + '_' + element]=0
                if type(review['attributes'][item][element])==unicode and review['attributes'][item][element]!='no':
                    attr_rec[item+'_'+ review['attributes'][item]+'_'+ element]=1       
    data.append(attr_rec)
print len(data)

#Regular linear regression model.
att_clf = Pipeline([
        ('vec', DictVectorizer()),
        ('regr', linear_model.LinearRegression())
    ])

att_clf = att_clf.fit(data, target)

#Store the instance using dill.
with open('att_file','w') as f:
    dill.dump(att_clf,f)
    
    
