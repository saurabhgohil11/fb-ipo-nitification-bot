import DBHelper
from datetime import datetime
from pytz import timezone 

asia_culcutta = timezone('Asia/Calcutta')

def getTodaysIPO():
    sa_time = datetime.now(asia_culcutta)
    today_date=sa_time.strftime('%Y-%m-%d')
    return DBHelper.getIPObyDate(today_date);
    
def getIPObyName(ipoName):
    return DBHelper.getIPO(ipoName)
    
def getIPObyDate(date):
    return DBHelper.getIPO(date)
    
def getCurrentIPO():
    sa_time = datetime.now(asia_culcutta)
    today_date=sa_time.strftime('%Y-%m-%d')
    return DBHelper.getIPOgreaterThanDate(today_date);
    
def getLast10IPO():
    return DBHelper.getLast10IPO();
