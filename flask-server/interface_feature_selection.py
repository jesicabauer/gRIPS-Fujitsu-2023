# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:06:44 2023

@author: Molly

Based on: Satoshi Hara and Takanori Maehara. Finding alternate features in lasso. arXiv preprint arXiv:1611.05940, 2016.

"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
import json



#############################################################
def prox(x,alpha): #proximal operator for absolute value function (for proximal gradient descent step) 
    return  np.sign(x)*max(0,abs(x)-alpha)

#########################################################################

#returns True if the optimal nonzero value of beta j is zero after setting beta i to 0 (can't switch beta j and beta i)
def optimal_betaj_zero(combo_mat,beta_star, intercept,y_vect, C, j, out_index):
    alpha=0.1 #constant step size for gradient descent step

    sigmoid=nn.Sigmoid() #function for calculating the prediction score
    loss=nn.BCELoss(reduction='sum') #adds loss for each term, doesn't take average
    beta_j=torch.tensor(0.0,requires_grad=True) #initialize beta_j as 0
    optimizer=optim.SGD(params=[beta_j],lr=alpha) #gradient descent with step size alpha
    
    m=combo_mat.shape[0] #number of training samples    
    n=combo_mat.shape[1] #number of combinations

    intercept_vect=torch.ones(m)*intercept #for adding intercept(beta0) to each prediction
    
    combo_mat=torch.from_numpy(combo_mat) #convert from np array to tensor
    y_vect=torch.from_numpy(y_vect) #convert from np array to tensor
    y_vect=y_vect.to(torch.float32) #converts tensor to float32 data type

    #calculate z_j vector based on beta_star and the out index
    z_j=torch.zeros(m)
    for k in range(n):
        if k!=out_index:
            z_j+=beta_star[k]*combo_mat[:,k] #k-th column 
    z_j+=intercept_vect
    
    #gets the next temp beta_j based on gradient descent (just from the logistic loss function)
    optimizer.zero_grad()   
    temp=beta_j*combo_mat[:,j]+z_j
    y_hat_vect=sigmoid(temp)
    l=C*loss(y_hat_vect,y_vect) #first term in the objective function (logistic loss with hyperparameter C)
    l.backward() #calculates gradient of the first term in the objective 
    
    #check to see if optimal beta is 0 based on the optimality condition
    if abs(beta_j.grad.data)<=1:
        return True
    else:
        return False
    
#########################################################################

#given a zero beta_j and a nonzero beta_i, gives the best nonzero beta_j when beta_i is set to 0
def nonzero_betaj(combo_mat,beta_star,intercept,y_vect,C,j,out_index):
    
    alpha=.1 #step size
    total_iterations=1000 #max num of iterations (if convergence is not reached sooner)
    
    sigmoid=nn.Sigmoid() #function to calculate prediction scores
    loss=nn.BCELoss(reduction='sum') #adds loss for each term, doesn't take average
    beta_j=torch.tensor(0.0,requires_grad=True) #initialize beta_j as 0
    optimizer=optim.SGD(params=[beta_j],lr=alpha) #gradient descent with step size alpha 
    
    m=combo_mat.shape[0] #num training samples    
    n=combo_mat.shape[1] #num combinations

    intercept_vect=torch.ones(m)*intercept  #for adding intercept(beta0) to each prediction
    
    combo_mat=torch.from_numpy(combo_mat) #convert from np array to tensor
    y_vect=torch.from_numpy(y_vect)  #convert from np array to tensor
    y_vect=y_vect.to(torch.float32)
    
    #calculate z_j vector based on beta_star and the out index
    z_j=torch.zeros(m)
    for k in range(n):
        if k!=out_index:
            z_j+=beta_star[k]*combo_mat[:,k] #k-th column 
    z_j+=intercept_vect
    
    #find optimal beta_j using proximal gradient descent
    for iter in range(total_iterations):  #max number of iterations if stopping criteria is not reached
        beta_j_old=beta_j.data.item() #gets old beta j to use in stopping criteria
        optimizer.zero_grad()   
        temp=beta_j*combo_mat[:,j]+z_j
        y_hat_vect=sigmoid(temp)
        l=C*loss(y_hat_vect,y_vect) #logistic loss term in objective with hyperparameter C
        l.backward()
        optimizer.step()
        temp_beta_j=beta_j.data.detach().clone() #beta from gradient descent
        beta_j.data=prox(temp_beta_j,alpha) 
        
        if abs(beta_j.item()-beta_j_old)<10e-4: #stopping condition
            break

    #calculating objective value with new beta_j
    temp=beta_j*combo_mat[:,j]+z_j
    y_hat_vect=sigmoid(temp)
    objective_val=C*loss(y_hat_vect,y_vect)
    for k in range(n):
        if k!=out_index:
            objective_val+=abs(beta_star[k])
    objective_val+=abs(beta_j.item())
    
    return beta_j.data,objective_val #new weights and their associated objective value

