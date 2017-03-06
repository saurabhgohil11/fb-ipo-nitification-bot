import os
import sys
import json
import IPOCrawler
import MessageParser
import IPOHelper
import DBHelper
import DateUtils

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    DBHelper.insertUser(sender_id)
                    responseList = formResponse(message_text)
                    for text in responseList:
                        send_message(sender_id, text)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message))

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
        log(r.status_code)
        log(r.text)

def formResponse(text):
    msg_type = MessageParser.parse(text)
    responseList = []
    if msg_type==MessageParser.GREETING_MSG:
        message1 = '''Hello, Welcome to IPO Notifier. 
We will message you on when ever a new IPO is going to be listed on BSE or NSE. Do not delete this chat if you want to get notified.'''
        
        message2 = '''Use Following Keywords for your task.
1. Current IPO
2. Today's IPO, IPO Of the Day
3. IPO List
4. ipo 'Company name'.'''
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)
        jsonFormat = generateJSONResposneForText(message2)
        responseList.append(jsonFormat)
        
    elif msg_type==MessageParser.UNKNOWN_MSG:
        message1 = "I didn't understand that. Try typing Help :P ."
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)
    
    elif msg_type==MessageParser.HELP:
        
        message1 = '''Use Following Keywords for your task.
1. Current IPO
2. Today's IPO, IPO Of the Day
3. IPO List
4. ipo 'Company name'.'''
        message2 = "If you don't want to unsubscribe type Remove Me and delete this chat."
        jsonFormat = generateJSONResposneForText(message1)
        responseList.append(jsonFormat)
        jsonFormat = generateJSONResposneForText(message2)
        responseList.append(jsonFormat)
               
        
    elif msg_type==MessageParser.CURRENT_OR_UPCOMING_IPO:
        ipolist = IPOHelper.getCurrentIPO()
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
            ipolist = IPOHelper.getCurrentIPO() 
        
        for ipoData in ipolist:
            jsonFormat = generateJSONResposneForIPO(ipoData)
            responseList.append(jsonFormat)
    
    #gives list of running ipo
    elif msg_type==MessageParser.TODAYS_IPO:
        ipolist = IPOHelper.getRunningIPO()
        for ipoData in ipolist:
            jsonFormat = generateJSONResposneForIPO(ipoData)
            responseList.append(jsonFormat)

    return responseList
    

def notifyNewIPO(ipoData):
    subscriberList = DBHelper.getUserIdList("1")
    for user in subscriberList:
        prettyFormat = generateJSONResposneForIPO(ipoData)
        send_message(user, prettyFormat)
    
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
                    }
                ]
            }
        }
    })
  

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()
    
def setup_app(app):
    # All your initialization code
    if not(os.path.isfile('ipocache.db')):
        log("DB not exist crawling data and creating DB")
        IPOCrawler.refreshData()
        log("DONE: DB not exist crawling data and creating DB")

setup_app(app)

if __name__ == '__main__':
    setup_app(app)
    app.run(debug=True)
