import sqlite3
import MyLogger
import os
import psycopg2
import urlparse

DB_PATH = "ipocache.db"

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


def createTable():
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists IPOLIST
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
    c.execute('''CREATE TABLE if not exists USERLIST
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
    
    c.execute('''CREATE TABLE if not exists PREFS
       (
           NAME TEXT  NOT NULL,
           VALUE         TEXT ,
           PRIMARY KEY (NAME)
       );''')

    conn.commit()
    conn.close()

    schedulerRunning('0')
    MyLogger.log("setting scheduler start to 0 ")
    MyLogger.log("Table created successfully")



def isTableExist():
    # select_stmt = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='IPOLIST'"
    # conn = sqlite3.connect(DB_PATH)
    select_stmt = "SELECT true FROM pg_tables WHERE tablename='IPOLIST'"
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    c.execute(select_stmt)
    a = c.fetchone()
    conn.close()
    if a:
        return a[0]
    else:
        return 0

def hasIPO(ipoData):
    select_stmt = "SELECT * FROM IPOLIST WHERE COMPANY = '%s' AND OPEN_DATE = '%s'" % (ipoData[0], ipoData[1])
    return executeSelect(select_stmt)
    
def updateIPO(ipoData):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    c.execute( """UPDATE IPOLIST SET CLOSE_DATE = ? ,OFFER_PRICE = ?,ISSUE_TYPE = ?,ISSUE_SIZE_CR = ?,LINK = ? WHERE COMPANY= ? AND OPEN_DATE = ?""",
                        (ipoData[2],ipoData[3],ipoData[4],ipoData[5],ipoData[6],ipoData[0],ipoData[1]))
    conn.commit()
    conn.close()
    return

def insertIPO(ipo):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    try:
        insert_stmt = "INSERT INTO IPOLIST VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (ipo[0],ipo[1],ipo[2],ipo[3],ipo[4],ipo[5],ipo[6])
        c.execute(insert_stmt)
        conn.commit()
        MyLogger.log("ipo "+ ipo[0] +"inserted successfully")
        conn.close()
    except psycopg2.IntegrityError:
        MyLogger.log("trying to add duplicate ipo")
        conn.close()

##TODO if user exists remove him
def insertUser(user_id):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    try:
        insert_stmt = "INSERT INTO USERLIST VALUES ('%s','','','','','',1)" % (user_id)
        c.execute(insert_stmt)
        conn.commit()
        MyLogger.log("user inserted successfully")
        conn.close()
    except psycopg2.IntegrityError:
        MyLogger.log("trying to add duplicate user")
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
    MyLogger.log("get user id")
    select_stmt = "SELECT USER_ID FROM USERLIST WHERE IS_ACTIVE = '%s'" % (active)
    list = executeSelect(select_stmt)
    MyLogger.log(list)
    return list

def removeuser(user_id):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    c.execute( "UPDATE USERLIST SET IS_ACTIVE = '0' WHERE USER_ID = ?",user_id)
    conn.commit()
    conn.close()
    return

def executeSelect(select_stmt):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    c.execute(select_stmt)
    datalist = c.fetchall()
    conn.close()
    return datalist
    
def dropTableIPO():
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    conn.execute("DROP TABLE IF EXISTS IPOLIST")
    conn.close()
    MyLogger.log("Table removed IPO")
    
def dropTableUser():
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    conn.execute("DROP TABLE IF EXISTS USERLIST")
    conn.close()
    MyLogger.log("Table removed user")
    
def isSchedulerRunning():
    select_stmt = "SELECT * FROM PREFS WHERE NAME = 'scheduler_running'"
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    c.execute(select_stmt)
    a = c.fetchone()
    conn.close()
    if a[1] == '0':
        return False
    else:
        return True
    
def schedulerRunning(value):
    prefVal = '0'
    if value:
        prefVal = '1'
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    c.execute("""UPDATE PREFS SET VALUE = ? WHERE NAME = 'scheduler_running'""",(prefVal))
    conn.commit()
    conn.close()
    return
