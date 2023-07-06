from flask import Flask
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np
import json

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


@app.route("/data")
def members():
    # number = random.random()
    # return {"data": ["data1", number]}
    csv_file = save_step2_data()
    json_data = csv_to_json(csv_file)

    return json_data




if __name__ == "__main__":
    app.run(debug=True)