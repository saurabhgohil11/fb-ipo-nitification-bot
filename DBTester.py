import DBHelper
import IPOCrawler
import sys


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

def startTest():
    log("start DBTester")
    IPOCrawler.refreshData()
    a = DBHelper.isSchedulerRunning()
    DBHelper.schedulerRunning(True)
    a = DBHelper.isSchedulerRunning()
    DBHelper.schedulerRunning(True)
    a = DBHelper.isSchedulerRunning()
    #log("----------Testing Today's IPO-------------")
    #log(app.formResponse("today"))
    #log("----------Testing Music IPO-------------")
    #log(app.formResponse("IPO MUSIC"))
    #log("----------Testing Current IPO-------------")
    #log(app.formResponse("current"))
    #log("----------Testing 10 IPO-------------")
    #log(app.formResponse("list"))
    
    log("End DBTester")
    
startTest()