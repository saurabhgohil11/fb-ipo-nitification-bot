import app
import IPOCrawler
import IPOHelper
import DBHelper
from pytz import timezone 

asia_culcutta = timezone('Asia/Calcutta')


def start():
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