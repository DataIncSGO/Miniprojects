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
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import linear_model
from sklearn.cross_validation import KFold
from sklearn.pipeline import Pipeline



##########################################################################
## Constants
##########################################################################

url = "http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_business.json.gz"

##########################################################################
## Program - Miniproject: ml Full Model
##########################################################################

#Download file
urllib.urlretrieve(url,'Reviews')

reviews_list = []
with gzip.open('Reviews', 'rb') as f:
    for line in f:
        review = ujson.loads(line)
        reviews_list.append(review)
        


#Load all of the estimators.

estimator = dill.load(open('est_file', 'r'))

clf = dill.load(open('latlong_file', 'r'))

cat_clf = dill.load(open('cat_file', 'r'))

att_clf = dill.load(open('att_file', 'r'))


#Get the X values by computing estimate for each record.

def get_estimates(record):
    
    temp_dict={}
    
    city_est = round(estimator.predict(record),2)
    temp_dict['city']=city_est

    record_arr = (record['latitude'], record['longitude'])
    answer_latlong = clf.predict(record_arr)
    latlong_est = round(answer_latlong[0],2)
    temp_dict['latlong']=latlong_est

    record_dict={}
    for category in record['categories']:
        record_dict[category]=1
    answer_cat = cat_clf.predict(record_dict)
    cat_est = round(answer_cat[0],2)
    temp_dict['cat']=cat_est


    data=[]
    attr_rec={}
    for item in record['attributes']:
        if type(record['attributes'][item])!= dict:
            if type(record['attributes'][item])==int:
                attr_rec[item]=record['attributes'][item]
            if record['attributes'][item]== True:
                attr_rec[item]=1
            if record['attributes'][item]==False:
                attr_rec[item]=0
            if type(record['attributes'][item])==unicode and record['attributes'][item]!='no':
                attr_rec[item+'_'+ record['attributes'][item]]=1
        else:
            for element in record['attributes'][item]:
                if type(record['attributes'][item][element])==int:
                    attr_rec[item + '_' + element]=record['attributes'][item][element]
                if record['attributes'][item][element]== True:
                    attr_rec[item + '_' + element]=1
                if record['attributes'][item][element]==False:
                    attr_rec[item + '_' + element]=0
                if type(record['attributes'][item][element])==unicode and record['attributes'][item][element]!='no':
                    attr_rec[item+'_'+ record['attributes'][item]+'_'+ element]=1       
    data.append(attr_rec)
    answer_att = att_clf.predict(attr_rec)
    att_est = round(answer_att[0],2)
    temp_dict['att']=att_est
    
    return temp_dict


#Get Y values and convert to format for sklearn.
df_reviews = pd.DataFrame(reviews_list)
y_val = np.array(df_reviews['stars'])
y_val = np.ravel(y_val)


#Get X values.

est_list=[]
for record in reviews_list:
    est_list.append(get_estimates(record))
    
df_estimates = pd.DataFrame(est_list)
X_val = np.array(df_estimates)

#Get estimator
full_clf = linear_model.Ridge(alpha=0.5)
full_clf= full_clf.fit(X_val, y_val)

#Store the instance using dill.
with open('full_file','w') as f:
    dill.dump(full_clf,f)
