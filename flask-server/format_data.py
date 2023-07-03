import pandas as pd
import re

##########################################
# for animal training dataset
# format into binary matrix to test LASSO
##########################################

original_data = pd.read_csv("animals_train.csv")
# print(original_data)

step2_data = pd.read_csv("animal_step2_data.csv")
# print(step2_data)

animals_col = list(original_data["Name"])
# print(animals_col)

combinations_col = list(step2_data["Combination of important items"])
# print(combinations_col)

matrix_dict = dict()
matrix_dict["animals"] = animals_col

# ------------ format combinations
# turn combos from step 2 data into binary 0 1
thresholds = set() # save thresholds for parsing later
all_combo_binary = [] # [{feature1: #, feature2: #, ..}, {combo 2}, {combo 3}]
for combo in combinations_col:
    matrix_dict[combo] = [0] * len(animals_col)
    combo_string = combo.split("∧") # get features from the combos
    single_combo = dict()
    for feature in combo_string:
        binary_split = feature.split("_") # get value for feature
        # print(binary_split)
        if len(binary_split) > 1: # it's not a threshold
            if binary_split[1].strip() == "Has" or binary_split[1].strip() == "Yes":
                single_combo[binary_split[0].strip()] = 1
            else:
                single_combo[binary_split[0].strip()] = 0 # placeholder 0 for thresholds
        else:
            thresholds.add(binary_split[0].strip())
            single_combo[binary_split[0].strip()] = 1
    # print(single_combo)
    all_combo_binary.append(single_combo)

# print(all_combo_binary)
# print(thresholds)
threshold_dict = dict() # {feature: set(threshold numbers)}
# --------------- thresholds into dictionary
for feature in thresholds:
    # print(feature)
    # print(re.split(r'(\W+)', feature, 1))
    threshold_value = re.split(r'(\W+)', feature, 1)
    if threshold_value[0] not in threshold_dict:
        threshold_dict[threshold_value[0]] = set()
    threshold_dict[threshold_value[0]].add(threshold_value[2])

# print(threshold_dict)
# ----------------
print(all_combo_binary)
# print(len(all_combo_binary))
# matrix_dict["combinations"] = combinations_col
# print(matrix_dict)

# matrix_df = pd.DataFrame(matrix_dict)
# print(matrix_df)
# matrix_df.to_csv("matrix_format.csv")


# ------------ fill in matrix df
# dict_original = original_data.to_dict()
# print(dict_original)

## turn original data into a dict
original_data_dict = dict() # {animal: {feature1: #, feature2: #,...}}
for index, row in original_data.iterrows():
    data = dict()
    # print(row)
    for column in original_data.columns[1:]:
        # print(column)
        # print(row[column])

        if column == "Label": # keep the label as is
            data[column] = row[column]
        elif row[column] == "Has" or row[column] == "Yes":
            data[column] = 1
        elif column == "Legs": # based on threshold
            # print(row[column])
            # columns based on threshold
            for t_feature, t_value in threshold_dict.items():
                # print(t_feature)
                for num in t_value:
                    if row[column] >= float(num):
                        data[t_feature+">="+num] = 1
                        data[t_feature+"<"+num] = 0
                    else:
                        data[t_feature+">="+num] = 0
                        data[t_feature+"<"+num] = 1
        else:
            data[column] = 0
        # break
    original_data_dict[row[0]] = data # row[0] is animal name
    # break

# print(original_data_dict)
# print(thresholds)
# print(matrix_dict)
# print(len(original_data_dict.keys()))

# for animals in matrix_dict
# for index, combination in enumerate(all_combo_binary):
    # print(index)
    # print(combination)

# print(all_combo_binary)

# loop through all animals with their features
check_combos = dict() # {animal: [combo1, combo2, combo3 ...]} combinations from step 2
for animal, value in original_data_dict.items():
    # print(value)
    check_combos[animal] = []
    # loop through all the combinations
    for step2_combo in all_combo_binary:
        # print(step2_combo)
        check_combos[animal].append(1)
        for feature, binary in step2_combo.items():
            # print(binary)
            if value[feature] != binary:
                check_combos[animal][-1] = 0
# print(matrix_dict)
combo_matrix = pd.DataFrame.from_dict(check_combos, orient="index") # put into matrix format
# print(check_combos)
# print(combo_matrix)
combo_matrix.columns = combinations_col # add in column names
# combo_matrix.to_csv("matrix_format.csv") # save to csv file

    

            
            