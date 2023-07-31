# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:35:21 2023

@author: GRIPS
"""
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
def main(train_data_name = "animal_combos_train.csv",test_data_name = 'animal_combos_test.csv'):
     #input data
     train_data=pd.read_csv(train_data_name)
     test_data=pd.read_csv(test_data_name)
     #split data
     train_y=train_data.iloc[:,-1]
     train_x=train_data.iloc[:,1:-1] 
     x=test_data.iloc[:,1:] 
     
     #setting model
     model = KNeighborsClassifier()
     model.fit(train_x, train_y)
     y_pred = model.predict(x)
     #y_prob = model.predict_proba(x)
     return y_pred
