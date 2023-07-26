import pandas as pd
import numpy as np
data = pd.read_csv('matrix_format.csv')
np.set_printoptions(threshold=np.inf)
df = data.copy()



def def1 (Set, q ,boolean):
    newSet = Set[Set.iloc[:,q] == boolean]
    return newSet
            
def def2 (setj):
    setj = setj.values 
    ones_matrix = setj[np.all(setj[:, -1:] == 1, axis=1)]
    count_1_1 = np.sum(ones_matrix, axis=0)  
    count_1_1 = count_1_1[1:-1]
    count_1_0 = np.abs([element - ones_matrix.shape[1] for element in count_1_1])
   
    zeros_matrix = setj[np.all(setj[:, -1:] == 0, axis=1)]
    count_0_1 = np.sum(zeros_matrix, axis=0) 
    count_0_1 = count_0_1[1:-1]  
    count_0_0 = np.abs([element - ones_matrix.shape[1] for element in count_0_1])
    vec1 = np.abs(count_1_1 - count_0_1)
    vec0 = np.abs(count_1_0 - count_0_0)
    
    if(np.max(vec1)>=np.max(vec0)):
        return np.argmax(vec1)+1 #becouse count_1_1 = count_1_1[1:-1]
    else :
        return np.argmin(vec0)+1
       
def def3 (Q,setj,boolean):
    setj = setj.values     
    if(boolean ==1):
        prob = np.sum(setj[:,Q]) / (setj.shape[0])
        
    else :
        prob = (setj.shape[0]  - np.sum(setj[:,Q])) / (setj.shape[0])
    print(prob)
    return prob
    

def main():
    p = 0.5
    setj = df
    for i in range (1):
        Q = 4#def2(setj)
       # print(Q)
        boolean = int(input("boolean:"))
        P_A = def3(Q,setj , boolean)     
        setj = def1 (setj , Q , boolean)
        P_A_B = def3(-1,setj,boolean)
        #print(P_A_B /P_A)
        p = p * P_A_B /P_A
        print(p)
        

main()