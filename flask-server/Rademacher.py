import pandas as pd
import numpy as np
import SVM
import RF
import DT2
import DT3
import DT5
import DT10
import LR2
import PT
import NB
import Data_generate
import Explore_data_correlations
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')




def Rademacher (model, erasuresize, data):
    data = data.iloc[:-erasuresize]
    df = data.copy()
    num_rows = df.shape[0]
    
    #Completely relabeling randomly

    df = df.iloc[:, :-1]
    probabilities = [0, 1]
    column_vector = np.random.choice(probabilities, size=(num_rows, 1), p=[0.5, 0.5]) 
    df['label'] = column_vector

    #Generate test data identical to the training data but without labels, and have it predicted
    df = df.replace(0, -1)
    test = np.delete(np.array(np.matrix(data)), -1, axis=1)
    test[test == 0] = -1
    prediction =  model.main(df, test)
    
    b = np.array([i for i in df.iloc[:,-1]])
    return np.dot(b, prediction)/num_rows

def main(Data):
    model = [SVM,RF, DT2, DT3, DT5, DT10,LR2, PT, NB]
    book  = {SVM:[],RF:[], DT2:[], DT3:[], DT5:[], DT10:[],LR2:[], PT:[], NB:[]} 
    for k in range(len(model)):
        run = 10
         
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
                compx += Rademacher(model[k], data_erasure_size, data)   
            List_Data[j] = (row  - data_erasure_size)
            List_comp[j] = (compx / run)
            data_erasure_size -= add_data_size
            print(List_Data[j])
        book[model[k]].append(List_comp)
        book[model[k]].append(List_Data)
        #plt.ylim(0, 1)
        #plt.xlabel('Data_size')
        #plt.ylabel('Complexity')
        #plt.plot(List_Data, List_comp,label=str(k))
    return book

main(Data = pd.read_csv('5000cutData.csv') )
