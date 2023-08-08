# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 13:16:44 2023

@author: GRIPS
"""
import pandas as pd
import numpy as np
from sklearn.svm import SVC
import pickle


def weights(train_data_name):
    #input data
    train_data=pd.read_csv(train_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    #get_combo
    combo_names=list(train_x.columns)
    #setting model
    model = SVC(kernel='linear', random_state=42,probability=True)
    # learning
    model.fit(train_x, train_y)

    # prediction
    weight = list(model.coef_[0])
    nonzero_weight_indices = np.nonzero(weight)[0]
    weight_dictionary_list=[]
    for i in nonzero_weight_indices:
        dictionary={}
        dictionary["Feature Combination"]=combo_names[i]
        dictionary["Weight"]=weight[i]
        weight_dictionary_list.append(dictionary)

    filename="SVM_model.sav"
    pickle.dump(model, open(filename,'wb'))

    return weight_dictionary_list


def predictions(test_data_name):

    #input data

    test_data = pd.read_csv(test_data_name)
    #split data
    test_x=test_data.iloc[:,1:]
    #get_combo
    combo_names=list(test_x.columns)
    row_names=list(test_data.iloc[:,0])
    #setting model
    # # learning
    model=pickle.load(open("SVM_model.sav",'rb'))

    # prediction
    y_pred = model.predict(test_x)
    score = model.predict_proba(test_x)[:,1]

    prediction_disctionary_list=[]
    for (k,v) in enumerate(row_names):
        dictionary={}
        dictionary["Data"]=row_names[k]
        dictionary["Score"]=score[k]
        dictionary["Prediction"]=float(y_pred[k])
        prediction_disctionary_list.append(dictionary)

    return prediction_disctionary_list