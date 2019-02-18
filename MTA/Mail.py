# Title: DBMS
# Author: K Nitesh Srivats
# Date: 01/06/2018

import os
import time
import pandas as pd
import keyboard
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


def tabs(driver, n):
    ActionChains(driver).send_keys(Keys.TAB*n).perform()
    time.sleep(0.1)


def click(driver, identifier):
    try:
        element = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, identifier)))
        element = driver.find_element_by_xpath(identifier).click()
    except TimeoutException:
        element = driver.find_element_by_xpath(identifier).click()


def tabfill(driver, string, n):
    ActionChains(driver).send_keys(Keys.TAB*n).perform()
    keyboard.write(str(string))
    time.sleep(0.2)


def tabenter(driver, n):
    ActionChains(driver).send_keys(Keys.TAB * n).perform()
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(0.2)


def down(driver, n):
    ActionChains(driver).send_keys(Keys.ARROW_DOWN*n).perform()
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    time.sleep(0.2)


def wait(driver, identifier):
    element = WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, identifier)))


def main():
    form = pd.read_csv(os.path.join(os.getcwd(), "Form.csv"))
    todo = pd.read_excel(os.path.join(os.getcwd(), "Mail_todo.xlsx"))
    done = form
    done["Done"] = pd.Series()
    done.fillna("No", inplace=True)

    username = "@gmail.com"
    password = ""
    subject = "Mail Test IEEE"
    file = open("Content.txt")
    content = ""
    for i in file:
        content += i

    todo["Path"].iloc[1] = username
    todo["Path"].iloc[4] = password
    todo["Path"].iloc[15] = subject
    todo["Path"].iloc[19] = content

    exe_path = os.path.join(os.getcwd(), "chromedriver.exe")
    driver = webdriver.Chrome(executable_path=exe_path)
    driver.implicitly_wait(30)
    driver.get("https://www.google.com/intl/en-GB/gmail/about/#")
    driver.maximize_window()

    for i in range(len(todo)):
        task = todo["Task"].iloc[i]
        path = todo["Path"].iloc[i]
        if task == "Sleep":
            time.sleep(path)
        elif task == "Tab":
            tabs(driver, path)
        elif task == "Click":
            click(driver, path)
        elif task == "TabEnter":
            tabenter(driver, path)
        elif task == "Enter":
            ActionChains(driver).send_keys(Keys.RETURN).perform()
        elif task == "Email":
            for j in range(len(form)):
                if done["Done"].iloc[j] != "Yes":
                    keyboard.write(form["Username"].iloc[j])
                    keyboard.write(" ")
                    done["Done"] = "Yes"
                    time.sleep(0.2)
        elif task == "Keyboard":
            keyboard.write(todo["Path"].iloc[i])
            time.sleep(0.5)
        elif task == "BCC":
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('shift')
            pyautogui.keyDown('b')
            time.sleep(0.01)
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('shift')
            pyautogui.keyUp('b')

    done.to_excel("Sent_Mails.xlsx", index=False)

    
if __name__ == "__main__":
    main()
