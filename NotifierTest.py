import IPOCrawler
import IPOHelper
import DBHelper
import DateUtils
import json

def notifyIPOswithMsg(IPOList,message1):
    jsonFormat = generateJSONResposneForText(message1)
    subscriberList = DBHelper.getUserIdList("1")
    for user in subscriberList:
        print("Notifying user :"+user[0])
        
        
    for ipoData in IPOList:
        notifyIPO(ipoData)


def notifyIPO(ipoData):
    subscriberList = DBHelper.getUserIdList("1")
    for user in subscriberList:
        jsonFormat = generateJSONResposneForIPO(ipoData)
        print(jsonFormat)
        
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
    query = 'Test'#urllib.urlencode({'q': ipoName})
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
    
    
newIPOList = IPOCrawler.refreshData()
    
if newIPOList:
    notifyIPOswithMsg(newIPOList,"Hey, Seems New IPOs are listed.")
    
#notify Opening Today
openList = IPOHelper.getOpeningTodayIPO()
if openList:
    notifyIPOswithMsg(openList,"Knock Knock!! Opening Today!")
       
#notify closing Today
closeList = IPOHelper.getClosingTodayIPO()
if closeList:
    notifyIPOswithMsg(closeList,"Hurry up!! Closing Today!")
    
#notify runningIPO except opening closing
runningList = IPOHelper.getRunningIPO(True)
if runningList:
    notifyIPOswithMsg(runningList,"Hola, Have you subscribed these Yet?.")
DBHelper.removeuser("2")