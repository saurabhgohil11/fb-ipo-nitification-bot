import sqlite3
import sys

def createTable():
    conn = sqlite3.connect('ipocache.db')
    a = conn.execute('''CREATE TABLE if not exists IPOLIST
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
    b = conn.execute('''CREATE TABLE if not exists USERLIST
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
    
def insertIPO(listOfIPO):
    conn = sqlite3.connect('ipocache.db')
    c = conn.cursor()
    try:
        c.executemany('INSERT INTO IPOLIST VALUES (?,?,?,?,?,?,?)', listOfIPO)
        conn.commit()
        log("ipo inserted successfully");
    except sqlite3.IntegrityError:
        log("trying to add duplicates")
    conn.close()
    
def insertUser(user_id):
    conn = sqlite3.connect('ipocache.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO USERLIST VALUES (?,'','','','','',1)", [user_id])
        conn.commit()
        log("user inserted successfully");
    except sqlite3.IntegrityError:
        log("trying to add duplicate user")
    conn.close()


def getLast10IPO():
    select_stmt = "SELECT * FROM IPOLIST order by OPEN_DATE DESC limit 10"
    return executeSelect(select_stmt)
    
#Provide IPO Name in UPPER CASE ONLY    
def getIPO(ipoName):
    select_stmt = "SELECT * FROM IPOLIST WHERE COMPANY LIKE '%"+ipoName+"%'"
    return executeSelect(select_stmt)
    
#date fore mate 2017-12-30
def getIPObyDate(date):
    select_stmt = "SELECT * FROM IPOLIST WHERE OPEN_DATE = '%s' OR CLOSE_DATE = '%s'" % (date, date)
    return executeSelect(select_stmt)

def getIPOgreaterThanDate(date):
    select_stmt = "SELECT * FROM IPOLIST WHERE OPEN_DATE >= '%s' OR CLOSE_DATE >= '%s'" % (date,date)
    return executeSelect(select_stmt)
    

def getUserIdList(active):
    select_stmt = "SELECT USER_ID FROM USERLIST WHERE IS_ACTIVE = '%s'" % (active)
    return executeSelect(select_stmt)

def executeSelect(select_stmt):
    conn = sqlite3.connect('ipocache.db')
    c = conn.cursor()
    c.execute(select_stmt)
    list = c.fetchall()
    conn.close()
    return list
    
    
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()
