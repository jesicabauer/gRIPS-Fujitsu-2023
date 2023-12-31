import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from numpy.polynomial.polynomial import Polynomial
from sklearn.linear_model import LogisticRegression
from sklearn import svm


def Lasso(train_data ,test_data):

    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)
    
    #split data
    train_y=train_data.iloc[:,-1]
    train_x=train_data.iloc[:,1:-1] 
    x=test_data.iloc[:,1:] 

    #train the model
    C_val=20
    n_nonzero=101
    while n_nonzero>100:
        C_val=C_val*.9  #large C=denser beta, small C=sparser beta
       
        model=LogisticRegression(penalty="l1",C=C_val,solver="liblinear",random_state=0) #sets random state for reproducability
        
        classifier=model.fit(train_x,train_y) #fit model
        
        #get coefficients
        original_coef=classifier.coef_[0].copy()
        nonzero_weight_indices=np.nonzero(original_coef)[0]
        n_nonzero=len(nonzero_weight_indices)
    

    #get predictions
    predictions=classifier.predict(x)

    return predictions    


def SVM(data,test):


    data1 = np.delete(np.array(np.matrix(data)), 0, axis=1)
    labels = data.iloc[:, -1]  # 最後のカラムのラベルを取得
    data1 = np.delete(np.array(np.matrix(data1)), -1, axis=1)
    test = np.delete(np.array(np.matrix(test)), 0, axis=1)
    # Manually split the data
    X_train, X_test = data1, test#X[-2:]
    y_train = labels
    
    

    model = svm.SVC(kernel='linear')  
    


    # モデルの学習
    model.fit(X_train, y_train)

    # テストデータに対する予測
    predictions = model.predict(X_test)

    # 予測の表示

    return predictions

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

def Rademacher (model, erasuresize, data):
    #data = data.iloc[:-erasuresize]
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
    prediction =  model(df, test)
    
    b = np.array([i for i in df.iloc[:,-1]])
    return np.dot(b, prediction)/num_rows

def Rade2(model,  data, n):
    # Reduce the size of data if erasuresize > 0


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

def Rasyomon (model, erasuresize, data):
    #data = data.iloc[:-erasuresize]
    df = data.copy()
    
    df = df.replace(0, -1)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 20, random_state=42)
    train_data = pd.concat([X_train, y_train], axis=1)
    
    #Generate test data identical to the training data but without labels, and have it predicted
    
    prediction =  model(train_data, X_test)
    num_rows = len(y_test)
    return np.dot(y_test, prediction)/num_rows

def main(Data):
    
    model = [Lasso,SVM,RF,DT2,DT3,DT5,DT10,LR2,PT,NB]
    model_name = ["Lasso","SVM","RF", "DT2", "DT3", "DT5", "DT10","LR2", "PT", "NB"]

    sup_corre = Explore_data_correlations(Data)[0]
    inf_corre = Explore_data_correlations(Data)[1]

    
    if(Data.shape[0]>=81 and Data.shape[1] >= 2):
        data = Data
    else :
        data = Data_generation(300, 20, inf_corre, sup_corre) 
    #data = Data_generation(2000, 200, inf_corre, sup_corre)
    done =0
    all_model_data = []
    iterations = 50 
    run = 10
    for k in range(len(model)):  
        # book = {"model_name":"" ,"value":[]}
        row = data.shape[0]
        
        model_data_dict = {}
        model_data_dict["Model Name"] = model_name[k]
               
        List_comp_Rade2 = np.zeros(iterations)
        List_Data_Rade2 = np.zeros(iterations)
        
        accuracy = 0
        for j in range(iterations):
            compx_Rade = 0
            compx_Rade2 = 0
            
        
            for i in range(run):
                if(j==iterations-1):
                    compx_Rade += Rademacher(model[k], 0, data)
                    accuracy += Rasyomon(model[k] , 0, data)
                compx_Rade2 += Rade2(model[k],  data , int(j * row/iterations))
                #accuracy += Rasyomon(model[k] , data_erasure_size_Rasyo, data)
                
            done += 100/( int(iterations) * len(model))
            print(str(done) + "%")
            List_Data_Rade2[j] = int(j * row/50)
            List_comp_Rade2[j] = (compx_Rade2 / run)
        model_data_dict["complexity"] = compx_Rade/run
        model_data_dict["accuracy"] = accuracy/run
        model_data_dict["y_axis_Rade2"] = list(List_comp_Rade2)
        model_data_dict["x_axis_Rade2"] = list(List_Data_Rade2)
        x_values = List_Data_Rade2
        y_values = List_comp_Rade2
        yf = np.fft.fft(y_values)
        xf = np.fft.fftfreq(len(x_values), (x_values[1] - x_values[0])/2)
        cutoff = np.max(np.abs(xf))/10  # カットオフ周波数を設定
        yf[np.abs(xf) > cutoff] = 0  # カットオフ周波数以上の成分を0にする
        y_filtered = np.fft.ifft(yf).real
        model_data_dict["y_axis_Rade2_Fourier"] = list(y_filtered)
        model_data_dict["x_axis_Rade2_Fourier"] = list(x_values)
        # p = Polynomial.fit(x_values, y_values, 2)
        # model_data_dict["least-squares-approximation"] = p
        all_model_data.append(model_data_dict)

    for d in all_model_data:
        plt.ylim(0, 1.1)
        plt.plot(d['x_axis_Rade2_Fourier'], d['y_axis_Rade2_Fourier'])
    # plt.show()
    
    # for d in all_model_data:
    #     plt.ylim(0, 1.1)
    #     plt.plot(d['x_axis_Rade2'], d['y_axis_Rade2'])
    print(mpld3.fig_to_html(plt.figure()))
    # plt.show()
    return (all_model_data)


if __name__ == "__main__":
    print(main(Data = pd.read_csv('matrix_format.csv') ))









