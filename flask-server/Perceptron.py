# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 13:42:15 2023

@author: tks
"""

import pandas as pd
from sklearn.linear_model import Perceptron

def main(train_data_name = "animal_combos_train.csv",test_data_name = 'animal_combos_test.csv'):
    train_data=pd.read_csv(train_data_name)
    test_data=pd.read_csv(test_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    x=test_data.iloc[:,1:] 
    
    #setting model
    model = Perceptron(random_state=42)
    model.fit(train_x, train_y)
    
    # prediction
    y_pred = model.predict(x)
    weight = model.coef_[0]
    return y_pred