import pandas as pd
# split dataset
class Storing_label():
    def __init__(self,label):
        self.label = label
def split_line(dataset,label_name):
    label_dataset = dataset.copy()
    label_dataset = label_dataset[label_name]
    delete_line = [];save_line = []
    for (i,l) in enumerate(label_dataset):
        if l == 1:
            save_line.append(i)
        else:
            delete_line.append(i)
    dataset_s = dataset.copy()
    dataset_d = dataset.copy()
    dataset_s.drop(index = delete_line, inplace=True)
    dataset_d.drop(index = save_line, inplace=True)
    return dataset_s,dataset_d
def split_dataset(dataset):
  #create data label and rows
  labels = [label for label in dataset.columns]
  rows = [row for row in dataset[labels[0]]]
  #parameter
  label_num = len(labels)
  true_label = [];false_label = []
  for i in range(label_num):
    dataset_s,dataset_d = split_line(dataset,labels[i])
    true_label.append(Storing_label(dataset_s))
    false_label.append(Storing_label(dataset_d))
  return true_label,false_label,dataset_s,dataset_d
#input data
data = pd.read_csv('matrix_format.csv')
data_c = data.copy()
true_label,false_label,dataset_s,dataset_d = split_dataset(data_c)
print(dataset_s,dataset_d)
