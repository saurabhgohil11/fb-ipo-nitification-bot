import DBHelper
import DateUtils

def getOpeningTodayIPO():
    return DBHelper.getIPObyopenDate(DateUtils.getTodaysDate());

def getClosingTodayIPO():
    return DBHelper.getIPObycloseDate(DateUtils.getTodaysDate());

def getRunningIPO(withOutBoundry):
    return DBHelper.getIPOwithinDate(DateUtils.getTodaysDate(),withOutBoundry);
    
def getIPObyName(ipoName):
    return DBHelper.getIPO(ipoName)
    
def getIPObyDate(date):
    return DBHelper.getIPO(date)
    
def getUpcomingIPO():
    return DBHelper.getIPOOpenDateGreaterThanDate(DateUtils.getTodaysDate())
    
def getLast10IPO():
    return DBHelper.getLast10IPO()

def insertNewIPOs(ipoList):
    newIPOList = []
    for x in ipoList:
        ipoOpenDate = x[1]
        if not ipoOpenDate:
            continue
        y = DBHelper.hasIPO(x)
        if not y: #new ipo
            DBHelper.insertIPO(x)
            newIPOList.append(x)
        elif tuple(x)!=y[0]: #new data found for existing ipo
            DBHelper.updateIPO(x)
            newIPOList.append(x)
    return newIPOList

