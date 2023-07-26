import pandas as pd
import numpy as np
import math as m
#setting
xl= pd.read_excel('matrix_format.xlsm')
Data = np.matrix(xl)
idx_num = len(xl.index)
col_num = len(xl.columns)
maxiteration = 1000000000
seta = np.zeros(idx_num)
A = np.zeros ((idx_num,col_num))
Z = np.zeros ((idx_num,1))
y = np.zeros (idx_num)
ganma = np.zeros (idx_num)

def idx(i):
   idx = (Data[0:idx_num,i])
   one_dim = idx.flatten()
   one_dim_list = one_dim.tolist()
   flat_list = [item for sublist in one_dim_list for item in sublist]
   return flat_list

def col(i):
    col = (Data[i])
    one_dim = col.flatten()
    one_dim_list = one_dim.tolist()
    flat_list = [item for sublist in one_dim_list for item in sublist]
    return flat_list

def matrixA (matrix,vector):
    for i in range (1,col_num):   
        num = np.dot(idx(i),vector)
        element = (1.0/(1.0 + m.exp(-num))) * (1.0 - 1.0/(1.0 + m.exp(-num)))
        matrix[i][i]=m.sqrt(element)
    return matrix
        
def vectorZ (z,vector):
    z = np.zeros ((idx_num,1))
    for i in range (1,col_num):   
        num = np.dot(idx(i),vector)
        element = num + (1.0/(1.0 + m.exp( 1.0 - y[i]*num ))*y[i]) / A[i][i]
        z[i][0] = element
    #Ze = np.reshape(z, (col_num, 1)) # Zを列ベクトルに変換
    return z
        
def Lasso (X,y,r):
    w = np.zeros(col_num)
    for k in range (1000):
        if k ==0:
            w[0] = (y - np.dot(X[:,1],w[1:])).sum() / idx_num
        
        else :
            k2 = [i for i in range(idx_num) if i not in [0,k]]
            
            a = np.dot((y-np.dot(X[:,k2],w[k2])-w[0]),k[:,k]).sum
            
            b = (X[:,k]**2).sum()
            if a > idx_num * r : # wkが正となるケース
                w[k] = (a - idx_num * r) / b
                
            elif a < -r * idx_num : # wkが負となるケース
                w[k] = (a + idx_num * r) / b
                
            else : # それ以外のケース
                w[k] = 0
    return w
    
        
#~main~
def main():
    seta = np.zeros(idx_num)
    A = np.zeros ((idx_num,col_num))
    Z = np.zeros ((idx_num,1))
    y = np.zeros (idx_num)
    ganma = np.zeros (idx_num)
    for k in range (2) :
        A = matrixA(A,seta)
        #print(A)
        Z = vectorZ(Z,seta)
        print(Z)
        #ganma = Lasso(np.dot(A,Z),y,seta)
        #print(A)
        #print(Z)
        


main()

     
        
        
    

    