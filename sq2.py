# Author: Selma Gomez Orr <selmagomezorr@gmail.com> Copyright (C) January 7, 2016


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

    
    #Establish connection to database. 
    con = sqlite3.connect("Restaurants")
    con.text_factory = str
    cur = con.cursor()

    #Create a dataframe from the inner join of the violation table and cuisine table.  Violations limited by date.
    dfv = pd.read_sql_query("SELECT violationdesc, codedesc FROM (SELECT violationcode, violationdesc FROM violations WHERE enddate >= '2014-01-01 00:00:00') AS V INNER JOIN (SELECT violcode, codedesc FROM cuisines AS C JOIN grades AS G WHERE C.CUISINECODE = G.CUISINECODE) AS D WHERE V.VIOLATIONCODE=D.VIOLCODE", con)
    
    #Create a working copy of the dataframe.
    hold = dfv
    
    #Get the total count for each violation cuisine pair to be used in calculating the joint and conditional probabilities.
    inter = hold.groupby(['violationdesc', 'codedesc']).size().reset_index()
    inter.columns = ['violationdesc', 'codedesc', 'tot']

    #Get total number of data points for probability computations
    Total = inter.sum(axis=0)[2]

    #Create a dict with the unconditional probabilities of the violations.
    viol_prob = inter.groupby('violationdesc', as_index=False).sum()
    viol_prob['prob']=viol_prob['tot']/Total
    viol_dict = {}
    for v in viol_prob.index:
        viol = viol_prob.iloc[v,0]
        viol_dict[viol]= viol_prob.iloc[v,2]

    #Create a dict with the unconditional probabilities of the cuisines.
    cuis_prob = inter.groupby('codedesc', as_index=False).sum()
    cuis_prob['c_prob']=cuis_prob['tot']/Total
    cuis_dict = {}
    for c in cuis_prob.index:
        cuis = cuis_prob.iloc[c,0]
        cuis_dict[cuis]= cuis_prob.iloc[c,2]

    #Create a column with the joint probability of each violation & cuisine pair.
    joint_prob = pd.DataFrame(inter)
    joint_prob['Jt_Prob']=joint_prob['tot']/Total


    #Initialize list to hold answer tuples
    ANSWER4 = []
    
    #Initialize counts to verify results.
    count = 0
    sum=0 


    #Create list of tuples with required answer of cuisine, violation, ratio, and count.  Limit counts above 100.
    for j in joint_prob.index:
        if joint_prob.iloc[j,2]>100:
            ratio = (joint_prob.iloc[j,3]/cuis_dict[joint_prob.iloc[j,1]])/viol_dict[joint_prob.iloc[j,0]]
            tup4=((joint_prob.iloc[j,1], joint_prob.iloc[j,0]), ratio, joint_prob.iloc[j,2])
            if ratio>=1.87:
                ANSWER4.append(tup4)
                count +=1
                sum+=ratio
 

    #Print answer and cross-check values.   
    print ANSWER4
    print count
    print sum
    print sum/count
    
    
    #Close the connection to sql database.
    con.close
    

