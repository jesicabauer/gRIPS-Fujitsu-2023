# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 12:06:40 2023
@author: GRIPS
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

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
#setting model
model = DecisionTreeClassifier(max_depth = 10, random_state=42)
# learning
model.fit(train_x, train_y)
# prediction
y_pred = model.predict(test_x)

weight = list(model.feature_importances_)
nonzero_weight_indices = np.nonzero(weight)[0]
weight_dictionary_list=[]
for i in nonzero_weight_indices:
    dictionary={}
    dictionary["Combo"]=combo_names[i]
    dictionary["Weight"]=weight[i]
    weight_dictionary_list.append(dictionary)