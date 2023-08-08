# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:06:44 2023

@author: Molly

Satoshi Hara and Takanori Maehara. Finding alternate features in lasso. arXiv preprint arXiv:1611.05940, 2016.

"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
import time

def prox(x,alpha):
    return  np.sign(x)*max(0,abs(x)-alpha)


#given a zero betaj and a nonzero betai, gives the best nonzero betaj when betai=0
def nonzero_betaj(combo_mat,beta_star,intercept,y_vect,C,j,out_index):
    #inputs
    #combo_mat   binary matrix, m by n, m=train samples, n=num combos
    #beta_star   vector of optimal betas found by Lasso, size n
    #intercept=   #intercept from original Lasso output
    #y_vect  vector of training labels, size m
    #C  weight parameter from original Lasso problem
    #out_index_list  index i of nonzero beta to be removed, if list checks all of them and sees which one decreases the objective the most
    
    
    alpha=.1 #step size
    total_iterations=1000 #max num of iterations
    
    
    
    sigmoid=nn.Sigmoid()
    loss=nn.BCELoss(reduction='sum') #adds loss for each term, doesn't take average
    beta_j=torch.tensor(0.0,requires_grad=True) #initialize beta_j as 0
    optimizer=optim.SGD(params=[beta_j],lr=alpha) 
    
    m=combo_mat.shape[0] #num training samples    
    n=combo_mat.shape[1] #num combinations

    intercept_vect=torch.ones(m)*intercept
    
    combo_mat=torch.from_numpy(combo_mat) #convert from np array to tensor
    y_vect=torch.from_numpy(y_vect)
    y_vect=y_vect.to(torch.float32)

    
    #calculate z_j vector based on beta_star and the out index
    z_j=torch.zeros(m)
    for k in range(n):
        if k!=out_index:
            z_j+=beta_star[k]*combo_mat[:,k] #k column 
    z_j+=intercept_vect
    
    
    
    #find optimal beta_j
    for iter in range(total_iterations):  #max number of iterations if stopping criteria is not reached
    
    
        #gets old beta j to use in stopping criteria
        beta_j_old=beta_j.data.item()
        #gets the next temp beta_j based on gradient descent from just the BCE Loss
        optimizer.zero_grad()   
        temp=beta_j*combo_mat[:,j]+z_j
        y_hat_vect=sigmoid(temp)
        #y_hat_vect=sigmoid(beta_j*combo_mat[:,j]+z_j)
        l=C*loss(y_hat_vect,y_vect)
        l.backward()
        
        #####check to see if optimal beta is 0######
       
        if abs(beta_j.grad.data)<=1:
            #print("optimal beta j is 0")
            #print(f"beta= {beta_j.data}")
            break
        
        
        
        optimizer.step()
        temp_beta_j=beta_j.data.detach().clone() #beta from gradient descent
        beta_j.data=prox(temp_beta_j,alpha) 
    
        if abs(beta_j.item()-beta_j_old)<10e-4:
            #print(f"stopping criteria reached at iteration {iter}")
            break
   
    
    #calculating objective value with new beta_j
    temp=beta_j*combo_mat[:,j]+z_j
    y_hat_vect=sigmoid(temp)
    objective_val=C*loss(y_hat_vect,y_vect)
    for k in range(n):
        if k!=out_index:
            objective_val+=abs(beta_star[k])
    objective_val+=abs(beta_j.item())
    
    
    return beta_j.data,objective_val




##########################################################################################################################



#Regular Lasso to find beta star, returns predictions and their probabilities, and classifer that contains the weights
def optimal_Lasso(X_train,X_test,y_train):
    
    C_val=20
    n_nonzero=101
    while n_nonzero>100:
        C_val=C_val*.9
    
        #large C=denser beta, small C = sparser beta
        model=LogisticRegression(penalty="l1",C=C_val,solver="liblinear",random_state=0) #sets random state for reproducability
        
        #fit model and display results
        classifier=model.fit(X_train,y_train)
        
        #get coefficients
        original_coef=classifier.coef_[0].copy()
        nonzero_weight_indices=np.nonzero(original_coef)[0]
        n_nonzero=len(nonzero_weight_indices)
        #print(f"# of nonzero weights={n_nonzero} with C value {C_val}")
    
    print(f"# of nonzero weights={n_nonzero} with C value {C_val}")
    
    #save results
    predictions=classifier.predict(X_test)
    probs=classifier.predict_proba(X_test)
    intercept=classifier.intercept_
    
    
    #print combinations used in model
    #combinations used in model
    print("combinations used in original Lasso model")
    for i in nonzero_weight_indices:
        print(combo_names[i])
    
    print("\n")
    
    return classifier,original_coef,predictions,probs,intercept,C_val


