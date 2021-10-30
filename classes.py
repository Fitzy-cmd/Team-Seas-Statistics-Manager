from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import time
import datetime
from math import *

class Requester():
    def __init__(self, url):
        self.url = url
        self.count = 0

    def updateLiveCount(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome('./drivers/chromedriver',options=option)

        driver.get("https://teamseas.org")
        time.sleep(2.5)
        self.count = driver.find_element_by_id("liveCounter").text
        self.count = self.count.replace(",","")

        print(f"[{self.count}]")

class StatisticsManager():
    def __init__(self):
        self.stats = {}
    
    def openStatsFile(self):
        with open("backgroundVars.txt", "r") as statsFile:
            self.baseStats = statsFile.readlines()
            statsFile.close()
        self.filterStats()
    
    def filterStats(self):
        for line in self.baseStats:
            line = line.strip("\n")
            line = line.split("=")
            self.stats[line[0]] = line[1]
    
    def calculateTotalUpTime(self):
        (startYear, startMonth, startDay, startHour, currentYear, currentMonth, currentDay, currentHour, currentMinute, currentSecond) = self.processDates()
        
        
        startDate = datetime.datetime(int(startYear), int(startMonth), int(startDay), int(startHour), int(0), int(0))
        currentDate = datetime.datetime(int(currentYear), int(currentMonth), int(currentDay), int(currentHour), int(currentMinute), currentSecond)

        timeDifference = currentDate - startDate
        self.uptime = round(timeDifference.total_seconds(),2)
        print(self.uptime)
        self.stats["TOTALUPTIME"] = self.uptime
        self.updateBackgroundVars()
        self.calculateAverage()
        self.calculateTotalAverage()
        self.updateTrackedInfo()
    
    def processDates(self):
        startYear = self.stats["STARTDATE"].split("/")[2]
        startMonth = self.stats["STARTDATE"].split("/")[1]
        startDay = self.stats["STARTDATE"].split("/")[0]
        startHour = self.stats["STARTTIME"]

        currentDateRaw = str(datetime.datetime.now().date())
        currentTimeRaw = str(datetime.datetime.now().time())

        currentDateRaw = currentDateRaw.split("-")
        currentTimeRaw = currentTimeRaw.split(":")

        return (startYear, startMonth, startDay, startHour, currentDateRaw[0], currentDateRaw[1], currentDateRaw[2], currentTimeRaw[0], currentTimeRaw[1], int(round(float(currentTimeRaw[2]),0)))

    def updateBackgroundVars(self):
        with open("backgroundVars.txt", "w+") as file:
            for line in self.stats:
                file.write(f"{line}={self.stats[line]}\n")
            file.close()
    
    def updateTrackedInfo(self):
        with open("trackerInfo/trackedData.txt", "a") as file:
            file.write(f"{self.uptime}|{r.count}|{self.average}|{self.globalAverage}\n")
            file.close()
        
        with open("trackerInfo/averages.txt", "a") as file:
            file.write(str(self.average) + "\n")
            file.close()
    
    def calculateAverage(self):
        totalUptime = self.uptime
        totalCount = r.count
        self.average = round(float(totalCount)/float(totalUptime),2)
    
    def calculateTotalAverage(self):
        totalAverage = 0
        totalCounted = 0
        with open("trackerInfo/averages.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                totalAverage += float(line.strip("\n"))
                totalCounted += 1
            file.close()

        self.globalAverage = round(float(totalAverage/totalCounted),2)


s = StatisticsManager()
s.openStatsFile()
r = Requester("https://teamseas.org")

