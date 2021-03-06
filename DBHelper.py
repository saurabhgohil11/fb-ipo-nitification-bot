import sqlite3
import MyLogger
import os
import psycopg2
import urlparse

DB_PATH = "ipocache.db"

WEBINDEX_COMPANY = 0
WEBINDEX_OPEN_DATE = 2
WEBINDEX_CLOSE_DATE = 3
WEBINDEX_OFFER_PRICE = 5
WEBINDEX_ISSUE_TYPE = 1  #deprecated
WEBINDEX_ISSUE_SIZE_CR = 6
WEBINDEX_LINK = 7

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


def createTable():

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

    conn.commit()
    conn.close()

    MyLogger.logMsg("Table created successfully")

def createPrefTable():
    conn2 = sqlite3.connect(DB_PATH)
    c2 = conn2.cursor()
    c2.execute('''CREATE TABLE if not exists PREFS
           (
               NAME TEXT  NOT NULL,
               VALUE         TEXT ,
               PRIMARY KEY (NAME)
           );''')
    c2.execute("INSERT INTO PREFS VALUES ('scheduler_running','0')")
    conn2.commit()
    conn2.close()
    MyLogger.logMsg("setting scheduler start to 0 ")


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
    select_stmt = "SELECT * FROM IPOLIST WHERE COMPANY = '%s' AND OPEN_DATE = '%s'" % (ipoData[WEBINDEX_COMPANY], ipoData[WEBINDEX_OPEN_DATE])
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
    update_stmt = """UPDATE IPOLIST SET CLOSE_DATE = '%s' ,OFFER_PRICE = '%s',ISSUE_TYPE = '%s',ISSUE_SIZE_CR = '%s',LINK = '%s' WHERE COMPANY= '%s' AND OPEN_DATE = '%s'""" % (ipoData[WEBINDEX_CLOSE_DATE],ipoData[WEBINDEX_OFFER_PRICE],ipoData[WEBINDEX_ISSUE_TYPE],ipoData[WEBINDEX_ISSUE_SIZE_CR],ipoData[WEBINDEX_LINK],ipoData[WEBINDEX_COMPANY],ipoData[WEBINDEX_OPEN_DATE])
    c.execute(update_stmt)
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
        insert_stmt = "INSERT INTO IPOLIST VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (ipo[WEBINDEX_COMPANY],ipo[WEBINDEX_OPEN_DATE],ipo[WEBINDEX_CLOSE_DATE],ipo[WEBINDEX_OFFER_PRICE],ipo[WEBINDEX_ISSUE_TYPE],ipo[WEBINDEX_ISSUE_SIZE_CR],ipo[WEBINDEX_LINK])
        c.execute(insert_stmt)
        conn.commit()
        MyLogger.logMsg("ipo " + ipo[WEBINDEX_COMPANY] + "inserted successfully")
        conn.close()
    except psycopg2.IntegrityError:
        MyLogger.logMsg("trying to add duplicate ipo")
        conn.close()

##TODO if user exists remove him
def insertUser(user_id,timestamp):
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
        insert_stmt = "INSERT INTO USERLIST VALUES ('%s','%s','','','','',0)" % (user_id,timestamp)
        c.execute(insert_stmt)
        conn.commit()
        MyLogger.logMsg("user inserted successfully")
        conn.close()
    except psycopg2.IntegrityError:
        MyLogger.logMsg("trying to add duplicate user")
        conn.close()


def getLast6IPO():
    select_stmt = "SELECT * FROM IPOLIST ORDER BY OPEN_DATE DESC LIMIT 6"
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
    MyLogger.logMsg("get user id")
    select_stmt = "SELECT USER_ID FROM USERLIST WHERE IS_ACTIVE = '%s'" % (active)
    list = executeSelect(select_stmt)
    MyLogger.logMsg(list)
    return list

def updateuser(user_id,subscriptionVal):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    update_stmt = "UPDATE USERLIST SET IS_ACTIVE = '%s' WHERE USER_ID = '%s'" % (subscriptionVal, user_id)
    c.execute(update_stmt)
    conn.commit()
    conn.close()
    return

def isSubscribed(user_id):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    select_stmt = "SELECT IS_ACTIVE FROM USERLIST WHERE USER_ID = '%s' AND IS_ACTIVE = '1'" % (user_id)
    c.execute(select_stmt)
    a = c.rowcount
    conn.close()
    if a == 0:
        return False
    else:
        return True

def isUserExists(user_id):
    # conn = sqlite3.connect(DB_PATH)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    c = conn.cursor()
    select_stmt = "SELECT * FROM USERLIST WHERE USER_ID = '%s'" % (user_id)
    c.execute(select_stmt)
    a = c.rowcount
    conn.close()
    if a == 0:
        return False
    else:
        return True


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
    MyLogger.logMsg("Table removed IPO")

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
    MyLogger.logMsg("Table removed user")

def isSchedulerRunning():
    select_stmt = "SELECT * FROM PREFS WHERE NAME = 'scheduler_running'"
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute(select_stmt)
    a = c.fetchone()
    conn.close()
    if a[1] == '1':
        return True
    else:
        return False

def schedulerRunning(value):
    prefVal = '0'
    if value:
        prefVal = '1'
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    update_stmt = """UPDATE PREFS SET VALUE = '%s' WHERE NAME = 'scheduler_running'""" % (prefVal)
    c.execute(update_stmt)
    conn.commit()
    conn.close()
    return
