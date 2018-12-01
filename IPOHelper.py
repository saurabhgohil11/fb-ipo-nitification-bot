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
    
def getLast6IPO():
    return DBHelper.getLast6IPO()

def insertNewIPOs(ipoList):
    newIPOList = []
    for x in ipoList:
        ipoOpenDate = x[1]
        if not ipoOpenDate:
            continue
        y = DBHelper.hasIPO(x)
        if not y: #new ipo
            DBHelper.insertIPO(x)
            x[1]=x[2]  #temp fix for new ipo notification
            x[2]=x[3]
            x[3]=x[4]
            newIPOList.append(x)
        elif tuple(x)!=y[0]: #new data found for existing ipo
            DBHelper.updateIPO(x)
            x[1]=x[2]  #temp fix for new ipo notification
            x[2]=x[3]
            x[3]=x[4]
            newIPOList.append(x)
    newIPOList = []
    return newIPOList

