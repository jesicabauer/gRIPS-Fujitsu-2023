import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split
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



def Rasyomon (model, erasuresize, data):
    data = data.iloc[:-erasuresize]
    df = data.copy()

    
    df = df.replace(0, -1)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 40, random_state=42)
    train_data = pd.concat([X_train, y_train], axis=1)
    
    #Generate test data identical to the training data but without labels, and have it predicted
    
    prediction =  model(train_data, X_test)
    num_rows = len(y_test)
    return np.dot(y_test, prediction)/num_rows


def main(Data):
    model = [RF, DT2, DT3, DT5, DT10,LR2, PT, NB]
    model2 = ["RF", "DT2", "DT3", "DT5", "DT10","LR2", "PT", "NB"]
    book1  = {"RF":[], "DT2":[], "DT3":[], "DT5":[], "DT10":[],"LR2":[], "PT":[], "NB":[]} 
    book_list =[]

    sup_corre = Explore_data_correlations(Data)[0]
    inf_corre = Explore_data_correlations(Data)[1]  
    if(Data.shape[0]>=81 and Data.shape[1] >= 2):
        data = Data
    else :
        data = Data_generation(300, 200, inf_corre, sup_corre) 
    done =0
    
    all_model_data = []
    for k in range(len(model)):
        # book = {"model_name":"" ,"value":[]}
        book = {}

        
        #何回平均
        run = 15   

        model_data_dict = {}
        model_data_dict["Model Name"] = model2[k]
                 
        row = data.shape[0]
        data_erasure_size = row - 50
        add_data_size = int(data.shape[0]/50)
        iterations = int((data_erasure_size ) /add_data_size)    
        List_comp = np.zeros(iterations)
        List_Data = np.zeros(iterations)
        
        for j in range(iterations):
            compx = 0
            for i in range(run):
                compx += Rasyomon(model[k] , data_erasure_size, data)   
            List_Data[j] = row - (data_erasure_size + 40)
            List_comp[j] = compx / run
            data_erasure_size -= add_data_size
            done += 100/( int(iterations) * len(model))
            print(str(done) + "%")
            
        # book1[model2[k]].append(List_comp)
        # book1[model2[k]].append(List_Data)

        model_data_dict["y_axis"] = list(List_comp)
        model_data_dict["x_axis"] = list(List_Data)
        all_model_data.append(model_data_dict)
        # plt.xlabel('Data_size')
        # plt.ylabel('accuracy')
        # plt.plot(List_Data, List_comp,label=str(k))
        book["Model Name"] = model2[k]
        book["Accuracy Value"] = List_comp[-1]
        book_list.append(book)
    return (all_model_data , book_list)

if __name__ == "__main__":
    print(main(Data = pd.read_csv('matrix_format.csv')) )

