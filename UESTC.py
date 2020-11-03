import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

browser = webdriver.Chrome(executable_path=path, options=chrome_options)

url = "http://aaa.uestc.edu.cn"

browser.get(url)

form_username = browser.find_element_by_xpath("//input[@id='username']")
form_username.send_keys("*")
form_password = browser.find_element_by_xpath("//input[@id='password']")
form_password.send_keys("*")
form_btn = browser.find_element_by_xpath("//button[@id='school-login']")
form_btn.click()
time.sleep(3)

browser.quit()
