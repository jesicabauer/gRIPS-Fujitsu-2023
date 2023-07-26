import pandas as pd
import numpy as np
from sklearn import linear_model


def main(train_data_name,test_data_name):
    #input data
    train_data=pd.DataFrame(train_data_name)
    test_data = pd.DataFrame(test_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    test_x=test_data.iloc[:,1:] 
    
    #setting model
    lr = linear_model.LinearRegression()
    #prediction
    lr.fit(train_x,train_y)
    y_pred = lr.predict(test_x)
    for i in range(len(y_pred)):
        if y_pred[i] < 0:
            y_pred[i] = -1
        else:
            y_pred[i] = 1

    #y_pred = [x.replace('.', '') for x in y_pred]
    y_pred=np.array([int(x) for x in y_pred])
    return y_pred

