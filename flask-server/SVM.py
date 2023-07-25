import numpy as np
from sklearn import svm


def main(data,test):


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





