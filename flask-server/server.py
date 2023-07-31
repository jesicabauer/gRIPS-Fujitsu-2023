from flask import Flask
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np
import json
from sklearn.linear_model import LogisticRegression
from sklearn.svm import l1_min_c
import pandas as pd
from flask import request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from io import BytesIO
from flask import jsonify, request
import csv
import io
# from Rademacher import main as RademacherMain
import Rademacher
import format_data
import Rashomon
import Rade2
import combine
import os.path
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager


app = Flask(__name__)

@app.route("/step1_display")
def step1_display():
    csv_data = pd.read_csv("training_data_input.csv")
    print(csv_data)

    df_list = []
    print(len(csv_data))
    print(len(csv_data.columns))

    for row_index in range(0, len(csv_data)):
        print(row_index)
        row_list = csv_data.loc[row_index, :].values.flatten().tolist()
        print(row_list)
        df_list.append(row_list)

    print(df_list)

    data_json = []
    for row in df_list:
        row_dict = {}
        for column in range(0, len(csv_data.columns)):
            if pd.isna(row[column]):
                print("here???")
                row_dict[csv_data.columns[column]] = "N/A"
            else:
                element_data = row[column]
                if type(row[column]) == np.int64:
                    element_data = row[column].item()
                row_dict[csv_data.columns[column]] = element_data
                # print(type(element_data))
            
        data_json.append(row_dict)

    training_data = json.dumps(data_json)

    return training_data

    # for row_index in range(0, len(csv_data)):
    #     print(row_index)
    #     row_list = csv_data.loc[row_index, :].values.flatten().tolist()
    #     print(row_list)
    #     df_list.append(row_list)

    # print(df_list)
    # print(csv_data.columns)

    # data_json = []
    # for row_data in df_list:
    #     # print(row_data)
    #     index = str(row_data.pop(0))

def save_step2_data():
    # print("here1")
    # options = webdriver.ChromeOptions()
    # options.binary_location = "/Applications/Google Chrome.app"
    # chrome_driver_binary = "/Users/lilyge/Downloads/gRIPS23/chromedriver_mac_arm64/chromedriver"
    # print("here2")
    # options.add_argument('--headless')
    # # print("here3")
    # # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # print("here4")
    # browser = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    # options = webdriver.FirefoxOptions()
    # browser = webdriver.Firefox(options=options)

    options = webdriver.ChromeOptions()
    # options.add_argument("-headless")
    

    # Install Webdriver
    service = Service(ChromeDriverManager(version='114.0.5735.90').install())
 
    # Create Driver Instance
    browser = webdriver.Chrome(service=service, options=options)
    browser.get("https://widelearning.labs.fujitsu.com/en/trialTool/terms.html")
    browser.fullscreen_window()
    browser.execute_script("window.scrollTo(720, 840)")

    browser.find_element(By.CLASS_NAME, "wl_check_styled").click()

    browser.find_element(By.CLASS_NAME, "btn-inner").click()

    file_upload = browser.find_element(By.CLASS_NAME, "input-btn")
    # file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/defect_prevention_train.csv")
    # file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/animals_train.csv")
    file_upload.send_keys(os.path.join(os.path.dirname(__file__), "training_data_input.csv"))

    browser.fullscreen_window()
    browser.find_element(By.CLASS_NAME, "v-btn__content").click()

    button_list = browser.find_elements(By.CLASS_NAME, "v-btn__content")
    print(button_list[len(button_list)-2]) # get the second to last button

    button_list[len(button_list)-2].click()
    time.sleep(6)
    browser.execute_script("window.scrollTo(720, 840)")
    browser.find_element(By.CLASS_NAME, "v-input__append-inner").click()

    browser.find_elements(By.CLASS_NAME, "v-list-item")[-1].click()


    print(browser.page_source)
    df_data = pd.read_html(browser.page_source)

    # df_data[0].to_csv("defect_prevention_train_step2_data.csv")
    df_data[0].to_csv("step2_data.csv")
    return "step2_data.csv"


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
    print(csv_data.columns)

    data_json = []
    for row_data in df_list:
        # print(row_data)
        index = str(row_data.pop(0))
        # data_json[index] = row_data
        # print(row_data)
        row_dict = {}
        row_dict["important_combo"] = row_data[0]
        row_dict["combo_length"] = int(row_data[1])
        row_dict["pos_count"] = int(row_data[2])
        row_dict["neg_count"] = int(row_data[3])
        # data_json[index] = row_dict
        data_json.append(row_dict)


    # print(data_json)

    data = json.dumps(data_json)
    # print(data)
    return data

