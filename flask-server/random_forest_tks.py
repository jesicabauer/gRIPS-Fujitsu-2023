# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:05:14 2023

@author: Takeshi
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
def main(train_data_name = "animal_combos_train.csv",test_data_name = 'animal_combos_test.csv'):
    #input data
    train_data=pd.read_csv(train_data_name)
    test_data=pd.read_csv(test_data_name)
    
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    test_x=test_data.iloc[:,1:] 
    
    
    # ランダムフォレストモデルを作成する create RF
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # モデルをトレーニングする training model
    rf.fit(train_x, train_y)
    
    # テストセットを予測する predicted test set
    y_pred = rf.predict(test_x)
    y_pred_prob = rf.predict_proba(test_x)
    #print(f'y:{y_pred},y_p:{y_pred_prob[:,1]}')
    return y_pred

# main(train_data_name,test_data_name) ;if file change, train_data_name = 'file_name'
main()