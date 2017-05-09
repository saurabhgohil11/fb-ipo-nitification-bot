import sys
from logentries import LogentriesHandler
import logging

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)

log.addHandler(LogentriesHandler('06380d85-3900-4507-913b-0b9d4f06f3b7'))


def log(message):  # simple wrapper for MyLogger.logging to stdout on heroku
    print str(message)
    # with open("logs.txt", "a") as myfile:
        # myfile.write(str(datetime.now())+" : "+str(message))
    sys.stdout.flush()
    log.info(message)
