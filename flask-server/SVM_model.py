# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 13:16:44 2023

@author: GRIPS
"""
import pandas as pd
from sklearn.svm import SVC

# setting dataset
train_data_name = "animal_combos_train.csv";test_data_name = "animal_combos_test.csv"

#input data
train_data=pd.read_csv(train_data_name)
test_data = pd.read_csv(test_data_name)
#split data
train_y=train_data.iloc[:,-1]
train_x=train_data.iloc[:,1:-1] 
test_x=test_data.iloc[:,1:]
#get_combo
combo_names=list(test_x.columns)
row_names=list(test_data.iloc[:,0])
#setting model
model = SVC(kernel='linear', random_state=42,probability=True)
# learning
model.fit(train_x, train_y)

# prediction
y_pred = model.predict(test_x)
score = model.predict_proba(test_x)[:,1]

prediction_disctionary_list=[]
for (k,v) in enumerate(row_names):
    dictionary={}
    dictionary["Row"]=row_names[k]
    dictionary["Score"]=score[k]
    dictionary["Predict"]=y_pred[k]
    prediction_disctionary_list.append(dictionary)