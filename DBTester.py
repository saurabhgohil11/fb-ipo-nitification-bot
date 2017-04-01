import DBHelper
import IPOCrawler
import MyLogger


def startTest():
    MyLogger.log("start DBTester")
    IPOCrawler.refreshData()
    a = DBHelper.isSchedulerRunning()
    DBHelper.schedulerRunning(True)
    a = DBHelper.isSchedulerRunning()
    DBHelper.schedulerRunning(True)
    a = DBHelper.isSchedulerRunning()
    # MyLogger.log("----------Testing Today's IPO-------------")
    # MyLogger.log(app.formResponse("today"))
    # MyLogger.log("----------Testing Music IPO-------------")
    # MyLogger.log(app.formResponse("IPO MUSIC"))
    # MyLogger.log("----------Testing Current IPO-------------")
    # MyLogger.log(app.formResponse("current"))
    # MyLogger.log("----------Testing 10 IPO-------------")
    # MyLogger.log(app.formResponse("list"))

    MyLogger.log("End DBTester")


startTest()
