# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 11:48:26 2023

@author: Molly

Logistic Lasso Regression using sklearn library
"""


from sklearn.linear_model import LogisticRegression
from sklearn.svm import l1_min_c
import pandas as pd
import numpy as np



#load in training and testing data
X_train=pd.read_csv("animal_combos_train.csv")
X_test=pd.read_csv("animal_combos_test.csv")

#gets lists of names of rows and columns
train_row_names=list(X_train.iloc[:,0])
test_row_names=list(X_test.iloc[:,0])


#get training label vector and remove unnecessary columns
y_train=X_train.iloc[:,-1]
X_train=X_train.iloc[:,1:-1] #removing animal name column and label column
X_test=X_test.iloc[:,1:] #removing animal name column

#list of all combinations
combo_names=list(X_test.columns)


#finding minimum acceptable C
min_C=l1_min_c(X_train,y_train,loss="log")
print(f"minimum acceptable C= {min_C}")


C_val=20
n_nonzero=101


while n_nonzero>100:
    C_val=C_val*.9

    #large C=denser beta, small C = sparser beta
    model=LogisticRegression(penalty="l1",C=C_val,solver="liblinear",random_state=0) #sets random state for reproducability
    #model=LogisticRegression(penalty="l1",C=1,solver="saga",random_state=0) #saga isn't converging with these default parameters
    
    #fit model and display results
    classifier=model.fit(X_train,y_train)
    
    #get coefficients
    coef=classifier.coef_[0]
    nonzero_weight_indices=np.nonzero(coef)[0]
    n_nonzero=len(nonzero_weight_indices)
    #print(f"# of nonzero weights={n_nonzero} with C value {C_val}")

    
print(f"# of nonzero weights={n_nonzero} with C value {C_val}")

#save results
predictions=classifier.predict(X_test)
probs=classifier.predict_proba(X_test)
intercept=classifier.intercept_

#display results

#predictions
for i in range(len(test_row_names)):
    print(f"{test_row_names[i]} predicted as {predictions[i]} score={probs[i,1]}")
    

#important combinations are their weights
print(f"number of nonzero weights={len(nonzero_weight_indices)}")
for i in nonzero_weight_indices:
    #print(f"{combo_names[i]   }    weight: {coef[i]}")
    print(combo_names[i])
    print(f"weight: {coef[i]}")



print(f"intercept= {intercept}")


#print(f"prediction score if all important combos are zero (just intercept): {1/(1+np.exp(-intercept))}")



dictionary_list=[]
for i in nonzero_weight_indices:
    dictionary={}
    dictionary["Important_combo"]=combo_names[i]
    dictionary["Weight"]=coef[i]
    dictionary_list.append(dictionary)
        
    
with open("animal_weights.txt", "w") as output:
    output.write(str(dictionary_list))


pred_dictionary_list=[]

for i in range(len(test_row_names)):
    dictionary={}
    dictionary["Animal"]=test_row_names[i]
    dictionary["Score"]=probs[i,1]
    dictionary["Prediction"]=predictions[i]
    pred_dictionary_list.append(dictionary)

with open("animal_predictions.txt", "w") as output:
    output.write(str(pred_dictionary_list))

























    


