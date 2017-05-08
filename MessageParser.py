GREETING_MSG = 0
UPCOMING_IPO = 1
ALL_IPO = 2
TODAYS_IPO = 3
IPO_NAME = 4
IPO_MONTH = 5
UNSUBSCRIBE = 6
SUBSCRIBE = 7
UNKNOWN_MSG = -1
HELP = 7

greeting_keywords = ['hi', 'hello', 'hey', 'whats', 'wassup']
curr_keywords = ["upcoming"]
all_keywords = ["ipo list", "list", "all"]
today_keyword = ["today", "current"]
ipo_name = ["ipo"]
ipo_month = ["month"]
unsubscribe_keyword = ["remove me", "unsubscribe"]
subscribe_keyword = ["subscribe"]
help_keyword = ["help"]


def parse(text):
    text = text.lower()
    if any(x in text for x in greeting_keywords):
        return GREETING_MSG
    elif any(x in text for x in curr_keywords):
        return UPCOMING_IPO
    elif any(x in text for x in all_keywords):
        return ALL_IPO
    elif any(x in text for x in today_keyword):
        return TODAYS_IPO
    elif any(x in text for x in ipo_name):
        return IPO_NAME
    elif any(x in text for x in ipo_month):
        return IPO_MONTH
    elif any(x in text for x in unsubscribe_keyword):
        return UNSUBSCRIBE
    elif any(x in text for x in subscribe_keyword):
        return SUBSCRIBE
    elif any(x in text for x in help_keyword):
        return HELP
    else:
        return UNKNOWN_MSG


def parseIPOName(text):
    text = text.upper()
    return text[3:len(text)].strip()
