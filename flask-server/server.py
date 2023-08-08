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
import Rademacher
import format_data
import Rashomon
import Rade2
import Step4
import os.path
import step4_model_weights
import step8_model_predictions
import interface_feature_selection


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
                row_dict[csv_data.columns[column]] = "N/A"
            else:
                element_data = row[column]
                if type(row[column]) == np.int64:
                    element_data = row[column].item()
                row_dict[csv_data.columns[column]] = element_data
            
        data_json.append(row_dict)

    training_data = json.dumps(data_json)

    return training_data

def save_step2_data():

    options = webdriver.ChromeOptions()
    options.add_argument("-headless")
    

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
    file_upload.send_keys(os.path.join(os.path.dirname(__file__), "training_data_input.csv"))

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
        index = str(row_data.pop(0))
        row_dict = {}
        row_dict["important_combo"] = row_data[0]
        row_dict["combo_length"] = int(row_data[1])
        row_dict["pos_count"] = int(row_data[2])
        row_dict["neg_count"] = int(row_data[3])
        data_json.append(row_dict)


    data = json.dumps(data_json)
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
    combo_names=list(X_test.columns)


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
        print(combo_names[i])
        print(f"weight: {coef[i]}")



    print(f"intercept= {intercept}")




    dictionary_list=[]
    for i in nonzero_weight_indices:
        dictionary={}
        dictionary["Important_combo"]=combo_names[i]
        dictionary["Weight"]=coef[i]
        dictionary_list.append(dictionary)
            

    json_data = json.dumps(dictionary_list)
    return json_data

def step6_data():
    list_dict = [{'Animal': 'Vulture', 'Score': 0.0003779295526581034, 'Prediction': 0}, {'Animal': 'Dolphin', 'Score': 0.958200951847406, 'Prediction': 1}, {'Animal': 'Penguin', 'Score': 0.0003779295526581034, 'Prediction': 0}, {'Animal': 'Platypus', 'Score': 0.9518695080210506, 'Prediction': 1}, {'Animal': 'Worm', 'Score': 0.00017021114676542243, 'Prediction': 0}]
    json_data = json.dumps(list_dict)
    return json_data

@app.route("/data")
def members():
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
# the flask post request receiver

@app.route('/training_file_upload', methods=['POST'])
def upload_training_file():
    """Handles the upload of a file."""
    d = {}
    try:
        file = request.files['file_from_react']
    
        filename = file.filename
    
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
    
        filename = file.filename
    
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

        json_file = open("step5_feature_selection_data.json")
        step5_json = json.load(json_file)
        json_file.close()

        print(step5_json)

        print(step5_json[0]["current_coef"])

        json_model_data = json.dumps(step5_json)
        with open("step5_feature_selection_data.json", "w") as outfile:
            outfile.write(json_model_data)


        updated_weights = interface_feature_selection.after_selection("binary_combo_data.csv", feature_selected, step5_json[0]["user_added"])

        print(updated_weights)

        d["return"] = updated_weights
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't select feature {e}")
        d['status'] = 0

    return jsonify(d)



@app.route("/step4_data")
def step4_data():
    print("in step4_data")
    binary_data = format_data.binary_combo_data("training_data_input.csv", "step2_data.csv", "train")
    binary_data.to_csv("binary_combo_data.csv")
    if os.path.exists(binary_data.columns[0]+"_step4_data.json"):
        json_file = open(binary_data.columns[0]+"_step4_data.json")
        step4_json = json.load(json_file)
        json_file.close()
        return step4_json
    else:
        print(binary_data.columns[0])
        models_data = Step4.main(Data = binary_data)
        print(models_data)
        prep_plot = []
        for m in models_data:
            for key in m:
                if key in ["Model Name", "x_axis_Rade2", "y_axis_Rade2"]:
                    for index in range(0, len(m["x_axis_Rade2"])):
                        plot_dict = {}
                        plot_dict["ModelName"] = m["Model Name"]
                        plot_dict["xAxis"] = m["x_axis_Rade2"][index]
                        plot_dict["yAxis"] = m["y_axis_Rade2"][index]


                        prep_plot.append(plot_dict)
        
        print(prep_plot)
        print(len(prep_plot))
        plot_file = open("step4_plot_data.csv", "w")
        csv_writer = csv.writer(plot_file)
        csv_writer.writerow(['ModelName', 'xAxis', 'yAxis'])
        for m_dict in prep_plot:
            csv_writer.writerow(m_dict.values())

        plot_file.close()
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


