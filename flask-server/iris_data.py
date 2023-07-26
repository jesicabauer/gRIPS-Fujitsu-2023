# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 11:18:28 2023

@author: Molly
"""

from sklearn.datasets import load_iris
import numpy as np

#load in data
all_data,all_targets=load_iris(return_X_y=True,as_frame=True)

#make labels binary and get list of all indices
all_indices=[]
for i in range(150):
    if all_targets[i]==2:
        all_targets[i]=0
    all_indices.append(i)
        
#select testing indices
testing_indices=np.random.choice(a=all_indices,size=30,replace=False)
training_indices=np.setdiff1d(all_indices, testing_indices)

#get test data and test labels
test_matrix=all_data.loc[testing_indices,:]
test_labels=all_targets[testing_indices]

#create training matrix with labels
train_matrix=all_data.loc[training_indices,:]
train_labels=all_targets[training_indices]

train_matrix.insert(loc=4,column="Label",value=train_labels)       


#save matrices as csv files

train_matrix.to_csv("iris_train.csv")
test_matrix.to_csv("iris_test.csv")