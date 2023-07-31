# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:19:52 2023

@author: GRIPS
"""
#ナイーブベイズ
import pandas as pd
from sklearn.naive_bayes import GaussianNB
 

def main(train_data_name = "animal_combos_train.csv",test_data_name = 'animal_combos_test.csv',max_depth=4):
    #input data
    train_data=pd.read_csv(train_data_name)
    test_data=pd.read_csv(test_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    x=test_data.iloc[:,1:] 
    
    model = GaussianNB()
    model.fit(train_x, train_y)
    y_pred = model.predict(x)
    #y_prob = model.predict_proba(x)
    return y_pred

main()