
import pandas as pd
import numpy as np
import SVM
import RF
import DT2
import DT3
import DT5
import DT10
import LR
import PT
import NB
import Data_generate
import Explore_data_correlations
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split
warnings.filterwarnings('ignore')



def Rasyomon (model, erasuresize, data):
    data = data.iloc[:-erasuresize]
    df = data.copy()

    
    df = df.replace(0, -1)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    train_data = pd.concat([X_train, y_train], axis=1)
    
    #Generate test data identical to the training data but without labels, and have it predicted
    
    prediction =  model.main(train_data, X_test)
    num_rows = len(y_test)
    return np.dot(y_test, prediction)/num_rows


def main(Data ):
    model = [SVM,RF, DT2, DT3, DT5, DT10,LR, PT, NB]
    book  = {SVM:[],RF:[], DT2:[], DT3:[], DT5:[], DT10:[],LR:[], PT:[], NB:[]} 
    for k in range(len(model)):
        #何回平均
        run = 10      
        Data = pd.read_csv('matrix_format.csv')
        sup_corre = Explore_data_correlations.main(Data)[0]
        inf_corre = Explore_data_correlations.main(Data)[1]   
        if Data.shape[0] <= 1500:
            size1 = Data.shape[0]
        else:
            size1 = 1500
        if Data.shape[1] <= 1500:
             size2 = Data.shape[0]
        else:
             size2 = 1500
            
        data = Data_generate.main(size1, size2, inf_corre, sup_corre)        
        row = data.shape[0]
        if(int(data.shape[0]/50)>10):
            data_erasure_size = row - int(data.shape[0]/50)
        else:
            data_erasure_size = row - 10
        add_data_size = int(data.shape[0]/50)
        iterations = int(data_erasure_size /add_data_size)    
        List_comp = np.zeros(iterations)
        List_Data = np.zeros(iterations)
        
        for j in range(iterations):
            compx = 0
            for i in range(run):
                compx += Rasyomon(model[k] , data_erasure_size, data)   
            List_Data[j] = row - data_erasure_size
            List_comp[j] = compx / run
            data_erasure_size -= add_data_size
            print(List_Data[j])
            print(List_comp[j])
        book[model[k]].append(List_comp)
        book[model[k]].append(List_Data)
        #plt.plot(List_Data, List_comp)
    return book

main(Data = pd.read_csv('5000cutData.csv') )
