# Author: Selma Gomez Orr <selmagomezorrds@gmail.com> January 15, 2016

##########################################################################
## Imports
##########################################################################


#imports
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
## Program - Miniproject: ml Category Model
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

#Transform the data
data = []

for review in reviews_list:
    cat_dict={}
    for category in review['categories']:
        cat_dict[category]=1
    data.append(cat_dict)
    
#Regular linear regression model.
cat_clf = Pipeline([
        ('vec', DictVectorizer()),
        ('TF-IDF', TfidfTransformer()),
        ('regr', linear_model.ElasticNetCV(n_alphas = 5, l1_ratio = [.1, .3, .5, .7, .9], cv=KFold(5), n_jobs = -1))
    ])

cat_clf = cat_clf.fit(data, target)


#Store the instance using dill.
with open('cat_file','w') as f:
    dill.dump(cat_clf,f)
    
