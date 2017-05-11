import DBHelper
import IPOHelper
import MyLogger
import app


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

    jsonFormat = app.generateJSONResposneForText("DBTested see logs")
    MyLogger.logMsg("Notifying admin")
    app.send_message("1349496018446216", jsonFormat)
    MyLogger.logMsg("**************End DBTester****************")


startTest()
