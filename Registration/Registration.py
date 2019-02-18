# Title: DBMS
# Author: K Nitesh Srivats
# Date: 15/08/2018

import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def drop_down(driver, xpath, tabs):
    element = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    element = driver.find_element_by_xpath(xpath).click()
    time.sleep(2)
    for i in range(tabs):
        element.send_keys(Keys.ARROW_DOWN)
    element.send_keys(Keys.RETURN)


def click(driver, xpath):
    element = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    element = driver.find_element_by_xpath(xpath).click()


def fill(driver, xpath, string):
    element = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    element = driver.find_element_by_xpath(xpath).send_keys(string)


def preprocessing(form):
    form.fillna(0, inplace=True)
    form.drop(["Timestamp"], axis=1, inplace=True)
    form = form.rename(
        columns={"Phone Number (WhatsApp Enabled)": "Phone Number",
                 "Expected Graduation Year": "Graduation Year"}
    )
    form["Password"] = pd.Series()
    form["City"] = "Bangalore"
    form["Pincode"] = "560003"
    form["College"] = "b.m"
    form["Address Line 1"] = "B.M.S. College of Engineering"
    form["Address Line 2"] = "P.O. Box No.: 1908, Bull Temple Road"
    for i in range(len(form)):
        j = 4
        k = 0
        password = ""
        if len(form["First Name"].iloc[i]) - \
                form["First Name"].iloc[i].count(' ') > 3:
            while j > 0:
                if form["First Name"].iloc[i][k] != ' ':
                    password += form["First Name"].iloc[i][k]
                    k = k + 1
                    j = j - 1
                else:
                    k = k + 1
        elif (len(form["Last Name"].iloc[i])-form["Last Name"].iloc[i].count(' ')) > 3:
            while j > 0:
                if form["Last Name"].iloc[i][k] != ' ':
                    password += form["Last Name"].iloc[i][k]
                    k = k + 1
                    j = j - 1
                else:
                    k = k + 1
        else:
            print(form["First Name"].iloc[i], form["Last Name"].iloc[i])

        if len(str(form["Phone Number"].iloc[i])) == 10:
            while j > -4:
                j = j - 1
                password += str(form["Phone Number"].iloc[i])[j]
        else:
            print(form["First Name"].iloc[i], form["Last Name"].iloc[i])
        form["Password"].iloc[i] = password
        form["Phone Number"].iloc[i] = "+91" + str(form["Phone Number"].iloc[i])
    form.to_csv("list.csv", index=False)
    return form


def main():
    todo = pd.read_excel(os.path.join(os.getcwd(), "todo.xlsx"))
    form = pd.read_csv(os.path.join(os.getcwd(), "Form.csv"))
    exe_path = os.path.join(os.getcwd(), "chromedriver.exe")
    form = preprocessing(form)
    for k in range(len(form)):
        driver = webdriver.Chrome(executable_path=exe_path)
        # Waits
        driver.implicitly_wait(10)
        
        driver.get("https://www.ieee.org/")
        for i in range(len(todo)):
            print(todo["Field"].iloc[i])
            if todo["Type"].iloc[i] == "Click":
                click(driver, todo["Identifier"].iloc[i])
            elif todo["Type"].iloc[i] == "Type":
                fill(driver,
                     todo["Identifier"].iloc[i],
                     form[todo["Form Field"].iloc[i]].iloc[k])
            elif todo["Type"].iloc[i] == "Down":
                drop_down(driver,
                          todo["Identifier"].iloc[i],
                          todo["Form Field"].iloc[i])
            elif todo["Type"].iloc[i] == "Time":
                time.sleep(todo["Form Field"].iloc[i])


if __name__ == '__main__':
    main()
