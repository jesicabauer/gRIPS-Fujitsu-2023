import random_forest_model
import lasso_model
import Perceptron_model
import decision_tree10_model
import decision_tree5_model
import decision_tree3_model
import decision_tree2_model

def main(index):
    models_list = [lasso_model, random_forest_model, Perceptron_model, decision_tree2_model, decision_tree3_model, decision_tree5_model, decision_tree10_model]
    print("in step4 model weights file")
    return models_list[index].weights("binary_combo_data.csv")

    

if __name__ == "__main__":
    main(0)