#############################################################################################################

#given a list of model coefficients, gives a list of the zero betaj's that can be put in the model
def acceptable_beta_j(original_coef,intercept,C_val):
    cant_insert_betajs=[]

    n_weights=len(original_coef)

    all_indices=[]
    for i in range(n_weights):
        all_indices.append(i)

    nonzero_weight_indices=np.nonzero(original_coef)[0]

    zero_weight_indices=np.setdiff1d(all_indices,nonzero_weight_indices)
    
    
    
    for in_idx in zero_weight_indices:
        nonzero_weight_indices=np.nonzero(original_coef)[0]
        #if in_idx>20:
        #    break
        #print("\n")
        #print(f"in index = {in_idx} name of combo = {combo_names[in_idx]}")
        #print(f"in index = {in_idx}")
    
        #get new beta_j for each nonzero i index that could be switched out, then compare objective values for the new betas
        
        new_beta_dict={} #might not need this with objective val dict
        obj_val_dict={}
        #out_idx_nonzero_beta=[]
        
        
        #print(f"nonzero weight indices {nonzero_weight_indices}")
        for out_idx in nonzero_weight_indices:
            new_betaj,obj_val=nonzero_betaj(combo_mat=X_train.to_numpy(),beta_star=original_coef.copy(),intercept=intercept,y_vect=y_train.to_numpy(),C=C_val,j=in_idx,out_index=out_idx)
            new_beta_dict[out_idx]=new_betaj.item()
            if new_betaj.item()!=0:    
                obj_val_dict[out_idx]=obj_val.item() #dictionary of objective values for nonzero betas
                #out_idx_nonzero_beta.append(out_idx)
            #print(f"objective val {obj_val} out idx {out_idx}")
        #print(new_beta_dict)
          
            
        
        #put in a check to see if the list/dictionary are empty, if so cannot put the new feature into the model
        if len(obj_val_dict)==0:
            #print(f"Feature Combo Selected by User= {combo_names[in_idx]}")
            #print("ERROR, new beta values are zero, cannot put this feature combination into the model")
            cant_insert_betajs.append(in_idx)
    
    
    
    #list of acceptable features to take out of model
    
    print(f"zero betajs that can't be put in model: {cant_insert_betajs}")
    print("\n")
    acceptable_in_idx=np.setdiff1d(zero_weight_indices,cant_insert_betajs)
    
    features_to_add=[]
    
    for i in acceptable_in_idx:
        features_to_add.append(combo_names[i])
    return features_to_add        

######################################################

#given a betaj to insert in the model, adds best betaj to coefficient list and sets the best betai to 0
def new_coef_list(original_coef,X_train,y_train,intercept,C_val,in_idx,user_feature_list):
    
    nonzero_weight_indices=np.nonzero(original_coef)[0]
    
    #get new beta_j for each nonzero i index that could be switched out, then compare objective values for the new betas
    new_beta_dict={} #might not need this with objective val dict
    obj_val_dict={}
    out_idx_nonzero_beta=[]
    
    #print(f"nonzero weight indices {nonzero_weight_indices}")
    for out_idx in nonzero_weight_indices:
        if out_idx not in user_feature_list:
            new_betaj,obj_val=nonzero_betaj(combo_mat=X_train.to_numpy(),beta_star=original_coef.copy(),intercept=intercept,y_vect=y_train.to_numpy(),C=C_val,j=in_idx,out_index=out_idx)
            new_beta_dict[out_idx]=new_betaj.item()
            if new_betaj.item()!=0:    
                obj_val_dict[out_idx]=obj_val.item() #dictionary of objective values for nonzero betas
                out_idx_nonzero_beta.append(out_idx)
    
    
    min_out_idx=out_idx_nonzero_beta[0]
    min_obj_val=obj_val_dict[min_out_idx]
    for idx in out_idx_nonzero_beta:
        if obj_val_dict[idx]<min_obj_val:
            min_obj_val=obj_val_dict[idx]
            min_out_idx=idx
    
        beta_star=original_coef.copy()
        
        new_betas=beta_star.copy()
        new_betas[min_out_idx]=0
        new_betas[in_idx]=new_beta_dict[min_out_idx]
    
    print(f"Feature Combo Selected by User= {combo_names[in_idx]}")
    print(f"Feature Combo Removed from Model= {combo_names[min_out_idx]}")
    print("\n")
    
    return new_betas











 







