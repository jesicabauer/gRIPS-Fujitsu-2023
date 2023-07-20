import pandas as pd
from sklearn.linear_model import Perceptron

def main(train_data ,test_data ):
    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    x=test_data.iloc[:,1:] 
    
    #setting model
    model = Perceptron(random_state=42)
    model.fit(train_x, train_y)
    
    # prediction
    y_pred = model.predict(x)

    return y_pred
