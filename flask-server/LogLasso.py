# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 11:48:26 2023

@author: Molly

Logistic Lasso Regression using sklearn library
"""


from sklearn.linear_model import LogisticRegression
from sklearn.svm import l1_min_c
import pandas as pd



#load in training and testing data
X_train=pd.read_csv("matrix_format.csv")
X_test=pd.read_csv("matrix_format_test.csv")
original_train_data=pd.read_csv("animals_train.csv")
y_train=original_train_data.iloc[:,-1]


#convert data to np, not sure if this is necessary
X_train=X_train.to_numpy()
X_train=X_train[:,1:] #removing animal name column

y_train=y_train.to_numpy()

X_test=X_test.to_numpy()
X_test=X_test[:,1:] #removing animal name column



#finding minimum acceptable C
min_C=l1_min_c(X_train,y_train,loss="log")
print(f"minimum acceptable C= {min_C}")
#min C=.045


#large C=denser beta, small C = sparser beta
model=LogisticRegression(penalty="l1",C=1,solver="liblinear",random_state=0) #sets random state for reproducability
#model=LogisticRegression(penalty="l1",C=1,solver="saga",random_state=0) #sets random state for reproducability



classifier=model.fit(X_train,y_train)

print(classifier.predict(X_test))

print(classifier.predict_proba(X_test))

print(classifier.coef_)
coef=classifier.coef_