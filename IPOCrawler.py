from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import DBHelper
import sys
from datetime import datetime

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
            datatoInsert = col.get_text()
            try:
                d = datetime.strptime(datatoInsert, "%b %d, %Y")
                datatoInsert = d.date()
            except:
                log("not a date")
            rowdata.append(datatoInsert.upper())
        rowdata.append(link)
        alldata.append(rowdata)
        
    log(indexheaders)
    for row in alldata:
        log(row)
        
    DBHelper.createTable()
    DBHelper.insertIPO(alldata)
    
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

refreshData()