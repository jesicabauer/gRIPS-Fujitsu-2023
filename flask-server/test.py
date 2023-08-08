# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:47:14 2023

@author: hirao
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd


sigmoid=nn.Sigmoid()
loss=nn.BCELoss(reduction='sum')

beta0=0.2
beta1=0
beta2=0
beta3=0.1

beta=torch.tensor([beta0,beta1,beta2,beta3])
print(beta)


X=torch.tensor([1.0,1.0,1.0,1.0])
y=torch.tensor(1.0)


orig_obj=loss(sigmoid(torch.inner(X,beta)),y)+torch.norm(beta,p=1)
print(f"original objective= {orig_obj}")

#######################################################

#same as above but beta0=0
beta0=0

beta=torch.tensor([beta0,beta1,beta2,beta3])
print(beta)


obj=loss(sigmoid(torch.inner(X,beta)),y)+torch.norm(beta,p=1)
print(f"objective beta0=0 {obj}")
print(f"objective change= {orig_obj-obj}")

c1=orig_obj-obj

####################################################

#original but with beta2=1

beta0=0.2
beta2=1

beta=torch.tensor([beta0,beta1,beta2,beta3])
print(beta)


obj=loss(sigmoid(torch.inner(X,beta)),y)+torch.norm(beta,p=1)
print(f"objective beta2=1 {obj}")

print(f"objective change= {orig_obj-obj}")
c2=orig_obj-obj


#####################################

#original with beta0 and beta2 being 1

beta0=0

beta=torch.tensor([beta0,beta1,beta2,beta3])
print(beta)



obj=loss(sigmoid(torch.inner(X,beta)),y)+torch.norm(beta,p=1)
print(f"objective beta0=0 and beta2=1= {obj}")
print(f"objective change= {orig_obj-obj}")


print(f"sum of individual objective changes= {c1+c2}")