def step3_data():
    #load in training and testing data
    X_train=pd.read_csv("animal_combos_train.csv")
    X_test=pd.read_csv("animal_combos_test.csv")

    #gets lists of names of rows and columns
    train_row_names=list(X_train.iloc[:,0])
    test_row_names=list(X_test.iloc[:,0])


    #get training label vector and remove unnecessary columns
    y_train=X_train.iloc[:,-1]
    X_train=X_train.iloc[:,1:-1] #removing animal name column and label column
    X_test=X_test.iloc[:,1:] #removing animal name column

    #list of all combinations
    combo_names=list(X_test.columns) #TODO: step 3 doesn't have test data yet?


    #finding minimum acceptable C
    min_C=l1_min_c(X_train,y_train,loss="log")
    print(f"minimum acceptable C= {min_C}")


    C_val=20
    n_nonzero=101


    while n_nonzero>100:
        C_val=C_val*.9

        #large C=denser beta, small C = sparser beta
        model=LogisticRegression(penalty="l1",C=C_val,solver="liblinear",random_state=0) #sets random state for reproducability
        #model=LogisticRegression(penalty="l1",C=1,solver="saga",random_state=0) #saga isn't converging with these default parameters
        
        #fit model and display results
        classifier=model.fit(X_train,y_train)
        
        #get coefficients
        coef=classifier.coef_[0]
        nonzero_weight_indices=np.nonzero(coef)[0]
        n_nonzero=len(nonzero_weight_indices)
        #print(f"# of nonzero weights={n_nonzero} with C value {C_val}")

        
    print(f"# of nonzero weights={n_nonzero} with C value {C_val}")

    #save results
    predictions=classifier.predict(X_test)
    probs=classifier.predict_proba(X_test)
    intercept=classifier.intercept_

    #display results

    #predictions
    for i in range(len(test_row_names)):
        print(f"{test_row_names[i]} predicted as {predictions[i]} score={probs[i,1]}")
        

    #important combinations are their weights
    print(f"number of nonzero weights={len(nonzero_weight_indices)}")
    for i in nonzero_weight_indices:
        #print(f"{combo_names[i]   }    weight: {coef[i]}")
        print(combo_names[i])
        print(f"weight: {coef[i]}")



    print(f"intercept= {intercept}")


    #print(f"prediction score if all important combos are zero (just intercept): {1/(1+np.exp(-intercept))}")



    dictionary_list=[]
    for i in nonzero_weight_indices:
        dictionary={}
        dictionary["Important_combo"]=combo_names[i]
        dictionary["Weight"]=coef[i]
        dictionary_list.append(dictionary)
            
        
    # with open("animal_weights.txt", "w") as output:
    #     output.write(str(dictionary_list))


    # pred_dictionary_list=[]

    # for i in range(len(test_row_names)):
    #     dictionary={}
    #     dictionary["Animal"]=test_row_names[i]
    #     dictionary["Score"]=probs[i,1]
    #     dictionary["Prediction"]=predictions[i]
    #     pred_dictionary_list.append(dictionary)

    # with open("animal_predictions.txt", "w") as output:
    #     output.write(str(pred_dictionary_list))





    # list_dict = [{'Important_combo': 'Wings_Does not have ^ Breathes using lungs_Yes ^ Legs<4.5', 'Weight': 1.784704645868965}, {'Important_combo': 'Wings_Does not have ^ Spine_Has ^ Breathes using lungs_Yes', 'Weight': 2.9378455963829655}, {'Important_combo': 'Oviparous_No', 'Weight': 1.57897613658887}, {'Important_combo': 'Hair/fur_Has', 'Weight': 1.8693838614090996}, {'Important_combo': 'Wings_Does not have ^ Eats meat_Yes ^ Breathes using lungs_Yes', 'Weight': 0.5518301318605916}, {'Important_combo': 'Sized about the same as a cat?_No', 'Weight': -2.5825805246885833}, {'Important_combo': 'Hair/fur_Does not have', 'Weight': -3.7211725606849746}, {'Important_combo': 'Oviparous_Yes', 'Weight': -4.1592521866718295}]
    json_data = json.dumps(dictionary_list)
    return json_data

