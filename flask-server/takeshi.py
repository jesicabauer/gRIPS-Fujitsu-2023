import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
#from pathlib import Path
#import codecs as cd
filepath = 'matrix_format.csv'
df = pd.read_csv(filepath)
#df.head()
labels = [label for label in df.columns]
'''
#df_x = df[[labels[0],labels[4],labels[9],labels[10]]]
df_x = df[[labels[l] for l in range(1,len(labels)-1)]]
df_y = df[labels[-1]]
'''
df_x = df.iloc[:,1:-1]
df_y = df.iloc[:,-1]
df_x = pd.get_dummies(df_x, drop_first=True)
train_x, test_x, train_y, test_y = train_test_split(df_x,df_y,random_state=1)
model = tree.DecisionTreeClassifier(max_depth=2, random_state=1)
model.fit(train_x, train_y)
model.predict(test_x)
model.score(test_x,test_y)
y_pred = model.predict(test_x)
accuracy = accuracy_score(test_y, y_pred)
print(f"Accuracy: {accuracy}")
#plot_tree(model, feature_names=train_x.columns, class_names=True, filled=True)
plot_tree(model, feature_names=train_x.columns)
plt.savefig("desicion_tree_animals.pdf")
