# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 11:25:44 2023

@author: GRIPS
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

# setting dataset
# train_data_name = "animal_combos_train.csv";test_data_name = "animal_combos_test.csv"
def weights(train_data_name):
    #input data
    train_data=pd.read_csv(train_data_name)
    # test_data = pd.read_csv(test_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    # test_x=test_data.iloc[:,1:]
    #get_combo
    # combo_names=list(test_x.columns)
    combo_names=list(train_x.columns)
    # row_names=list(test_data.iloc[:,0])
    #setting model
    model = LogisticRegression()
    # learning
    model.fit(train_x, train_y)
    # prediction
    # y_pred = model.predict(test_x)
    # score = model.predict_proba(test_x)[:,1]
    weight = list(model.coef_[0])
    nonzero_weight_indices = np.nonzero(weight)[0]
    weight_dictionary_list=[]
    for i in nonzero_weight_indices:
        dictionary={}
        dictionary["Feature Combination"]=combo_names[i]
        dictionary["Weight"]=weight[i]
        weight_dictionary_list.append(dictionary)

    filename="LR_model.sav"
    pickle.dump(model, open(filename,'wb'))

    return weight_dictionary_list
        
    # prediction_disctionary_list=[]

    # for (k,v) in enumerate(row_names):
    #     dictionary={}
    #     dictionary["Row"]=row_names[k]
    #     dictionary["Score"]=score[k]
    #     dictionary["Predict"]=y_pred[k]
    #     prediction_disctionary_list.append(dictionary)
    
def predictions(test_data_name):
    #input data
    # train_data=pd.read_csv(train_data_name)
    test_data = pd.read_csv(test_data_name)
    #split data
    # train_y=train_data.iloc[:,-1]
    # train_x=train_data.iloc[:,1:-1] 
    test_x=test_data.iloc[:,1:]
    #get_combo
    combo_names=list(test_x.columns)
    row_names=list(test_data.iloc[:,0])
    #setting model
    # model = LogisticRegression()
    # # learning
    # model.fit(train_x, train_y)
    model=pickle.load(open("LR_model.sav",'rb'))
    # prediction
    y_pred = model.predict(test_x)
    score = model.predict_proba(test_x)[:,1]
    # weight = list(model.coef_[0])
    # nonzero_weight_indices = np.nonzero(weight)[0]
    # weight_dictionary_list=[]
    # for i in nonzero_weight_indices:
    #     dictionary={}
    #     dictionary["Combo"]=combo_names[i]
    #     dictionary["Weight"]=weight[i]
    #     weight_dictionary_list.append(dictionary)
        
    prediction_disctionary_list=[]

    for (k,v) in enumerate(row_names):
        dictionary={}
        dictionary["Data"]=row_names[k]
        dictionary["Score"]=score[k]
        dictionary["Prediction"]=float(y_pred[k])
        prediction_disctionary_list.append(dictionary)

    return prediction_disctionary_list