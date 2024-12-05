from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import json


service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.implicitly_wait(10)

driver.get("https://www.digikala.com/users/login/?backUrl=/treasure-hunt/")


mobile = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/label/div/div/input")
mobile.send_keys("09167363123")
send = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/button")
send.click()

otp = input()
otp_input = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/form/label/div/div/input")
otp_input.send_keys(otp)

sleep(10)

cookies = driver.get_cookies()
cookie_file = open("cookies.json", "w")
json.dump(cookies, cookie_file, indent=2)





