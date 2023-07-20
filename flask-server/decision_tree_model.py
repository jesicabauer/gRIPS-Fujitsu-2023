import pandas as pd
from sklearn import tree


def main(train_data_name = "animal_combos_train.csv",test_data_name = 'animal_combos_test.csv',max_depth=4):
    #input data
    train_data=pd.read_csv(train_data_name)
    test_data=pd.read_csv(test_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1]
    x=test_data.iloc[:,1:]
    
    #setting model
    model = tree.DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(train_x, train_y)
    # prediction
    y_pred = model.predict(x)
    
    return y_pred

#main(train_data_name = "animal_combos_train.csv",test_data_name = 'animal_combos_test.csv',max_depth=4)

main()