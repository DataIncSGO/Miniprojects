# Author: Selma Gomez Orr <selmagomezorr@gmail.com> Copyright (C) January 5, 2016


##########################################################################
## Imports
##########################################################################

import os
import numpy as np
import pandas as pd
import sqlite3



    
##########################################################################
## Program 
##########################################################################
if __name__== "__main__":

    
    #Establish connection to sql database.
    con = sqlite3.connect("Restaurants")
    con.text_factory = str
    cur = con.cursor()
    
    #Question 1 of SQL 
    #Create a dataframe of the zipcodes, restaurant id's(camis), scores, and inspection date for sorting to get most recent.
    df = pd.read_sql_query("SELECT camis, zipcode, score, inspdate FROM grades ORDER BY camis ASC, inspdate DESC", con)
    
    #For each unique restaurant get score information and zipcode for latest inspection.  Drop the rest of the columns.
    df = df.groupby('CAMIS', as_index=False).first()
    del df['INSPDATE'], df['CAMIS']
    
    #Convert scores to numeric values for aggregating for mean, std, and total count per zipcode.  Fill in 0's where no score is recorded.
    df['SCORE']=df['SCORE'].convert_objects(convert_numeric=True).fillna(0)
    df = df.groupby('ZIPCODE', as_index=False).agg(['mean', 'std', 'count'])
    
    #Level the dataframe to columns in one dimension instead of two and reset the index.
    df.columns = df.columns.get_level_values(1)
    df = df.reset_index()
    
    #Initialize the answer tuple.
    ANSWER1 = []
    
    #Get the required values for the answer tuple as computed above.  Get standard error from std.
    for i in df.index:
        if df.iloc[i,3]>100:
            tup1=(str(df.iloc[i,0]), df.iloc[i,1], df.iloc[i,2]/(df.iloc[i,3]**0.5), df.iloc[i,3])
            ANSWER1.append(tup1)

    print ANSWER1
    
    #Create a file for mapping zipcode values against mean and other statistics if desired.
    df_map = df.to_csv("Zip_Data.txt", index=False)
    
    
    
    #Question 2 of SQL 
  
    #Create a dataframe using the boro information to get similar statistics to above question.  Sort by inspection date.
    dfb = pd.read_sql_query("SELECT camis, boro, score, inspdate FROM grades ORDER BY camis ASC, inspdate DESC", con)
    
    #For each unique restaurant id (camis) take the first entry which includes score on most recent inspection.  Drop other columns.
    dfb = dfb.groupby('CAMIS', as_index=False).first()
    del dfb['INSPDATE'], dfb['CAMIS']
    
    #Convert scores to numeric values for aggregating for mean, std, and total count per zipcode.  Fill in 0's where no score is recorded.
    dfb['SCORE']=dfb['SCORE'].convert_objects(convert_numeric=True).fillna(0)
    dfb = dfb.groupby('BORO', as_index=False).agg(['mean', 'std', 'count'])
    
    #Level the dataframe to columns in one dimension instead of two and reset the index.  
    dfb.columns = dfb.columns.get_level_values(1)
    dfb = dfb.reset_index()
    
    #Create dict with boro names
    boro_names = {"1": "MANHATTAN", "2": "THE BRONX", "3": "BROOKLYN", "4": "QUEENS", "5": "STATEN ISLAND"}
    
    #Initialize the answer tuple.
    ANSWER2 = []
    
    #Get the required values for the answer tuple as computed above.  Get standard error from std.
    for i in dfb.index:
        if dfb.iloc[i,0] in ["1", "2", "3", "4", "5"]:
            tup2=(boro_names[dfb.iloc[i,0]], dfb.iloc[i,1], dfb.iloc[i,2]/(dfb.iloc[i,3]**0.5), dfb.iloc[i,3])
            ANSWER2.append(tup2)
            
    print ANSWER2
    

    #Question 3 of SQL
    
    #Create a dataframe with cuisine information from an inner join of tables.
    dfc = pd.read_sql_query("SELECT codedesc, score FROM cuisines AS C JOIN grades AS G ON C.CUISINECODE=G.CUISINECODE", con)
    
    #Conver scores to numeric values for aggregating for mean, std, and count per cuisine.
    dfc['SCORE']=dfc['SCORE'].convert_objects(convert_numeric=True).fillna(0)
    dfc = dfc.groupby('CODEDESC', as_index=False).agg(['mean', 'std', 'count'])
    
    #Level the dataframe to columns in one dimension instead of two and reset the index.
    dfc.columns = dfc.columns.get_level_values(1)
    dfc = dfc.reset_index()

    #Initialize the answer tuple.
    ANSWER3 = []
    
   #Get the required values for he answer tuple as computed above.  Get standard error from std. 
    count = 0
    for i in dfc.index:
        if dfc.iloc[i,3]>100:
            tup3=(dfc.iloc[i,0], dfc.iloc[i,1], dfc.iloc[i,2]/(dfc.iloc[i,3]**0.5), dfc.iloc[i,3])
            ANSWER3.append(tup3)
            count = count + 1
     
    print ANSWER3
    print count
    
   
   
   
   
   
    con.close





