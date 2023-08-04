import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from numpy.polynomial.polynomial import Polynomial
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pickle

def weights(train_data):

    # train_data = pd.DataFrame(train_data)
    # test_data = pd.DataFrame(test_data)
    
    train_data=pd.read_csv(train_data)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    # x=test_data.iloc[:,1:] 

    #train the model
    C_val=20
    n_nonzero=101
    while n_nonzero>100:
        C_val=C_val*.9  #large C=denser beta, small C=sparser beta
       
        model=LogisticRegression(penalty="l1",C=C_val,solver="liblinear",random_state=0) #sets random state for reproducability
        
        classifier=model.fit(train_x,train_y) #fit model
        
        #get coefficients
        original_coef=classifier.coef_[0].copy()
        nonzero_weight_indices=np.nonzero(original_coef)[0]
        n_nonzero=len(nonzero_weight_indices)


    # nonzero_weight_indices = np.nonzero(original_coef)
    weight_dictionary_list=[]
    for i in nonzero_weight_indices:
        dictionary={}
        # print(nonzero_weight_indices[0])
        dictionary["Feature Combination"]=list(train_x.columns)[i]
        dictionary["Weight"]=original_coef[i]
        weight_dictionary_list.append(dictionary)

    filename="lasso_model.sav"
    pickle.dump(classifier, open(filename,'wb'))

    return weight_dictionary_list
    

def predictions(test_data_name):
    #making the predictions
    # classifier.coef_[0]=current_coef.copy() #changing the coefficients in the model to the new ones from user feature selection
    test_in = pd.read_csv(test_data_name)
    test_row_names=list(test_in.iloc[:,0])
    X_test=test_in.iloc[:,1:] 

    print(X_test)

    classifier=pickle.load(open("lasso_model.sav",'rb'))

    predictions=classifier.predict(X_test)
    probs=classifier.predict_proba(X_test)
    
    
    
    #saving predictions for each testing data point in a list of dictionaries
    pred_dictionary_list=[]
    for i in range(len(test_row_names)):
        dictionary={}
        dictionary["Data"]=test_row_names[i]
        dictionary["Score"]=probs[i,1]
        dictionary["Prediction"]=int(predictions[i])
        pred_dictionary_list.append(dictionary)
    
    return pred_dictionary_list