##########################################################################################################################

#Regular Lasso to find beta star, returns predictions and their probabilities, and classifier that contains the weights
def optimal_Lasso(X_train,y_train):
    C_val=20
    n_nonzero=101
    while n_nonzero>100:
        C_val=C_val*.9  #large C=denser beta, small C=sparser beta
       
        model=LogisticRegression(penalty="l1",C=C_val,solver="liblinear",random_state=0) #sets random state for reproducability
        
        classifier=model.fit(X_train,y_train) #fit model and display results
        
        #get coefficients
        original_coef=classifier.coef_[0].copy()
        nonzero_weight_indices=np.nonzero(original_coef)[0]
        n_nonzero=len(nonzero_weight_indices)
    
    print(f"# of nonzero weights={n_nonzero} with C value {C_val}")
    
    intercept=classifier.intercept_
    
    return classifier,original_coef,intercept,C_val


#############################################################################################################

#given a list of model coefficients, gives a list of the zero betaj's that can be put in the model
def acceptable_beta_j(original_coef,intercept,C_val,X_train, y_train):
    combo_names=list(X_train.columns)
    cant_insert_betajs=[] #initialize list that keeps track of zero weight beta_j that can't be added to the model
    n_weights=len(original_coef)

    #get list of all the indices
    all_indices=[]
    for i in range(n_weights):
        all_indices.append(i)

    #lists of which indices are zero and nonzero
    nonzero_weight_indices=np.nonzero(original_coef)[0]
    zero_weight_indices=np.setdiff1d(all_indices,nonzero_weight_indices)
        
    #looping through all of betas with 0 weights to check if they can be put in the model
    for in_idx in zero_weight_indices:
        cant_insert_beta=True
        for out_idx in nonzero_weight_indices: #looping through all nonzero betas that could potentially be replaced with the current beta_j
            #opt_betaj_zero is True if the optimal beta_j when replacing it with beta_i is zero
            opt_betaj_zero=optimal_betaj_zero(combo_mat=X_train.to_numpy(),beta_star=original_coef.copy(),intercept=intercept,y_vect=y_train.to_numpy(),C=C_val,j=in_idx,out_index=out_idx)
            if opt_betaj_zero==False: #if a nonzero betaj exists
                cant_insert_beta=False
                break
        if cant_insert_beta:
            cant_insert_betajs.append(in_idx)
    
    acceptable_in_idx=np.setdiff1d(zero_weight_indices,cant_insert_betajs) #gets indices of feature combinations that can be put in the model
    
    features_to_add=[]
    for i in acceptable_in_idx:
        features_to_add.append(combo_names[i])
    print(features_to_add)
    return features_to_add        

##############################################################################################


