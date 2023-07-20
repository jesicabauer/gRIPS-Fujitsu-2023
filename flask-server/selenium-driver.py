from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np


# driver_exe = 'chromedriver'
# options = Options()
# options.add_argument("--headless=new")
# browser = webdriver.Chrome(options=options)
options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome.app"
chrome_driver_binary = "/Users/lilyge/Downloads/gRIPS23/chromedriver_mac_arm64/chromedriver"
# options.add_argument('--headless')
# browser = webdriver.Chrome(options=options)
browser = webdriver.Chrome(options=options)

# browser = webdriver.Chrome()

browser.get("https://widelearning.labs.fujitsu.com/en/trialTool/terms.html")
browser.fullscreen_window()
browser.execute_script("window.scrollTo(720, 840)")

time.sleep(3)

browser.find_element(By.CLASS_NAME, "wl_check_styled").click()

time.sleep(2)
browser.find_element(By.CLASS_NAME, "btn-inner").click()

time.sleep(3)

file_upload = browser.find_element(By.CLASS_NAME, "input-btn")
file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/animals_train.csv")
# file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/election_train.csv")
# file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/COVID_train.csv")
# file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/defect_prevention_train.csv")
# file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/iris_train.csv")

time.sleep(3)

browser.find_element(By.CLASS_NAME, "v-btn__content").click()

time.sleep(3)

button_list = browser.find_elements(By.CLASS_NAME, "v-btn__content")
# print(button_list[len(button_list)-2]) # get the second to last button

button_list[len(button_list)-2].click()
time.sleep(5)
browser.find_element(By.CLASS_NAME, "v-input__append-inner").click()

time.sleep(2)
browser.find_elements(By.CLASS_NAME, "v-list-item")[-1].click()

time.sleep(3)

# print(browser.page_source)
df_data = pd.read_html(browser.page_source)

df_data[0].to_csv("/Users/lilyge/Desktop/animal_step2_data.csv")
# df_data[0].to_csv("elections_step2_data.csv")
# df_data[0].to_csv("covid_step2_data.csv")
# df_data[0].to_csv("defect_prevention_train_step2_data.csv")
# df_data[0].to_csv("iris_step2_data.csv")

print("step 2 data saved")
