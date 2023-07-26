# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 16:26:07 2023

@author: Molly
"""

import pandas as pd
import re


def combination_counter(dataset_csv,dataset_type,step2data_csv,combination_to_count):

    ##########################################
    # for animal training dataset
    # format into binary matrix to test LASSO
    ##########################################
    
    #data_type="train"
    data_type=dataset_type
    
    original_data = pd.read_csv(dataset_csv)
    
    step2_data=pd.read_csv(step2data_csv)
   
    combinations_col = list(step2_data["Combination of important items"])
    
    
    
    # ------------ format combinations
    
    
    ################### getting threshold column names ###########################
    thresholds = set() # save thresholds for parsing later
    for combo in combinations_col:
        combo_string = combo.split("∧") # get features from the combos
        for feature in combo_string:
            binary_split = feature.split("_") # get value for feature
            if len(binary_split)==1: #threshold
                thresholds.add(binary_split[0].strip())
            
           
    
    ################# creating threshold dictionary with cutoff values ###############
    threshold_dict = dict() # {feature: set(threshold numbers)}
    # --------------- thresholds into dictionary
    for feature in thresholds:
        threshold_value = re.split(r'>=|<', feature)
        if threshold_value[0] not in threshold_dict:
            threshold_dict[threshold_value[0]] = set()
        threshold_dict[threshold_value[0]].add(threshold_value[1])
    
    
    
    
    ###############adding new columns to make all variables binary #####################
    
    original_data_bin_cols=original_data.copy()
    col_idx=1
    n_cols=len(original_data.columns)
    if data_type=="test":
        n_cols+=1
    
    threshold_cols=list(threshold_dict.keys())
    
    
    for col_name, col_data in original_data.items():
        #converting all categorical columns to binary
        if col_idx!=1 and col_idx!=n_cols and col_name not in threshold_cols: #all columns except name, label, and threshold columns
            col_val_set=set() #set of unique values in that column
            for val in col_data:
                if not pd.isna(val):
                    col_val_set.add(val)
            for val in col_val_set: #loops through each unique value from that column
                new_col_name=col_name+"_"+str(val) #new name of column, i.e. Wings_Has
                binary_list=[]
                for v in col_data:
                    if v==val: #check if val is a number or string
                        binary_list.append(1)
                    else:
                        binary_list.append(0)
                original_data_bin_cols.insert(loc=1,column=new_col_name,value=binary_list) #add new column
            original_data_bin_cols=original_data_bin_cols.drop(col_name,axis=1)  #remove original column
        
        #converting threshold columns to binary
        if col_name in threshold_cols:            
            t_values=threshold_dict[col_name]
            for num in t_values:
                bin_list_geq=[]
                bin_list_l=[]
                for r in col_data:
                    if r>=float(num):
                        bin_list_geq.append(1)
                        bin_list_l.append(0)
                    else:
                        bin_list_geq.append(0)
                        bin_list_l.append(1)
                original_data_bin_cols.insert(loc=1,column=col_name+">="+num,value=bin_list_geq)
                original_data_bin_cols.insert(loc=1,column=col_name+"<"+num,value=bin_list_l)
            original_data_bin_cols=original_data_bin_cols.drop(col_name,axis=1)  #remove original column
            
        col_idx+=1
    binary_col_names=list(original_data_bin_cols.columns)
    

    
    ####################building final data matrix by checking combinations ###############################
    

    combo_count=0
    for idx,row in original_data_bin_cols.iterrows():
        has_combo=1
        combo_string_list=combination_to_count.split("∧")
        for feature in combo_string_list:
            feature=feature.strip()
            if feature not in binary_col_names: #if a particular feature value does not exist in the data but does exist in step 2 combo
                print(f"feature {feature} is not present in the dataset")
                has_combo=0
                break
            elif original_data_bin_cols.loc[idx,feature]!=1:
                has_combo=0
                break
        combo_count+=has_combo
        
    
    print(f"combination {combination_to_count} occurs {combo_count} times in this dataset")
    return combo_count
      
    



#####################################################################################################################



dataset_csv="election_test.csv"
dataset_type="test" #either "train" or "test"
step2data_csv="elections_step2_data.csv"
combination_to_count="Gender_Female"

#note: combination_to_count must be in format: feature name∧feature name
#if format is incorrect, error message will display saying the feature is not present in the dataset

#function returns the number of times the combination occurs in the dataset
count=combination_counter(dataset_csv,dataset_type,step2data_csv,combination_to_count)











