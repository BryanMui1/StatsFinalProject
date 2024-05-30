#!/usr/bin/env python3

'''
Random Sampling Function:
- Choose a random city, a random house, and a random person 
- If the person isnt a working class citizen(age 15 to 64), then redraw
- If participant declines, then redraw
- obtain n = 220 samples
'''

################################################################################################################
## IMPORTS
################################################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import numpy as np
import pandas as pd

import time
import datetime

start_time = time.time()

################################################################################################################
## LOGIN
################################################################################################################

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://islands.smp.uq.edu.au/login.php")

driver.implicitly_wait(1)

email = driver.find_elements(by=By.TAG_NAME, value="input")

login = open('passwords.config', 'r')
usrpass = [line.rstrip('\n') for line in login]


email[0].send_keys(usrpass[1])
email[1].send_keys(usrpass[2])

email[2].click()

logURL = "https://islands.smp.uq.edu.au/index.php"

assert(driver.current_url == logURL)

################################################################################################################
## ENUMERATE CONSTANTS AND GLOBAL VARS(LOAD INDEX DATA TOO)
################################################################################################################

# making dataframe  
df = pd.read_csv("sample_index.csv") 
city_index = df['city_index']
sample_index = df['sample_index']
person_index = df['person_index']

SAMPLE_SIZE = len(df)
people_sampled = 0

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
NUM_CITIES = len(cities)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))

assert(len(buttons) == NUM_CITIES)

# enumerate datavectors
# city = [] #rng_city
# housers = [] #SAMPLE_INDEX
# persons = [] #rng_person

################################################################################################################
## RUNTIME BODY
################################################################################################################

for df_count in range(0, SAMPLE_SIZE):

    ## window check 1
    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Loop through until we find a new window handle
    if driver.current_window_handle == original_window and len(driver.window_handles) > 1:
        driver.close()

    driver.switch_to.window(driver.window_handles[0])

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1
    driver.implicitly_wait(3)

    #reprocess island page
    cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
    buttons = []
    for j in cities:
        buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "towndot towndot")]'))
    click_btn = ActionChains(driver)
    click_btn.move_to_element(buttons[city_index[df_count]])
    click_btn.click()
    click_btn.perform()
    
    ## window check 2
    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Loop through until we find a new window handle
    if driver.current_window_handle == original_window and len(driver.window_handles) > 1:
        driver.close()

    driver.switch_to.window(driver.window_handles[0])

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1
    driver.implicitly_wait(3)    
   

    ### PERFORM SOME TASK HERE ###

    ################################################################################################################
    ## ENUMERATE INDICES
    ################################################################################################################

    houses = driver.find_elements(By.CLASS_NAME, "house")

    ids = driver.find_elements(By.CLASS_NAME, "houseid")
 
    ################################################################################################################
    ## SCRAPE RESIDENT INFORMATION
    ################################################################################################################


    actions = ActionChains(driver)
    ctrl_click = ActionChains(driver)

    # open the desired house

    houses[sample_index[df_count]].click()
 
    ##### TASK START #####

    ## open a random person
    resident_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]')
    num_residents = len(resident_links)

    resident_links[person_index[df_count]].click()
    driver.implicitly_wait(1)

        ### touch some fellas ###
    isl = driver.find_element(By.ID, "title")
    print("touched " + isl.text)
    
    # tab = driver.find_element(By.ID, "t2tab")
    # obtain = driver.find_elements(By.ID, "obtain")
    # if len(obtain) > 0:
    #     print("not obtained")
    # else:
    #     print("obtained")
    # tab.click()
        ### done touching people ###

  
  
    ##### TASK END #####

    ### DONE

    ### close window 
    #driver.switch_to.window(driver.window_handles[0])
    # close = driver.find_element(By.XPATH, '//label[starts-with(@class, "modal__close")]')
    # actions.move_to_element(close).click().perform()
    # driver.implicitly_wait(3)

    ### END TASK//

    island_home = driver.find_element(By.CLASS_NAME, "menu")
    island_home.click()
    driver.implicitly_wait(3)
## Create data frame and write to csv

# data = pd.DataFrame(
#     {
#         "city_index": city,
#         "sample_index": housers,
#         "person_index": persons,
#     }
# )

# print(data.head())

# data.to_csv('sample_index.csv')


end_time = time.time()

if __name__ == '__main__':
    execution_time = end_time - start_time
    print("Script completed normally.")
    print("Script runtime: " + str(datetime.timedelta(seconds=execution_time)))

    time.sleep(10)
    driver.close()