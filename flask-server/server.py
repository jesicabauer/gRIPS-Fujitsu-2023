from flask import Flask
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np
import json
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import l1_min_c
# import pandas as pd


app = Flask(__name__)

def save_step2_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    browser.get("https://widelearning.labs.fujitsu.com/en/trialTool/terms.html")
    browser.fullscreen_window()
    browser.execute_script("window.scrollTo(720, 840)")

    browser.find_element(By.CLASS_NAME, "wl_check_styled").click()

    browser.find_element(By.CLASS_NAME, "btn-inner").click()

    file_upload = browser.find_element(By.CLASS_NAME, "input-btn")
    # file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/defect_prevention_train.csv")
    file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/animals_train.csv")

    browser.find_element(By.CLASS_NAME, "v-btn__content").click()

    button_list = browser.find_elements(By.CLASS_NAME, "v-btn__content")
    print(button_list[len(button_list)-2]) # get the second to last button

    button_list[len(button_list)-2].click()
    time.sleep(5)
    browser.find_element(By.CLASS_NAME, "v-input__append-inner").click()

    browser.find_elements(By.CLASS_NAME, "v-list-item")[-1].click()


    print(browser.page_source)
    df_data = pd.read_html(browser.page_source)

    # df_data[0].to_csv("defect_prevention_train_step2_data.csv")
    df_data[0].to_csv("animal_step2_data.csv")
    return "animal_step2_data.csv"


def csv_to_json(csv_file):
    csv_data = pd.read_csv(csv_file)
    print(csv_data)

    df_list = []
    print(len(csv_data))

    for row_index in range(0, len(csv_data)):
        print(row_index)
        row_list = csv_data.loc[row_index, :].values.flatten().tolist()
        print(row_list)
        df_list.append(row_list)

    print(df_list)

    data_json = []
    for row_data in df_list:
        print(row_data)
        index = str(row_data.pop(0))
        # data_json[index] = row_data
        print(row_data)
        row_dict = {}
        row_dict["important_combo"] = row_data[0]
        row_dict["combo_length"] = int(row_data[1])
        row_dict["pos_count"] = int(row_data[2])
        row_dict["neg_count"] = int(row_data[3])
        # data_json[index] = row_dict
        data_json.append(row_dict)


    print(data_json)

    data = json.dumps(data_json)
    print(data)
    return data

def step3_data():
    list_dict = [{'Important_combo': 'Wings_Does not have ^ Breathes using lungs_Yes ^ Legs<4.5', 'Weight': 1.784704645868965}, {'Important_combo': 'Wings_Does not have ^ Spine_Has ^ Breathes using lungs_Yes', 'Weight': 2.9378455963829655}, {'Important_combo': 'Oviparous_No', 'Weight': 1.57897613658887}, {'Important_combo': 'Hair/fur_Has', 'Weight': 1.8693838614090996}, {'Important_combo': 'Wings_Does not have ^ Eats meat_Yes ^ Breathes using lungs_Yes', 'Weight': 0.5518301318605916}, {'Important_combo': 'Sized about the same as a cat?_No', 'Weight': -2.5825805246885833}, {'Important_combo': 'Hair/fur_Does not have', 'Weight': -3.7211725606849746}, {'Important_combo': 'Oviparous_Yes', 'Weight': -4.1592521866718295}]
    json_data = json.dumps(list_dict)
    return json_data

def step6_data():
    list_dict = [{'Animal': 'Vulture', 'Score': 0.0003779295526581034, 'Prediction': 0}, {'Animal': 'Dolphin', 'Score': 0.958200951847406, 'Prediction': 1}, {'Animal': 'Penguin', 'Score': 0.0003779295526581034, 'Prediction': 0}, {'Animal': 'Platypus', 'Score': 0.9518695080210506, 'Prediction': 1}, {'Animal': 'Worm', 'Score': 0.00017021114676542243, 'Prediction': 0}]
    json_data = json.dumps(list_dict)
    return json_data

@app.route("/data")
def members():
    # number = random.random()
    # return {"data": ["data1", number]}
    csv_file = save_step2_data()
    json_data = csv_to_json(csv_file)

    return json_data


@app.route("/step3")
def step3():

    return step3_data()

@app.route("/step6")
def step6():

    return step6_data()



# @app.route("/lasso")
# def members():
#     #load in training and testing data
#     X_train=pd.read_csv("matrix_format.csv")
#     X_test=pd.read_csv("matrix_format_test.csv")
#     original_train_data=pd.read_csv("animals_train.csv")
#     y_train=original_train_data.iloc[:,-1]


#     #convert data to np, not sure if this is necessary
#     X_train=X_train.to_numpy()
#     X_train=X_train[:,1:] #removing animal name column

#     y_train=y_train.to_numpy()

#     X_test=X_test.to_numpy()
#     X_test=X_test[:,1:] #removing animal name column



#     #finding minimum acceptable C
#     min_C=l1_min_c(X_train,y_train,loss="log")
#     # print(f"minimum acceptable C= {min_C}")
#     #min C=.045


#     #large C=denser beta, small C = sparser beta
#     model=LogisticRegression(penalty="l1",C=1,solver="liblinear",random_state=0) #sets random state for reproducability
#     #model=LogisticRegression(penalty="l1",C=1,solver="saga",random_state=0) #sets random state for reproducability


#     #fit model and display results
#     classifier=model.fit(X_train,y_train)

#     print(classifier.predict(X_test))

#     print(classifier.predict_proba(X_test))

#     print(classifier.coef_)
#     coef=classifier.coef_

#     return coef




if __name__ == "__main__":
    app.run(debug=True)