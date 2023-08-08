# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 12:03:02 2023

@author: GRIPS
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# setting dataset

def weights(train_data_name):
    print("in RF weights function")
    #input data
    train_data=pd.read_csv(train_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    #get_row & label
    combo_names=list(train_x.columns)
    #setting model
    model = RandomForestClassifier(n_estimators=1000, random_state=42)
    # learning
    model.fit(train_x, train_y)
    # prediction
    # get_weight
    weight = list(model.feature_importances_)
    nonzero_weight_indices = np.nonzero(weight)[0]
    #make_dictionary
    weight_dictionary_list=[]
    print(combo_names[-1])
    for i in nonzero_weight_indices:
        dictionary={}
        dictionary["Feature Combination"]=combo_names[i]
        dictionary["Weight"]=weight[i]
        weight_dictionary_list.append(dictionary)

    filename="RF_model.sav"
    pickle.dump(model, open(filename,'wb'))
    

    return weight_dictionary_list

def predictions(test_data_name):
    #input data
    test_data = pd.read_csv(test_data_name)
    print(test_data)
    #split data
    test_x=test_data.iloc[:,1:]
    #get_row & label
    combo_names=list(test_x.columns)
    row_names=list(test_data.iloc[:,0])
    #setting model

    model=pickle.load(open("RF_model.sav",'rb'))
    # learning
    # prediction
    y_pred = list(model.predict(test_x))

    score = list(model.predict_proba(test_x)[:,1])

    prediction_disctionary_list=[]
    for (k,v) in enumerate(row_names):
        dictionary={}
        dictionary["Data"]=row_names[k]
        dictionary["Score"]=score[k]
        dictionary["Prediction"]=float(y_pred[k])
        prediction_disctionary_list.append(dictionary)

    return prediction_disctionary_list


