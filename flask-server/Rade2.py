import pandas as pd
import numpy as np
import SVM
import RF
import LR
import PT
import NB
import DT2
import DT3
import DT5
import DT10
import Data_generate
import Explore_data_correlations
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


def Rade2(model, erasuresize, data, n):
    # Reduce the size of data if erasuresize > 0
    if erasuresize > 0:
        data = data.iloc[:-erasuresize]

    # Replace 0 with -1
    data = data.replace(0, -1)
    
    # Reverse n labels chosen randomly
    size = data.shape[0]
    random_indices = np.random.choice(size, size=n, replace=False)
    
    # Create a vector with 1s and -1s
    vector = np.ones(size)
    vector[random_indices] = -1
    
    # Replace the labels in the dataframe
    data.iloc[:, -1] *= vector

    # Generate test data
    test = data.iloc[:, :-1].values
    test[test == 0] = -1
    
    # Predict using the model
    prediction = model.main(data, test)

    # Return the dot product divided by the number of rows
    return (data.iloc[:, -1] * prediction).mean()



def main(Data):
    model = [RF, DT2, DT3, DT5, DT10,LR, PT, NB]
    book  = {RF:[], DT2:[], DT3:[], DT5:[], DT10:[],LR:[], PT:[], NB:[]} 
    sup_corre = Explore_data_correlations.main(Data)[0]
    inf_corre = Explore_data_correlations.main(Data)[1]   
    
    if Data.shape[0] <= 2000:
        size1 = Data.shape[0]
    else:
        size1 = 2000

    
    data = Data_generate.main(size1, 200, inf_corre, sup_corre) 
    done =0
    for k in range(len(model)):
        run = 10 
        row = data.shape[0]
        data_erasure_size = 0
       
        iterations = row  - data_erasure_size
            
        List_comp = np.zeros(50)
        List_Data = np.zeros(50)
            
        for j in range(50):
            compx = 0
            for i in range(run):
                compx += Rade2(model[k], data_erasure_size, data , int(j * iterations/50))  
            List_Data[j] = int(j * iterations/50)
                #"run" times average
            List_comp[j] = (compx / run)
            done += 100/(50 * len(model))
            print(str(done) + "%")
        book[model[k]].append(List_comp)
        book[model[k]].append(List_Data)
        plt.ylim(0, 1)
        plt.xlim(0,iterations)
        plt.xlabel('landumly')
        plt.ylabel('Complexity')
        plt.plot(List_Data, List_comp,label=str(k))
    return book

main(Data = pd.read_csv('matrix_format.csv') )