#####################################################################
start=time.time()

X_train=pd.read_csv("election_combos_train.csv")
X_test=pd.read_csv("election_combos_test.csv")
y_train=X_train.iloc[:,-1]

#gets lists of names of rows and columns
train_row_names=list(X_train.iloc[:,0])
test_row_names=list(X_test.iloc[:,0])
#print(test_row_names)

X_train=X_train.iloc[:,1:-1] #removing animal name column and label column
X_test=X_test.iloc[:,1:] #removing animal name column

combo_names=list(X_test.columns)

#user_feature_list=['Flies_Does','Breathes using lungs_Yes ∧ Legs<3.0 ∧ Tail_Does not have','Legs>=3.0 ∧ Tail_Has', 'Teeth_Has ∧ Bred by humans_Has','Legs>=4.5', 'Spine_Has ∧ Tail_Does not have']
user_feature_list=['Gender_Male ∧ Advocates Pension_No ∧ Hobbies_Watching movies']
user_feature_indices=[]
classifier,original_coef,predictions,probs,intercept,C_val=optimal_Lasso(X_train,X_test,y_train)


current_coef=original_coef.copy()

for in_combo in user_feature_list:
    #get index of user selected combo
    in_idx=combo_names.index(in_combo)
    
    #get list of acceptable combinations that can be added given the current model coefficients
    s=time.time()
    acceptable_combo_list=acceptable_beta_j(current_coef,intercept,C_val)
    e=time.time()
    

    
    if in_combo in acceptable_combo_list:
        current_coef=new_coef_list(current_coef,X_train,y_train,intercept,C_val,in_idx,user_feature_indices)
        user_feature_indices.append(in_idx)
    else:
        print(f"Can't put {in_combo} in the model")




#acceptable_combo_list1=acceptable_beta_j(original_coef,intercept,C_val)

#user_combo_selection='Flies_Does'
#user_combo_selection='Legs<3.0 ∧ Tail_Does not have ∧ Bred by humans_Has'
#in_combo=user_combo_selection
#in_idx=combo_names.index(in_combo)
#if in_idx in acceptable_combo_list1:
#    new_betas=new_coef_list(original_coef,X_train,y_train,intercept,C_val,in_idx,user_feature_list)
#    user_feature_list.append(in_idx)
#else:
#    print(f"Can't put {user_combo_selection} in the model")

#acceptable_combo_list2=acceptable_beta_j(new_betas.copy(),intercept,C_val)


#user_combo_selection='Legs>=3.0 ∧ Tail_Has'

#in_combo=user_combo_selection
#in_idx=combo_names.index(in_combo)

#make sure this doesn't take out the original feature
#new_betas=new_coef_list(new_betas.copy(),X_train,y_train,intercept,C_val,in_idx,user_feature_list)




#############predictions from user feature selection ########################
print("PREDICTIONS FROM USER FEATURE SELECTION")
#print(intercept)

#changing the coefficients in the model to the new ones from user feature selection
classifier.coef_[0]=current_coef.copy() 
new_coef=classifier.coef_[0].copy()
nonzero_weight_indices=np.nonzero(new_coef)[0]
predictions=classifier.predict(X_test)
probs=classifier.predict_proba(X_test)
intercept=classifier.intercept_

#print(intercept)
#predictions
for i in range(len(test_row_names)):
    print(f"{test_row_names[i]} predicted as {predictions[i]} score={probs[i,1]}")
print("\n")


#combinations used in model
print("combinations used in final user selection model")
for i in nonzero_weight_indices:
    print(combo_names[i])



end=time.time()

print(end-start)

print(f"time for acceptable beta function = {e-s} ")



#define combo names somewhere!!!!!!!!!!!!!!!!!!!!!!!!!!






