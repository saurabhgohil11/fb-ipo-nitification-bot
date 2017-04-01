import app
import IPOCrawler
import IPOHelper
import DBHelper
import MyLogger


def doNotify():
    MyLogger.log("doNotify")
    # notify for new listings
    newIPOList = IPOCrawler.refreshData()

    if newIPOList:
        notifyIPOswithMsg(newIPOList, "Hey, Seems New IPOs are listed.")

    # notify Opening Today
    openList = IPOHelper.getOpeningTodayIPO()
    if openList:
        notifyIPOswithMsg(openList, "Knock Knock!! Opening Today!")

    # notify closing Today
    closeList = IPOHelper.getClosingTodayIPO()
    if closeList:
        notifyIPOswithMsg(closeList, "Hurry up!! Closing Today!")

    # notify runningIPO except opening closing
    runningList = IPOHelper.getRunningIPO(True)
    if runningList:
        notifyIPOswithMsg(runningList, "Hola, Have you subscribed these Yet?.")

    notifyIPOswithMsg([], "morning msg bitches")


def notifyIPOswithMsg(IPOList, message1):
    jsonFormat = app.generateJSONResposneForText(message1)
    subscriberList = DBHelper.getUserIdList("1")
    for user in subscriberList:
        MyLogger.log("Notifying user :" + user[0])
        app.send_message(user[0], jsonFormat)
        for ipoData in IPOList:
            jsonFormat = app.generateJSONResposneForIPO(ipoData)
            app.send_message(user[0], jsonFormat)
