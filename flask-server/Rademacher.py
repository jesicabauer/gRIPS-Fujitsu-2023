import pandas as pd
import numpy as np
import SVM
import RF
import DT
import LR
import PT
import NB
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')



def Rademacher (model, erasuresize, data):
    data = data.iloc[:-erasuresize]
    df = data.copy()
    num_rows = df.shape[0]
    
    df = df.iloc[:, :-1]
    probabilities = [0, 1]
    column_vector = np.random.choice(probabilities, size=(num_rows, 1), p=[0.5, 0.5]) 
    df['label'] = column_vector
    
    df = df.replace(0, -1)
    test = np.delete(np.array(np.matrix(data)), -1, axis=1)
    test[test == 0] = -1
    prediction =  model.main(df, test)
    
    b = np.array([i for i in df.iloc[:,-1]])
    return np.dot(b, prediction)/num_rows


def main():
    data = pd.read_csv('5000cutData.csv')
    row = data.shape[0]
    data_erasure_size = row - 50
    run = 10
    iterations = 90
    
    List_comp = np.zeros(iterations)
    List_Data = np.zeros(iterations)

    for j in range(iterations):
        compx = 0
        for i in range(run):
            compx += Rademacher(PT , data_erasure_size, data)   
        List_Data[j] = (row  - data_erasure_size)
        List_comp[j] = (compx / run)
        data_erasure_size -= 50
        print(List_Data[j])
        print(List_comp[j])
        plt.ylim(0, 1)
    plt.plot(List_Data, List_comp)

main()
