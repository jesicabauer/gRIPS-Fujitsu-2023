import random_forest_model
import lasso_model
import Perceptron_model
import decision_tree10_model
import decision_tree5_model
import decision_tree3_model
import decision_tree2_model
import logistic_regression_model
import GaussianNB_model
import SVM_model

def main(index):
    print("in step8_model_predictions py file")
    print(index)
    models_list = {"Lasso": lasso_model, 
                   "RF": random_forest_model, 
                   "PT": Perceptron_model, 
                   "DT2": decision_tree2_model, 
                   "DT3": decision_tree3_model, 
                   "DT5": decision_tree5_model, 
                   "DT10": decision_tree10_model,
                   "LR2": logistic_regression_model,
                    "NB": GaussianNB_model,
                   "SVM": SVM_model
                   }
    print("in step8 model weights file")
    return models_list[index].predictions("binary_combo_data_test.csv")

    

if __name__ == "__main__":
    main(0)