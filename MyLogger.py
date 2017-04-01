import sys
from datetime import datetime


def log(message):  # simple wrapper for MyLogger.logging to stdout on heroku
    print str(message)
    with open("logs.txt", "a") as myfile:
        myfile.write(str(datetime.now())+" : "+str(message))
    sys.stdout.flush()
