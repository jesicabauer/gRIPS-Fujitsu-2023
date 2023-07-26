import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB

def RF(train_data_name ,test_data_name):
    train_data = pd.DataFrame(train_data_name)
    test_data = pd.DataFrame(test_data_name)
    
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    test_x=test_data.iloc[:,1:] 
    
    rf = RandomForestClassifier(n_estimators=20, random_state=42)
    
    rf.fit(train_x, train_y)
    
    y_pred = rf.predict(test_x)
    
    return y_pred


def DT2(train_data ,test_data):

    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)

    
    #split data
    train_y=train_data.iloc[:,-1]

    train_x=train_data.iloc[:,1:-1] 
    
    x=test_data.iloc[:,1:] 

    
    #setting model
    model = DecisionTreeClassifier(max_depth = 2, random_state=42)
    model.fit(train_x, train_y)
    
    # prediction
    y_pred = model.predict(x)

    # Plotting the decision tree

    return y_pred

def DT3(train_data ,test_data):

    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)

    
    #split data
    train_y=train_data.iloc[:,-1]

    train_x=train_data.iloc[:,1:-1] 
    
    x=test_data.iloc[:,1:] 

    
    #setting model
    model = DecisionTreeClassifier(max_depth = 3, random_state=42)
    model.fit(train_x, train_y)
    
    # prediction
    y_pred = model.predict(x)

    # Plotting the decision tree

    return y_pred

def DT5(train_data ,test_data):

    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)

    
    #split data
    train_y=train_data.iloc[:,-1]

    train_x=train_data.iloc[:,1:-1] 
    
    x=test_data.iloc[:,1:] 

    
    #setting model
    model = DecisionTreeClassifier(max_depth = 3, random_state=42)
    model.fit(train_x, train_y)
    
    # prediction
    y_pred = model.predict(x)

    # Plotting the decision tree

    return y_pred


def DT10(train_data ,test_data):

    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)

    
    #split data
    train_y=train_data.iloc[:,-1]

    train_x=train_data.iloc[:,1:-1] 
    
    x=test_data.iloc[:,1:] 

    
    #setting model
    model = DecisionTreeClassifier(max_depth = 10, random_state=42)
    model.fit(train_x, train_y)
    
    # prediction
    y_pred = model.predict(x)

    # Plotting the decision tree

    return y_pred

def LR2(train_data ,test_data):

    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)

    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    x=test_data.iloc[:,1:] 

    #setting model
    model = LogisticRegression(random_state=42)
    model.fit(train_x, train_y)
    
    # prediction
    y_pred = model.predict(x)

    # Plotting the decision tree

    return y_pred


def PT(train_data ,test_data ):
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
 

def NB(train_data_name ,test_data_name ):

    #input data
    train_data = pd.DataFrame(train_data_name)
    test_data = pd.DataFrame(test_data_name)
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    x=test_data.iloc[:,1:] 
    
    model = GaussianNB()
    model.fit(train_x, train_y)
    y_pred = model.predict(x)
    #y_prob = model.predict_proba(x)
    return y_pred


def Explore_data_correlations(data):
    df = data# pd.read_csv('matrix_format.csv')#Data_generate.main(1000,1000,0.0,1.0)
    df = df.iloc[:, 1:]
    df = df.replace(0, -1)
    # 最後の行の2列目以降をラベルデータとして取り出し、0 を -1 に変換する
    labels = df.iloc[:, -1] 
    
    df = df.drop(df.columns[-1], axis=1)
    
    
    
    # Compute the dot products
    dot_products = df.T.dot(labels)
    
    # Compute the norm (magnitude) of each column
    
    # Divide the dot products by the norms
    normalized_dot_products = dot_products / len(labels)
    final_results = (normalized_dot_products + 1) / 2
    sorted_results = final_results.sort_values(ascending=False)
    return sorted_results[0] , sorted_results[-1]

def Data_generation(n_rows, n_cols,inf_correlation,sup_correlation):
    # ラベル列の生成
    labels = np.random.choice([0, 1], size=n_rows)

    # すべての列に対してランダムな相関を設定
    correlations = np.random.uniform(inf_correlation, sup_correlation, size=n_cols)
    
    # 相関に基づいて各列のデータを生成
    data = np.array([np.where(labels==1, np.random.choice([0, 1], p=[1-correlation, correlation], size=n_rows), np.random.choice([0, 1], p=[correlation, 1-correlation], size=n_rows)) for correlation in correlations]).T

    # DataFrameに変換（行のラベルは行番号、列のラベルは相関係数）
    df = pd.DataFrame(data, index=[f"Row_{i}" for i in range(1, n_rows + 1)], columns=[str(correlation) for correlation in correlations])

    # 最後の列にラベルを設定
    df["Label"] = labels
    return df


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
    prediction = model(data, test)

    # Return the dot product divided by the number of rows
    return (data.iloc[:, -1] * prediction).mean()



def main(Data):
    model = [RF, DT2, DT3, DT5, DT10,LR2, PT, NB]
    book  = {"RF":[],"DT2":[],"DT3":[],"DT5":[],"DT10":[],"LR2":[],"PT":[],"NB":[]} 
    sup_corre = Explore_data_correlations(Data)[0]
    inf_corre = Explore_data_correlations(Data)[1]   
    
    if Data.shape[0] <= 2000:
        size1 = Data.shape[0]
    else:
        size1 = 2000
    if Data.shape[1] <= 200:
        size2 = Data.shape[0]
    else:
        size2 = 200

    
    data = Data_generation(size1, size2, inf_corre, sup_corre) 
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
        book[model[k].__name__].append(List_comp)
        book[model[k].__name__].append(List_Data)
        plt.ylim(0, 1)
        plt.xlim(0,iterations)
        plt.xlabel('landumly')
        plt.ylabel('Complexity')
        plt.plot(List_Data, List_comp,label=str(k))
    return book

main(Data = pd.read_csv('matrix_format.csv') )