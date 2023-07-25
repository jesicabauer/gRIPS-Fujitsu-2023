import pandas as pd
import numpy as np
import Data_generate

def main(data):
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
    return sorted_results[0],sorted_results[-1]
# Print the results

