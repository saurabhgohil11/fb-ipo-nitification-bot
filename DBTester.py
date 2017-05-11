import DBHelper
import IPOHelper
import MyLogger
import app


def startTest():
    MyLogger.logMsg("**************start DBTester*******************")
    openList = IPOHelper.getOpeningTodayIPO()
    MyLogger.log("------OpenList-------")
    MyLogger.log(openList)

    closeList = IPOHelper.getClosingTodayIPO()
    MyLogger.log("------closeList-------")
    MyLogger.log(closeList)

    runningList = IPOHelper.getRunningIPO(True)
    MyLogger.log("------runningList-------")
    MyLogger.log(runningList)

    subscriberList = DBHelper.getUserIdList("1")
    MyLogger.log("------subscriberList-------")
    MyLogger.log(subscriberList)

    jsonFormat = app.generateJSONResposneForText("DBTested see logs")
    MyLogger.logMsg("Notifying admin")
    app.send_message("1349496018446216", jsonFormat)
    MyLogger.logMsg("**************End DBTester****************")


startTest()