def step6_data():
    # TODO load a saved model from step 3 so no need to rerun when reloaded
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

@app.route("/step4")
def step4():
    return

@app.route("/step6")
def step6():

    return step6_data()

@app.route("/step4_select", methods=['GET', 'POST'])
def user_select():
    sd = ""
    print(request.method)
    if request.method == 'POST':
        sd = ""
        sd = request.form.get('startDate')
        print(request.form)
        
    # print(sd)
    return [{"selected": sd}]
     # print(request.json["testinig"])
    # return [{"hello": "hi"}]
    # todo_data = request.get_json()

# the flask post request receiver

@app.route('/training_file_upload', methods=['POST'])
def upload_training_file():
    """Handles the upload of a file."""
    d = {}
    try:
        file = request.files['file_from_react']
        # stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        # print(stream)
        # csv_input = csv.reader(stream)
        # print(csv_input)
        # save_step2_data(file)
        filename = file.filename
        # print(f"Uploading file {filename}")
        # # print(file.read())
        file_bytes = file.read()
        file_content = BytesIO(file_bytes).readlines()
        print(len(file_content))
        data_list = []
        for b in file_content:
            print(b.decode('utf-8'))
            str_data = b.decode('utf-8')
            data_list.append(str_data)
        print(data_list)
        print("writing csv...")
        csv_file = open('training_data_input.csv', 'w')
        w = csv.writer(csv_file, delimiter = ',')
        w.writerows([x.split(',') for x in data_list])
        csv_file.close()
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)


@app.route('/testing_file_upload', methods=['POST'])
def upload_testing_file():
    """Handles the upload of a file."""
    d = {}
    try:
        file = request.files['file_from_react']
        # stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        # print(stream)
        # csv_input = csv.reader(stream)
        # print(csv_input)
        # save_step2_data(file)
        filename = file.filename
        # print(f"Uploading file {filename}")
        # # print(file.read())
        file_bytes = file.read()
        file_content = BytesIO(file_bytes).readlines()
        print(len(file_content))
        data_list = []
        for b in file_content:
            print(b.decode('utf-8'))
            str_data = b.decode('utf-8')
            data_list.append(str_data)
        print(data_list)
        print("writing csv...")
        csv_file = open('testing_data_input.csv', 'w')
        w = csv.writer(csv_file, delimiter = ',')
        w.writerows([x.split(',') for x in data_list])
        csv_file.close()
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)