#given a betaj to insert in the model, adds best beta_j to coefficient list and sets the best beta_i to 0
def new_coef_list(original_coef,X_train,y_train,intercept,C_val,in_idx,user_feature_list):
    nonzero_weight_indices=np.nonzero(original_coef)[0]
    
    #to store the new betas and corresponding objective values
    new_beta_dict={}
    obj_val_dict={}
    out_idx_nonzero_beta=[]
    
    #get new beta_j for each nonzero i index that could be switched out, then compare objective values for the new betas
    for out_idx in nonzero_weight_indices:
        if out_idx not in user_feature_list: #makes sure any feature combinations already added by the user are not taken out of the model
            new_betaj,obj_val=nonzero_betaj(combo_mat=X_train.to_numpy(),beta_star=original_coef.copy(),intercept=intercept,y_vect=y_train.to_numpy(),C=C_val,j=in_idx,out_index=out_idx)
            new_beta_dict[out_idx]=new_betaj.item()
            if new_betaj.item()!=0:    
                obj_val_dict[out_idx]=obj_val.item() #dictionary of objective values for nonzero betas
                out_idx_nonzero_beta.append(out_idx)
    
    if len(obj_val_dict)==0: #users should only have the option to pick a beta where this won't happen
        print("ERROR, new beta values are zero, cannot put this feature combination into the model")
        return original_coef
    
    #finding the feature combination beta_i to be taken out of the model that results in the smallest change in the objective value
    min_out_idx=out_idx_nonzero_beta[0]
    min_obj_val=obj_val_dict[min_out_idx]
    for idx in out_idx_nonzero_beta:
        if obj_val_dict[idx]<min_obj_val:
            min_obj_val=obj_val_dict[idx]
            min_out_idx=idx
    
    #replacing the old beta i and beta j with the new ones
    new_betas=original_coef.copy()
    new_betas[min_out_idx]=0
    new_betas[in_idx]=new_beta_dict[min_out_idx]

    return new_betas, min_out_idx #new betas after switching beta j and beta i, index i (feature combination removed from the model)

#####################################################################

def interface_feature_selection(in_combo,current_coef,user_feature_indices,X_train, y_train, intercept, C_val):
    print("in interface_feature_selection function")
    combo_names=list(X_train.columns)
    in_idx=combo_names.index(in_combo)
    current_coef,out_idx=new_coef_list(current_coef,X_train,y_train,intercept,C_val,in_idx,user_feature_indices)
    user_feature_indices.append(in_idx)
    print("end of interface_feature_selection function")
    
    return current_coef.copy(),out_idx,user_feature_indices #updated model weights, list of feature combinations already added by the user

#################################################################################################################


def interface_weights(coef,out_idx,X_train):
    new_coef=coef.copy()
    nonzero_weight_indices=np.nonzero(new_coef)[0]
    combo_names=list(X_train.columns)
    
    #saving updated nonzero weights as a list of dictionaries
    weight_dictionary_list=[]
    for i in nonzero_weight_indices:
        dictionary={}
        dictionary["Combo"]=combo_names[i]
        dictionary["Weight"]=new_coef[i]
        dictionary["Old"]=False #only True for the beta i that was just removed from the model
        weight_dictionary_list.append(dictionary)
    
    #adding dictionary for the beta i that was removed from the model
    dictionary={}
    dictionary["Combo"]=combo_names[out_idx]    
    dictionary["Weight"]=0
    dictionary["Old"]=True
    weight_dictionary_list.append(dictionary)
    
    return weight_dictionary_list


#################################################################################################################

def interface_predictions(X_test,classifier,current_coef):
    test_row_names=list(X_test.iloc[:,0])
    X_test=X_test.iloc[:,1:] #removing first column (row names)
    #making the predictions
    classifier.coef_[0]=current_coef.copy() #changing the coefficients in the model to the new ones from user feature selection
    predictions=classifier.predict(X_test)
    probs=classifier.predict_proba(X_test)
    
    #saving predictions for each testing data point in a list of dictionaries
    pred_dictionary_list=[]
    for i in range(len(test_row_names)):
        dictionary={}
        dictionary["Row"]=test_row_names[i]
        dictionary["Score"]=probs[i,1]
        dictionary["Prediction"]=predictions[i]
        pred_dictionary_list.append(dictionary)
    
    return pred_dictionary_list


