from datetime import datetime

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