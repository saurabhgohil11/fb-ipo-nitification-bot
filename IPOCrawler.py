from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import DBHelper
import sys
from datetime import datetime
import IPOHelper
import app

req = Request("http://www.chittorgarh.com/ipo/ipo_list.asp", headers={'User-Agent': 'Mozilla/5.0'})

def refreshData():
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    
    x = soup.find('table', { "class" : "table-bordered" })
    headers = x.find_all('th')
    indexheaders = []
    for header in headers:
        indexheaders.append(header.get_text())
    indexheaders.append('link')
    alldata = []
    rows = x.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols)==0:
            continue
        link = row.find('a').get('href')
        rowdata = []
        for col in cols:
            datatoInsert = col.get_text().upper()
            try:
                d = datetime.strptime(datatoInsert, "%b %d, %Y")
                datatoInsert = d.strftime('%Y-%m-%d')
            except:
                #dummt stmnt
                a=10; 
            rowdata.append(datatoInsert)
        rowdata.append(link)
        alldata.append(rowdata)
        
    #log(indexheaders)
    #for row in alldata:
    #    log(row)
    log('check for table existance')
    if not DBHelper.isTableExist():
        log("table not exists") 
        DBHelper.createTable()
    jsonFormat = app.generateJSONResposneForText("Damnn it is not working")
    subscriberList = DBHelper.getUserIdList("1")
    log('sending dummy msg')
    for user in subscriberList:
        log("user is"+user[0])
        app.send_message(user, jsonFormat)
    return IPOHelper.insertNewIPOs(alldata)
    
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()
    