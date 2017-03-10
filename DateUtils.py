from datetime import datetime
from pytz import timezone 

asia_culcutta = timezone('Europe/Amsterdam')

def formatComparable(dateStr):
    try:
        d = datetime.strptime(dateStr, "%b %d, %Y")
        return d.strftime('%Y-%m-%d')
    except:
        return dateStr

def formatReadable(dateStr):
    try:
        d = datetime.strptime(dateStr, '%Y-%m-%d')
        return d.strftime("%b %d, %Y")
    except:
        return dateStr
    
def getTodaysDate():
    sa_time = datetime.now(asia_culcutta)
    return sa_time.strftime('%Y-%m-%d')
    