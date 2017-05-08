import os
import json
import IPOCrawler
import MessageParser
import IPOHelper
import DBHelper
import DateUtils
import urllib
import EveryDayNotifier
import MyLogger

import requests
from flask import Flask, request

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
    
def initScheduler():
    MyLogger.log("init scheduler"+str(os.getpid()))
    if os.getpid() == 10:
        MyLogger.log("up starting")
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=startNotifier,
            trigger=IntervalTrigger(hours=24,start_date='2017-05-04 08:40:00',timezone='Asia/Calcutta'),
            id='notifiying_job_morning',
            name='Notifiy at 0840AM',
            replace_existing=True)
        scheduler.add_job(
            func=startNotifier,
            trigger=IntervalTrigger(hours=24,start_date='2017-05-04 13:52:00',timezone='Asia/Calcutta'),
            id='notifiying_job_noon',
            name='Notifiy at 0152PM',
            replace_existing=True)
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

def startNotifier():
    MyLogger.log("startNotifier")
    EveryDayNotifier.doNotify()

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    privacy_policy = '''Last updated: 7th May 2017.
IPO Notifier ("us", "we", or "our") operates this chat bot (the "Site"). This page informs you of our policies regarding the collection, use and disclosure of Personal Information we receive from users of the Site.
We use your Personal Information (i.e fb user id) only for providing and improving the Site. By using the service, you agree to the collection and use of information in accordance with this policy. We do not share this info to anyone. We do not ask about any of your personal Information anywhere. We might log your searches in future but it will be used to improve our services only. If you have any questions about this Privacy Policy, please contact us.
'''
    return privacy_policy, 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    MyLogger.log(data)  # you may not want to MyLogger.log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    timestamp = messaging_event["timestamp"]
                    if not (messaging_event["message"]).get("text"):
                        continue
                    message_text = messaging_event["message"]["text"]  # the message's text
                    if not DBHelper.isUserExists(sender_id):
                        DBHelper.insertUser(sender_id,timestamp)
                    responseList = formResponse(sender_id,message_text)
                    for text in responseList:
                        send_message(sender_id, text)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    timestamp = messaging_event["timestamp"]
                    if not DBHelper.isUserExists(sender_id):
                        DBHelper.insertUser(sender_id, timestamp)
                    payload = messaging_event["postback"]["payload"]  # the message's text
                    responseList = formResponse(sender_id, payload)
                    for text in responseList:
                        send_message(sender_id, text)

    return "ok", 200


def send_message(recipient_id, message):

    MyLogger.log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": 
            json.loads(message)
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        MyLogger.log(r.status_code)
        MyLogger.log(r.text)

def formResponse(sender_id,text):
    msg_type = MessageParser.parse(text)
    responseList = []
    if msg_type==MessageParser.GREETING_MSG:
        message1 = '''Hello, Welcome to IPO Notifier. 
Do you want to Get Notified when new IPO is going to be listed on BSE or NSE?'''

        message2 = '''You can use following Keywords to get IPO details.
1. Upcoming IPO
2. Today's IPO, Current IPO
3. Recent IPO
4. Help.'''
        jsonFormat = generateJSONResposneForPostbackButtons(message1,'Yes, Subscribe Me', 'Subscribe',"No, Don't Notify Me",'Unsubscribe')
        responseList.append(jsonFormat)
        jsonFormat = generateJSONResposneForText(message2)
        responseList.append(jsonFormat)
        
    elif msg_type==MessageParser.UNKNOWN_MSG:
        message1 = "I didn't understand that. Try typing Help :P ."
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)
    
    elif msg_type==MessageParser.HELP:
        
        message1 = '''Use Following Keywords for your task.
1. Upcoming IPO
2. Today's IPO, Current IPO
3. Recent IPO
4. ipo 'Company name'.'''
        message2 = "To get latest IPO updates type 'Subscribe'."
        isSubscribed = DBHelper.isSubscribed(sender_id)
        if isSubscribed:
            message2 = "To unsubscribe type 'Unsubscribe'."
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)
        jsonFormat = generateJSONResposneForText(message2)
        responseList.append(jsonFormat)
               
        
    elif msg_type==MessageParser.UPCOMING_IPO:
        ipolist = IPOHelper.getUpcomingIPO()
        for ipoData in ipolist:
            jsonFormat = generateJSONResposneForIPO(ipoData)
            responseList.append(jsonFormat)
        
    elif msg_type==MessageParser.ALL_IPO:
        ipolist = IPOHelper.getLast10IPO()
        for ipoData in ipolist:
            jsonFormat = generateJSONResposneForIPO(ipoData)
            responseList.append(jsonFormat)
        
    elif msg_type==MessageParser.IPO_NAME:
        ipoName = MessageParser.parseIPOName(text)
        ipolist = IPOHelper.getIPObyName(ipoName)
        if not ipoName:
            ipolist = IPOHelper.getRunningIPO(False)
            msg1 = "Try ipo 'company name'. By the way here is the running IPO List" 
            jsonFormat = generateJSONResposneForText(msg1)
            responseList.append(msg1)
        
        for ipoData in ipolist:
            jsonFormat = generateJSONResposneForIPO(ipoData)
            responseList.append(jsonFormat)
    
    #gives list of running ipo
    elif msg_type==MessageParser.TODAYS_IPO:
        ipolist = IPOHelper.getRunningIPO(False)
        for ipoData in ipolist:
            jsonFormat = generateJSONResposneForIPO(ipoData)
            responseList.append(jsonFormat)

    elif msg_type==MessageParser.UNSUBSCRIBE:
        DBHelper.updateuser(sender_id, '0')
        message1 = "You are successfully unsubscribed. Type 'Subscribe' any time if you want to get updates again."
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)

    elif msg_type==MessageParser.SUBSCRIBE:
        DBHelper.updateuser(sender_id, '1')
        message1 = "You are successfully subscribed. We will notify you for latest IPO news and updates."
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)
            
    if not responseList:
        message1 = "Sorry, No Results Found."
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)
        
    return responseList


    
def generateJSONResposneForText(responsemsg):
    return json.dumps({
        "text": responsemsg
        })

def generateJSONResposneForIPO(ipoData):
    ipoName = ipoData[0]
    openDate = DateUtils.formatReadable(ipoData[1])
    closeDate = DateUtils.formatReadable(ipoData[2])
    price = ipoData[3]
    infoURL = ipoData[6]
    messageStr = ipoName + '\nOpen : ' + openDate + '\nClose : ' + closeDate + '\nPrice : ' + price
    query = urllib.urlencode({'q': ipoName})
    googleURL = "http://www.google.com/search?%s" % query
    
    return json.dumps({
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text": messageStr,
                "buttons":[
                    {
                      "type":"web_url",
                      "url":infoURL,
                      "title":"More Info"
                    },
                    {
                      "type":"web_url",
                      "url":googleURL,
                      "title":"Google It!"
                    },       
                ]
            }
        }
    })

def generateJSONResposneForPostbackButtons(msg,button1,payload1,button2,payload2):
    return json.dumps({
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": msg,
                "buttons": [
                    {
                        "type": "postback",
                        "title": button1,
                        "payload": payload1
                    },
                    {
                        "type": "postback",
                        "title": button2,
                        "payload": payload2
                    },
                ]
            }
        }
    })


def setup_app():
    # All your initialization code
    IPOCrawler.refreshData()


setup_app()  
initScheduler()

if __name__ == '__main__':
    
    app.run(debug=False, use_reloader=False)
