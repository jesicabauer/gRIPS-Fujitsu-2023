from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np

browser = webdriver.Chrome()

browser.get("https://widelearning.labs.fujitsu.com/en/trialTool/terms.html")
browser.fullscreen_window()
browser.execute_script("window.scrollTo(720, 840)")

time.sleep(5)

browser.find_element(By.CLASS_NAME, "wl_check_styled").click()

time.sleep(2)
browser.find_element(By.CLASS_NAME, "btn-inner").click()

time.sleep(5)

file_upload = browser.find_element(By.CLASS_NAME, "input-btn")
file_upload.send_keys("/Users/lilyge/Downloads/gRIPS23/animals_train.csv")

# time.sleep(10)

browser.find_element(By.CLASS_NAME, "v-btn__content").click()

button_list = browser.find_elements(By.CLASS_NAME, "v-btn__content")
print(button_list[len(button_list)-2]) # get the second to last button

button_list[len(button_list)-2].click()
time.sleep(5)
browser.find_element(By.CLASS_NAME, "v-input__append-inner").click()

time.sleep(2)
browser.find_elements(By.CLASS_NAME, "v-list-item")[-1].click()

time.sleep(10)

print(browser.page_source)
df_data = pd.read_html(browser.page_source)

df_data[0].to_csv("step2_data.csv")
