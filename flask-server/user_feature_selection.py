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

def prox(x,alpha):
    return  np.sign(x)*max(0,abs(x)-alpha)

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


    '''
    #original_objective, can make this more efficient by skipping zero betas
    z=torch.zeros(m)
    for k in range(n):
        z+=beta_star[k]*combo_mat[:,k]
    z+=intercept_vect
    y_hat=sigmoid(z)
    original_obj=C*loss(y_hat,y_vect)
    for k in range(n):
        original_obj+=abs(beta_star[k])
    print(f"original objective {original_obj}")
    '''
    
    #calculate z_j vector based on beta_star and the out index
    z_j=torch.zeros(m)
    for k in range(n):
        if k!=out_index:
            z_j+=beta_star[k]*combo_mat[:,k] #k column 
    z_j+=intercept_vect
    
    
    
    #find optimal beta_j
    for iter in range(total_iterations):  #replace this with same stopping criteria from original Lasso problem
        #gets old beta j to use in stopping criteria
        beta_j_old=beta_j.data.item()
        #gets the next temp beta_j based on gradient descent from just the BCE Loss
        optimizer.zero_grad()   
        temp=beta_j*combo_mat[:,j]+z_j
        y_hat_vect=sigmoid(temp)
        #y_hat_vect=sigmoid(beta_j*combo_mat[:,j]+z_j)
        l=C*loss(y_hat_vect,y_vect)
        l.backward()
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



#Regular Lasso to find beta star

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
#min_C=l1_min_c(X_train,y_train,loss="log")
#print(f"minimum acceptable C= {min_C}")

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
    original_coef=classifier.coef_[0].copy()
    nonzero_weight_indices=np.nonzero(original_coef)[0]
    n_nonzero=len(nonzero_weight_indices)
    #print(f"# of nonzero weights={n_nonzero} with C value {C_val}")

#print(f"nonzero coefs first assignment {nonzero_weight_indices}")
print(f"# of nonzero weights={n_nonzero} with C value {C_val}")

#save results
predictions=classifier.predict(X_test)
probs=classifier.predict_proba(X_test)
intercept=classifier.intercept_


#############################################################################################################

#trading a zero feature combinations for a nonzero feature combination



n_weights=X_train.to_numpy().shape[1]

all_indices=[]
for i in range(n_weights):
    all_indices.append(i)

nonzero_weight_indices=np.nonzero(original_coef)[0]
#print(f"nonzero coefs second assignment {nonzero_weight_indices}")

zero_weight_indices=np.setdiff1d(all_indices,nonzero_weight_indices)

print("Combinations being used in the model:")
for i in nonzero_weight_indices:
    print(f"{combo_names[i]} index {i}")
print("\n")
print("Combinations NOT being used in the model:")
for i in zero_weight_indices:
    print(f"{combo_names[i]} index {i}")



#get index of feature combination that user wants to include in the model
#user_combo_selection='Legs<3.0 ∧ Tail_Has'
#in_idx=combo_names.index(user_combo_selection)

#in_idx=2   #can be any of the zero indices, will be inputted by the user

for in_idx in zero_weight_indices:
    nonzero_weight_indices=np.nonzero(original_coef)[0]
    if in_idx>30:
        break
    print("\n")
    #print(f"in index = {in_idx} name of combo = {combo_names[in_idx]}")
    print(f"in index = {in_idx}")

    #get new beta_j for each nonzero i index that could be switched out, then compare objective values for the new betas
    
    new_beta_dict={} #might not need this with objective val dict
    obj_val_dict={}
    out_idx_nonzero_beta=[]
    
    
    #print(f"nonzero weight indices {nonzero_weight_indices}")
    for out_idx in nonzero_weight_indices:
        new_betaj,obj_val=nonzero_betaj(combo_mat=X_train.to_numpy(),beta_star=original_coef.copy(),intercept=intercept,y_vect=y_train.to_numpy(),C=C_val,j=in_idx,out_index=out_idx)
        new_beta_dict[out_idx]=new_betaj.item()
        if new_betaj.item()!=0:    
            obj_val_dict[out_idx]=obj_val.item() #dictionary of objective values for nonzero betas
            out_idx_nonzero_beta.append(out_idx)
        #print(f"objective val {obj_val} out idx {out_idx}")
    #print(new_beta_dict)
      
        
    
    #put in a check to see if the list/dictionary are empty, if so cannot put the new feature into the model
    if len(obj_val_dict)==0:
        print(f"Feature Combo Selected by User= {combo_names[in_idx]}")
        print("ERROR, new beta values are zero, cannot put this feature combination into the model")
    else:
        min_out_idx=out_idx_nonzero_beta[0]
        min_obj_val=obj_val_dict[min_out_idx]
        for idx in out_idx_nonzero_beta:
            if obj_val_dict[idx]<min_obj_val:
                min_obj_val=obj_val_dict[idx]
                min_out_idx=idx
        #print(min_obj_val)
        #print(min_out_idx)
    
    
        beta_star=original_coef.copy()
        
        new_betas=beta_star.copy()
        new_betas[min_out_idx]=0
        new_betas[in_idx]=new_beta_dict[min_out_idx]
        
        #print(f"Feature Combo Selected by User= {combo_names[in_idx]}")
        #print(f"Feature Combo Removed from Model= {combo_names[min_out_idx]}")
        
        
        '''
        #############predictions from beta star original lasso ########################
        print("PREDICTIONS FROM ORIGINAL LASSO")
        
        #already calculated above
        #predictions=classifier.predict(X_test)
        #probs=classifier.predict_proba(X_test)
        #intercept=classifier.intercept_
        
        #predictions
        for i in range(len(test_row_names)):
            print(f"{test_row_names[i]} predicted as {predictions[i]} score={probs[i,1]}")
            
       
        #important combinations are their weights
        print(f"number of nonzero weights={len(nonzero_weight_indices)}")
        for i in nonzero_weight_indices:
            print(combo_names[i])
            print(f"weight: {original_coef[i]}")
        
        
        print(f"intercept= {intercept}")
        
        '''
        
        
        #############predictions from user feature selection ########################
        print("PREDICTIONS FROM USER FEATURE SELECTION")
        
        print(f"Feature Combo Selected by User= {combo_names[in_idx]}")
        print(f"Feature Combo Removed from Model= {combo_names[min_out_idx]}")
        
        #changing the coefficients in the model to the new ones from user feature selection
        classifier.coef_[0]=new_betas.copy() 
        new_coef=classifier.coef_[0].copy()
        nonzero_weight_indices=np.nonzero(new_coef)[0]
        predictions=classifier.predict(X_test)
        probs=classifier.predict_proba(X_test)
        intercept=classifier.intercept_
        
        #predictions
        for i in range(len(test_row_names)):
            print(f"{test_row_names[i]} predicted as {predictions[i]} score={probs[i,1]}")
            
            
        #important combinations are their weights
        
        '''
        print(f"number of nonzero weights={len(nonzero_weight_indices)}")
        for i in nonzero_weight_indices:
            print(combo_names[i])
            print(f"weight: {new_coef[i]}")
        
        
        print(f"intercept= {intercept}")
        '''


#####################################################
'''
things to consider:
- how to set C (determines sparsity of beta), currently set to keep the number of nonzero weights less than 100
- how to set alpha (stepsize for prox grad descent), currently set as 0.1
- how to deal with user selected features that cannot be put in the model (all new betas are zero)- give error 
  message or only show user zero weight features that are able to be put in the model?



'''








