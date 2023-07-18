import pandas as pd
import re

##########################################
# for animal training dataset
# format into binary matrix to test LASSO
##########################################

data_type="train"

original_data = pd.read_csv("animals_train.csv")
#original_data = pd.read_csv("COVID_train.csv")
# original_data = pd.read_csv("defect_prevention_train.csv")
#original_data = pd.read_csv("election_test.csv")



step2_data = pd.read_csv("animal_step2_data.csv")
#step2_data = pd.read_csv("covid_step2_data.csv")
# step2_data = pd.read_csv("defect_prevention_train_step2_data.csv")
#step2_data = pd.read_csv("elections_step2_data.csv")
# print(step2_data)


animals_col = list(original_data[original_data.columns[0]])

if data_type=="train":
    labels_col = list(original_data[original_data.columns[-1]])

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
    # print(feature)
    # print(re.split(r'(\W+)', feature, 1))
    threshold_value = re.split(r'>=|<', feature)
    #print(threshold_value)
    if threshold_value[0] not in threshold_dict:
        threshold_dict[threshold_value[0]] = set()
    threshold_dict[threshold_value[0]].add(threshold_value[1])




###############adding new columns to make all variables binary #####################

original_data_bin_cols=original_data
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
            #print(f"value={val}")
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
        #use process from lines 168 to 172 to make new columns
        print(col_name)
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

check_combos = dict() # {animal: [combo1, combo2, combo3 ...]} combinations from step 2
for idx,row in original_data_bin_cols.iterrows():
    animal=row[0]
    #print(animal)
    check_combos[animal] = []
    # loop through all the combinations
    for step2_combo in combinations_col:
        #print(step2_combo)
        combo_string_list=step2_combo.split(" ∧ ")
        check_combos[animal].append(1)
        for feature in combo_string_list:
            if feature not in binary_col_names: #if a particular feature value does not exist in the data but does exist in step 2 combo
                check_combos[animal][-1]=0
                break
            elif original_data_bin_cols.loc[idx,feature]!=1:
                check_combos[animal][-1]=0
                break
    if data_type=="train":
        check_combos[animal].append(labels_col[idx])   
 

combo_matrix = pd.DataFrame.from_dict(check_combos, orient="index") # put into matrix format
if data_type=="train":
    combinations_col.append("Label")
combo_matrix.columns = combinations_col # add in column names

combo_matrix.to_csv("covid_combos_train.csv") # save to csv file

