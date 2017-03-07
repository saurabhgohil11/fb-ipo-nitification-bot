import DBHelper
import DateUtils

def getOpeningTodayIPO():
    
    return DBHelper.getIPObycloseDate(DateUtils.getTodaysDate());

def getClosingTodayIPO():
    return DBHelper.getIPObycloseDate(DateUtils.getTodaysDate());

def getRunningIPO(withOutBoundry):
    return DBHelper.getIPOwithinDate(DateUtils.getTodaysDate(),withOutBoundry);
    
def getIPObyName(ipoName):
    return DBHelper.getIPO(ipoName)
    
def getIPObyDate(date):
    return DBHelper.getIPO(date)
    
def getCurrentIPO():
    return DBHelper.getIPOgreaterThanDate(DateUtils.getTodaysDate())
    
def getLast10IPO():
    return DBHelper.getLast10IPO()

def insertNewIPOs(ipoList):
    newIPOList = []
    for x in ipoList:
        if not DBHelper.hasIPO(x):
            DBHelper.insertIPO(x)
            newIPOList.append(x)
    
    return newIPOList

