import pandas as pd
import numpy as np
from sklearn import svm

def main1(data,test):


    data1 = np.delete(np.array(np.matrix(data)), 0, axis=1)
    labels = data.iloc[:, -1]  # 最後のカラムのラベルを取得

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


def Rademacher ():
    data = pd.read_csv('matrix_format.csv')
    df = data.copy()
    
    # 最後の列を削除
    df = df.iloc[:, :-1]
    num_rows = df.shape[0]
    probabilities = [0, 1]  # 0と1の要素
    column_vector = np.random.choice(probabilities, size=(num_rows, 1), p=[0.5, 0.5])
    
    df['label'] = column_vector
    df = df.replace(0, -1)
    
    Data = np.delete(np.array(np.matrix(data)), 0, axis=1)
    test = Data[:]
    
    prediction =  main1(df,test)
    b=np.array([i for i in df.iloc[:,-1]])

    return np.dot(b, prediction)/num_rows

ran=1000
def main2():
    compx=0
    for i in range (ran):
        compx += Rademacher()
    print(compx / ran)

main2()
