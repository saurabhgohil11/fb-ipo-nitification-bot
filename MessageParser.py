
GREETING_MSG = 0
CURRENT_OR_UPCOMING_IPO = 1
ALL_IPO = 2
TODAYS_IPO = 3
IPO_NAME = 4
IPO_MONTH = 5
REMOVE_ME = 6
UNKNOWN_MSG = -1

grerting_keywords = ['hi','hello','hey','whats','wassup']
curr_keywords = ["current","upcoming"]
all_keywords = ["ipo list","list","all"]
today_keyword = ["day"]
ipo_name = ["ipo"]
ipo_month = ["month"]
remove_me_keyword =["remove me"]

def parse(text):
	text = text.lower()
	if any(x in text for x in grerting_keywords):
		return GREETING_MSG
	elif any(x in text for x in curr_keywords):
		return CURRENT_OR_UPCOMING_IPO
	elif any(x in text for x in all_keywords):
		return ALL_IPO
	elif any(x in text for x in today_keyword):
		return TODAYS_IPO
	elif any(x in text for x in ipo_name):
		return IPO_NAME
	elif any(x in text for x in ipo_month):
		return IPO_MONTH
	elif any(x in text for x in remove_me_keyword):
		return REMOVE_ME
	else:
		return UNKNOWN_MSG
	
def parseIPOName(text):
	text=text.upper()
	return text[3:len(text)].strip()