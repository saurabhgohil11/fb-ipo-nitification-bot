import sqlite3
import sys

DB_PATH = "ipocache.db"

def createTable():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE if not exists IPOLIST
       (
           COMPANY TEXT  NOT NULL,
           OPEN_DATE         TEXT ,
           CLOSE_DATE        TEXT,
           OFFER_PRICE       TEXT,
           ISSUE_TYPE        TEXT,
           ISSUE_SIZE_CR     TEXT,
           LINK                 TEXT,
           PRIMARY KEY (COMPANY, OPEN_DATE)
       );''')
    conn.execute('''CREATE TABLE if not exists USERLIST
       (
           USER_ID TEXT  NOT NULL,
           ADD_DATA1         TEXT ,
           ADD_DATA2        TEXT,
           ADD_DATA3       TEXT,
           ADD_DATA4        TEXT,
           ADD_DATA5     TEXT,
           IS_ACTIVE    INT,
           PRIMARY KEY (USER_ID)
       );''')
    log("Table created successfully");

    conn.close()

def isTableExist():
    select_stmt = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='IPOLIST'"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(select_stmt)
    a = c.fetchone()
    conn.close()
    return a[0]

def hasIPO(ipoData):
    select_stmt = "SELECT * FROM IPOLIST WHERE COMPANY = '%s' AND OPEN_DATE = '%s'" % (ipoData[0], ipoData[1])
    return executeSelect(select_stmt)
    
def updateIPO(ipoData):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute( """UPDATE IPOLIST SET CLOSE_DATE = ? ,OFFER_PRICE = ?,ISSUE_TYPE = ?,ISSUE_SIZE_CR = ?,LINK = ? WHERE COMPANY= ? AND OPEN_DATE = ?""",
                        (ipoData[2],ipoData[3],ipoData[4],ipoData[5],ipoData[6],ipoData[0],ipoData[1]))
    conn.commit()
    conn.close()
    return

def insertIPO(ipo):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO IPOLIST VALUES (?,?,?,?,?,?,?)', ipo)
        conn.commit()
        log("ipo "+ ipo[0] +"inserted successfully");
    except sqlite3.IntegrityError:
        log("trying to add duplicate ipo")
    conn.close()

##TODO if user exists remove him
def insertUser(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO USERLIST VALUES (?,'','','','','',1)", [user_id])
        conn.commit()
        log("user inserted successfully");
    except sqlite3.IntegrityError:
        log("trying to add duplicate user")
    conn.close()


def getLast10IPO():
    select_stmt = "SELECT * FROM IPOLIST ORDER BY OPEN_DATE DESC LIMIT 10"
    return executeSelect(select_stmt)
    
#Provide IPO Name in UPPER CASE ONLY    
def getIPO(ipoName):
    select_stmt = "SELECT * FROM IPOLIST WHERE COMPANY LIKE '%"+ipoName+"%'"
    return executeSelect(select_stmt)
    
#date fore mate 2017-12-30
def getIPObyopenDate(date):
    select_stmt = "SELECT * FROM IPOLIST WHERE OPEN_DATE = '%s'" % (date)
    return executeSelect(select_stmt)

#date fore mate 2017-12-30
def getIPObycloseDate(date):
    select_stmt = "SELECT * FROM IPOLIST WHERE CLOSE_DATE = '%s'" % (date)
    return executeSelect(select_stmt)

def getIPOwithinDate(date,withOutBoundry):
    select_stmt = "SELECT * FROM IPOLIST WHERE OPEN_DATE <= '%s' AND CLOSE_DATE >= '%s'" % (date,date)
    if withOutBoundry:
        select_stmt = "SELECT * FROM IPOLIST WHERE OPEN_DATE < '%s' AND CLOSE_DATE > '%s'" % (date,date)
    return executeSelect(select_stmt)

def getCurrentAndUpcomingIPO(date):
    select_stmt = "SELECT * FROM IPOLIST WHERE OPEN_DATE >= '%s' OR CLOSE_DATE >= '%s'" % (date,date)
    return executeSelect(select_stmt)

def getIPOOpenDateGreaterThanDate(date):
    select_stmt = "SELECT * FROM IPOLIST WHERE OPEN_DATE > '%s'" % (date)
    return executeSelect(select_stmt)

def getUserIdList(active):
    log("get user id")
    select_stmt = "SELECT USER_ID FROM USERLIST WHERE IS_ACTIVE = '%s'" % (active)
    list = executeSelect(select_stmt)
    log(list)
    return list

def removeuser(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute( "UPDATE USERLIST SET IS_ACTIVE = '0' WHERE USER_ID = ?",user_id)
    conn.commit()
    conn.close()
    return

def executeSelect(select_stmt):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(select_stmt)
    datalist = c.fetchall()
    conn.close()
    return datalist
    
def dropTableIPO():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS IPOLIST")
    conn.close()
    log("Table removed IPO")
    
def dropTableUser():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS USERLIST")
    conn.close()
    log("Table removed user")
    
    
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()
