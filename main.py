from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import time

class Requester():
    def __init__(self, url):
        self.url = url

    def updateLiveCount(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome('./drivers/chromedriver',options=option)

        driver.get("https://teamseas.org")
        time.sleep(2.5)
        self.count = driver.find_element_by_id("liveCounter").text

        print(f"[{self.count}]")