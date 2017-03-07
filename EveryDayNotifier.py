import app
import IPOCrawler
import IPOHelper
import DBHelper
from pytz import timezone
from apscheduler.scheduler import Scheduler
from datetime import datetime
import sys

asia_culcutta = timezone('Asia/Calcutta')

sched = Scheduler()
sched.start()

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

def start():
    log("start notifier")
    job = sched.add_date_job(doNotify, datetime(2017, 3, 7, 17, 5, 0), ['yo'])
    
def doNotify():
    log("notifing")
    #notify for new listings
    newIPOList = IPOCrawler.refreshData()
    if not newIPOList:
        notifyIPOswithMsg(newIPOList,"Hey, Seems New IPOs are listed.")
        
    #notify Opening Today
    openList = IPOHelper.getOpeningTodayIPO()
    if not list:
        notifyIPOswithMsg(openList,"Knock Knock!! Opening Today!")
           
    #notify closing Today
    closeList = IPOHelper.getClosingTodayIPO()
    if not list:
        notifyIPOswithMsg(closeList,"Hurry up!! Closing Today!")
        
    #notify runningIPO except opening closing
    runningList = IPOHelper.getRunningIPO(True)
    if not list:
        notifyIPOswithMsg(runningList,"Hola, Have you subscribed these Yet?.")
        


def notifyIPOswithMsg(IPOList,message1):
    jsonFormat = app.generateJSONResposneForText(message1)
    subscriberList = DBHelper.getUserIdList("1")
    for user in subscriberList:
        app.send_message(user, jsonFormat)
        
    for ipoData in IPOList:
        notifyIPO(ipoData)


def notifyIPO(ipoData):
    subscriberList = DBHelper.getUserIdList("1")
    for user in subscriberList:
        jsonFormat = app.generateJSONResposneForIPO(ipoData)
        app.send_message(user, jsonFormat)