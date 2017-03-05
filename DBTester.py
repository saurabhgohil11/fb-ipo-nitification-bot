import DBHelper
import os
import IPOHelper
import app
import sys

print "start DBTester"
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

DBHelper.dropTableIPO()
DBHelper.dropTableUser()
if not(os.path.isfile('ipocache.db')):
    log("DB not exist crawling data and creating DB")
    IPOCrawler.refreshData()
    log("DONE: DB not exist crawling data and creating DB")

log("----------Testing Today's IPO-------------")
log(formResponse("today"))
log("----------Testing Music IPO-------------")
log(formResponse("IPO MUSIC"))
log("----------Testing Current IPO-------------")
log(formResponse("current"))
log("----------Testing 10 IPO-------------")
log(formResponse("list"))

print "End DBTester"