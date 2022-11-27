from selenium.webdriver.chrome.service import Service
from selenium import webdriver

s = Service('C:/Users/Admin/PycharmProjects/pythonProject1/chromedriver/chromedriver.exe')
user_data = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data"
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data}")
driver = webdriver.Chrome(service=s, options=options)