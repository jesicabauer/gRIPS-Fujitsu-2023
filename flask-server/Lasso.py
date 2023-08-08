
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle


def Lasso(train_data ,test_data):

    #train_data = pd.DataFrame(train_data)
    #test_data = pd.DataFrame(test_data)
    
    
    train_data=pd.read_csv(train_data) 
    test_data=pd.read_csv(test_data)    

    
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
    
    #save model
    filename="lasso_file.sav"
    pickle.dump(classifier,open(filename,'wb'))
    

    return predictions    





pred=Lasso("animal_combos_train.csv","animal_combos_test.csv")


#lasso_classifier=pickle.loads(lasso_model)

#s = pickle.dumps(clf)
#clf2 = pickle.loads(s)