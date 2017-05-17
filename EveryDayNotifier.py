import app
import IPOCrawler
import IPOHelper
import DBHelper
import MyLogger
import datetime
import pytz
import os
#from time import sleep

def doNotify():
    MyLogger.logMsg("doNotify")
    # notify for new listings
    newIPOList = IPOCrawler.refreshData()

    my_date = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
    isNoon  = my_date.hour > 12
    MyLogger.logMsg("doNotify isNoon : " +str(isNoon));
    if newIPOList:
        notifyIPOswithMsg(newIPOList, "Hey, Seems New IPOs are listed.")

    # notify Opening Today
    openList = IPOHelper.getOpeningTodayIPO()
    if openList and not isNoon:
        notifyIPOswithMsg(openList, "Knock Knock!! Opening Today!")

    # notify closing Today
    closeList = IPOHelper.getClosingTodayIPO()
    if closeList and isNoon:
        notifyIPOswithMsg(closeList, "Hurry up!! Closing Today!")

    # notify runningIPO except opening closing
    runningList = IPOHelper.getRunningIPO(True)
    if runningList and not isNoon:
        notifyIPOswithMsg(runningList, "Hola, Have you subscribed these Yet?.")

    if not isNoon:
        notifyAdmin("I'm alive.")


def notifyIPOswithMsg(IPOList, message1):
        jsonFormatText = app.generateJSONResposneForText(message1)
        subscriberList = DBHelper.getUserIdList("1")
        for user in subscriberList:
            MyLogger.logMsg("Notifying user :" + user[0])
            app.send_message(user[0], jsonFormatText)
            #sleep(1)
            for ipoData in IPOList:
                jsonFormat = app.generateJSONResposneForIPO(ipoData)
                app.send_message(user[0], jsonFormat)
                #sleep(1)

def notifyAdmin(msg):
    jsonFormat = app.generateJSONResposneForText(msg)
    MyLogger.logMsg("Notifying admin")
    app.send_message(os.environ["ADMIN_ID"], jsonFormat)
