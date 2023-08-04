# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 13:42:34 2023

@author: GRIPS
"""
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB

# setting dataset
# train_data_name = "animal_combos_train.csv";test_data_name = "animal_combos_test.csv"


def predictions(test_data_name):
    #input data
    train_data=pd.read_csv("binary_combo_data.csv")
    test_data = pd.read_csv(test_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    test_x=test_data.iloc[:,1:]
    #get_combo
    combo_names=list(test_x.columns)
    row_names=list(test_data.iloc[:,0])
    #setting model
    model = GaussianNB(var_smoothing=1e-9)
    # learning
    model.fit(train_x, train_y)
    # prediction
    y_pred = model.predict(test_x)
        
    prediction_disctionary_list=[]

    for (k,v) in enumerate(row_names):
        dictionary={}
        dictionary["Data"]=row_names[k]
        dictionary["Prediction"]=float(y_pred[k])
        prediction_disctionary_list.append(dictionary)

    return prediction_disctionary_list