@app.route("/step4_display_selected_model", methods=['POST']) 
def step4_display_selected_model():
  
    print("in step4_display_selected_model")

    d = {}
    print("in user feature selection")
    try:
        model_selected = request.form.get("model_selected")
        print(model_selected)
        
        model_weights = step4_model_weights.main(model_selected)
        print(model_weights)
    
        d["return"] = model_weights
       
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't select model {e}")
        d['status'] = 0

    # return step4_model_weights.main(0)
    return jsonify(d)


@app.route("/step5_features_selection")
def step5_features_selection():

    current_coef = interface_feature_selection.main("binary_combo_data.csv")
    try:
        json_file = open("step5_feature_selection_data.json")
        step5_json = json.load(json_file)
        print(step5_json)
        json_file.close()
        return step5_json[0]["selectable_features"]
    except:
        step5_json = [{
            "current_coef": current_coef,
            "user_added": []
        }]
        json_model_data = json.dumps(step5_json)
        with open("step5_feature_selection_data.json", "w") as outfile:
            outfile.write(json_model_data)


    return step5_json[0]["current_coef"]
    

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
                row_dict[csv_data.columns[column]] = "N/A"
            else:
                element_data = row[column]
                if type(row[column]) == np.int64:
                    element_data = row[column].item()
                row_dict[csv_data.columns[column]] = element_data
            
        data_json.append(row_dict)

    testing_data = json.dumps(data_json)

    return testing_data

@app.route("/step8_data")
def step8_data():
    print("in step8_data")
    binary_data = format_data.binary_combo_data("testing_data_input.csv", "step2_data.csv", "test")
    binary_data.to_csv("binary_combo_data_test.csv")
    if os.path.exists(binary_data.columns[0]+"_step8_data.json"):
        json_file = open(binary_data.columns[0]+"_step8_data.json")
        step4_json = json.load(json_file)
        json_file.close()
        return step4_json
    else:
        print(binary_data.columns[0])
        models_data = Step4.main(Data = binary_data)
        print(models_data)
        prep_plot = []
        for m in models_data:
            for key in m:
                if key in ["Model Name", "x_axis_Rade2", "y_axis_Rade2"]:
                    for index in range(0, len(m["x_axis_Rade2"])):
                        plot_dict = {}
                        plot_dict["ModelName"] = m["Model Name"]
                        plot_dict["xAxis"] = m["x_axis_Rade2"][index]
                        plot_dict["yAxis"] = m["y_axis_Rade2"][index]

                        prep_plot.append(plot_dict)
        
        print(prep_plot)
        print(len(prep_plot))
        plot_file = open("step8_plot_data.csv", "w")
        csv_writer = csv.writer(plot_file)
        csv_writer.writerow(['ModelName', 'xAxis', 'yAxis'])
        for m_dict in prep_plot:
            csv_writer.writerow(m_dict.values())

        plot_file.close()
        json_model_data = json.dumps(models_data)

        with open(binary_data.columns[0]+"_step8_data.json", "w") as outfile:
            outfile.write(json_model_data)

        return models_data


@app.route("/step8_display_selected_model", methods=['POST']) 
def step8_display_selected_model():
    # models = []
    print("in step8_display_selected_model")
    d = {}
    try:
        model_selected = request.form.get("model_selected_step8")
        print(model_selected)
        
        model_predictions = step8_model_predictions.main(model_selected)
        print(model_predictions)
   
        d["return"] = model_predictions
      
        d['status'] = 1

    except Exception as e:
        print(f"Couldn't select model {e}")
        d['status'] = 0


    return jsonify(d)



if __name__ == "__main__":
    app.run(debug=True)