@app.route('/user_feature_selection', methods=['POST'])
def user_feature_selection():
    """Handles the upload of a file."""
    d = {}
    print("in user feature selection")
    try:
        feature_selected = request.form.get("feature_selected")
        print(feature_selected)
        # stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        # print(stream)
        # csv_input = csv.reader(stream)
        # print(csv_input)
        # save_step2_data(file)
        # filename = file.filename
        # # print(f"Uploading file {filename}")
        # # # print(file.read())
        # file_bytes = file.read()
        # file_content = BytesIO(file_bytes).readlines()
        # print(len(file_content))
        # data_list = []
        # for b in file_content:
        #     print(b.decode('utf-8'))
        #     str_data = b.decode('utf-8')
        #     data_list.append(str_data)
        # print(data_list)
        # print("writing csv...")
        # csv_file = open('training_data_input.csv', 'w')
        # w = csv.writer(csv_file, delimiter = ',')
        # w.writerows([x.split(',') for x in data_list])
        # csv_file.close()
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't select feature {e}")
        d['status'] = 0

    return jsonify(d)


# @app.route("/rademacher_complexity")
# def rademacher_complexity():
#     print("in rademacher_complexity")
#     binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
#     print(binary_data)
#     return Rademacher.main(Data = binary_data)[1]

# @app.route("/rashomon_accuracy")
# def rashomon_accuracy():
#     print("in rashomon_accuracy")
#     binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
#     print(binary_data)
#     return Rashomon.main(Data = binary_data)[1]

# @app.route("/model_accuracy_complexity")
# def model_accuracy_complexity():
#     binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
#     model_complexity = Rademacher.main(Data = binary_data)[1]
#     model_accuracy = Rashomon.main(Data = binary_data)[1]

#     print(model_complexity)
#     print(model_accuracy)

#     for index in range(0, len(model_complexity)):
#         model_complexity[index]["Accuracy Value"] = model_accuracy[index]["Accuracy Value"]


#     return model_complexity

    # for key in model_complexity:


# @app.route("/complexity_chart")
# def complexity_chart():
#     print("in complexity_chart")
#     binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
#     print(binary_data)
#     return Rademacher.main(Data = binary_data)[0]

# @app.route("/accuracy_chart")
# def accuracy_chart():
#     print("in accuracy_chart")
#     binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
#     print(binary_data)
#     return Rashomon.main(Data = binary_data)[0]

# @app.route("/new_complexity_chart")
# def new_complexity_chart():
#     print("in new_complexity_chart")
#     binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
#     print(binary_data)
#     return Rade2.main(Data = binary_data)

@app.route("/step4_data")
def step4_data():
    print("in step4_data")
    binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
    if os.path.exists(binary_data.columns[0]+"_step4_data.json"):
        json_file = open(binary_data.columns[0]+"_step4_data.json")
        step4_json = json.load(json_file)
        json_file.close()
        return step4_json
    else:
        print(binary_data.columns[0])
        models_data = combine.main(Data = binary_data)
        json_model_data = json.dumps(models_data)

        with open(binary_data.columns[0]+"_step4_data.json", "w") as outfile:
            outfile.write(json_model_data)

        return models_data

@app.route("/step4_saved_data")
def step4_saved_data():
    print("in step4 saved data")
    json_file = open("step4_data.json")
    step4_json = json.load(json_file)
    json_file.close()
    return step4_json

@app.route("/step7_display")
def step7_display():
    csv_data = pd.read_csv("testing_data_input.csv")
    print(csv_data)

    df_list = []
    print(len(csv_data))
    print(len(csv_data.columns))

    for row_index in range(0, len(csv_data)):
        print(row_index)
        row_list = csv_data.loc[row_index, :].values.flatten().tolist()
        print(row_list)
        df_list.append(row_list)

    print(df_list)

    data_json = []
    for row in df_list:
        row_dict = {}
        for column in range(0, len(csv_data.columns)):
            if pd.isna(row[column]):
                print("here???")
                row_dict[csv_data.columns[column]] = "N/A"
            else:
                element_data = row[column]
                if type(row[column]) == np.int64:
                    element_data = row[column].item()
                row_dict[csv_data.columns[column]] = element_data
                # print(type(element_data))
            
        data_json.append(row_dict)

    testing_data = json.dumps(data_json)

    return testing_data

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