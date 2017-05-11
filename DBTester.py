import app
import DBHelper
import IPOHelper
import MyLogger
import EveryDayNotifier


def startTest():
    MyLogger.logMsg("**************start DBTester*******************")
    openList = IPOHelper.getOpeningTodayIPO()
    MyLogger.logMsg("------OpenList-------")
    MyLogger.logMsg(openList)

    closeList = IPOHelper.getClosingTodayIPO()
    MyLogger.logMsg("------closeList-------")
    MyLogger.logMsg(closeList)

    runningList = IPOHelper.getRunningIPO(True)
    MyLogger.logMsg("------runningList-------")
    MyLogger.logMsg(runningList)

    subscriberList = DBHelper.getUserIdList("1")
    MyLogger.logMsg("------subscriberList-------")
    MyLogger.logMsg(subscriberList)

    jsonFormat = app.generateJSONResposneForText("DB Test Done")
    MyLogger.logMsg("Notifying admin")
    app.send_message("1349496018446216", jsonFormat)
    MyLogger.logMsg("**************End DBTester****************")


def notifyUpcomingIPOs():
    ipolist = IPOHelper.getUpcomingIPO();
    if ipolist:
        EveryDayNotifier.notifyIPOswithMsg(ipolist, "Here are some upcoming IPOs")