######################################## USER INTERFACE INPUTS AND OUTPUTS #################################################################


# train_combo_data="animal_combos_train.csv"
# test_combo_data="animal_combos_test.csv"
# in_combo="Flies_Does"

def main(train_combo_data):
    print("in interface_feature_selection file")
    #preparing training data
    X_train=pd.read_csv(train_combo_data)
    y_train=X_train.iloc[:,-1]
    X_train=X_train.iloc[:,1:-1] #removing row name column and label column

    #gets the Lasso classifier and list of weights (betas)
    classifier,current_coef,intercept,C_val=optimal_Lasso(X_train,y_train)

    #gives list of combinations that can be added to the model
    acceptable_combinations=acceptable_beta_j(current_coef,intercept,C_val,X_train, y_train)

    # combo_names=list(X_train.columns)
    # selectable_features = {}
    # selectable_features["selectable_features"] = []
    # for coef in list(current_coef):
    #     if coef == 0:
    #         print(coef)
    #         # selectable_features["selectable_features"].append(combo_names[index])
    
    return acceptable_combinations

def after_selection(train_combo_data, selected_feature, already_addeded):
    print("in after_selection function")
    #preparing training data
    X_train=pd.read_csv(train_combo_data)
    y_train=X_train.iloc[:,-1]
    X_train=X_train.iloc[:,1:-1] #removing row name column and label column

    #gets the Lasso classifier and list of weights (betas)
    classifier,current_coef,intercept,C_val=optimal_Lasso(X_train,y_train)

    current_coef,out_idx,user_feature_indices=interface_feature_selection(selected_feature,current_coef,already_addeded,X_train, y_train, intercept,C_val)

    acceptable_combinations=acceptable_beta_j(current_coef,intercept,C_val,X_train, y_train)

    # json_file = open("step5_feature_selection_data.json")
    # fetch_step5_json = json.load(json_file)
    # json_file.close()
    
    print("before new_step5_json??")
    new_step5_json = [{
        "current_coef": list(current_coef),
        "user_added": user_feature_indices,
        "selectable_features": acceptable_combinations
    }]
    json_model_data = json.dumps(new_step5_json)
    with open("step5_feature_selection_data.json", "w") as outfile:
        outfile.write(json_model_data)

    print("new_json", new_step5_json)

    weight_dict_list=interface_weights(current_coef,out_idx,X_train)

    print("here??")

    return weight_dict_list


if __name__ == "__main__":
    main("animal_combos_train.csv")
    # #maximum number of feature combination switches (number of nonzero weights in the original model)
    # nonzero_weight_indices=np.nonzero(current_coef)[0]


    # ################## in loop for set number of feature combination switches  ###################################################

    # #gives list of combinations that can be added to the model
    # acceptable_combinations=acceptable_beta_j(current_coef,intercept,C_val,X_train)

    # #keeps track of which combos the user has added so they are not taken out at the next iteration
    # user_feature_indices=[]

    # #does the feature switch, gives list of updated coefficients
    # current_coef,out_idx,user_feature_indices=interface_feature_selection(in_combo,current_coef,user_feature_indices,X_train)

    # #returns list of dictionaries for the model weights
    # weight_dict_list=interface_weights(current_coef,out_idx,X_train)

    # #####################################################################



    # #preparing testing data
    # X_test=pd.read_csv(test_combo_data)
    # X_test=X_test.iloc[:,1:] #removing first column (row names)

    # #returns list of dictionaries for the prediction scores and classes
    # pred_dict_list=interface_predictions(X_test,classifier,current_coef)

