import re
import base64
import datetime 

def find_nc(website):
	websiteCopy = website
	regex = "<input type=\"hidden\" name=\"nc\" value=\"(.*?)\">"
	nc = re.search(regex, websiteCopy)
	if nc == None:
		print("Error: nc number could not be found, please try again")
		return -1
	else:
		return nc.group(1)

def find_Challenge(website):
	websiteCopy = website
	regex = "<input type=\"hidden\" name=\"challenge\" value=\"(.*?)\">"
	challenge = re.search(regex, websiteCopy)
	if challenge == None:
		print("Error: Challenge number could not be found, please try again")
		return -1
	else:
		return challenge.group(1)

def get_Captcha_Image(website):
	websiteCopy = website
	regex = "<tr id=\"captcha\"><td>.*?<img .*?width=\".*?\" height=\".*?\" src=\"(.*?)\">"
	captchaImageText = re.search(regex, websiteCopy)
	if captchaImageText == None:
		print("Error: Captcha image cannot be found, please try again")
		return -1
	else:
		return captchaImageText.group(1)

def get_B64_From_Image(imageText):
	imageTextCopy = imageText
	regex = "data:image/gif;base64,(.*)"
	captchaImageB64 = re.search(regex, imageTextCopy)
	if captchaImageB64 == None:
		print("Error: Could not get base64 text of the image")
		return -1
	else:
		return captchaImageB64.group(1)

def make_Image_Of_B64(imageString):
	imageData = base64.b64decode(imageString)
	filename = 'captcha.png'
	with open(filename, 'wb') as image:
    		image.write(imageData)
	image.close()
	return filename

def error_Check(website):
	websiteCopy = website
	regex = "<h2>Error: (.*?)</h2>"
	errorSearch = re.search(regex, websiteCopy)
	if errorSearch == None:
		return 0
	else:
		error = errorSearch.group(1)
		if error == "Invalid nickname (20 characters maximum and has to match the regular expression \"^[A-Za-z0-9]*$\")":
			print("Site Error: Invalid nickname (20 characters maximum and has to match the regular expression \"^[A-Za-z0-9]*$\")")
			return error
		elif error == "Wrong Captcha":
			print("Site Error: Captcha was wrong")
			return error
		elif error == "Invalid password (At least 5 characters and has to match the regular expression \".*\")":
			print("Site Error: Invalid password (At least 5 characters and has to match the regular expression \".*\"")
			return error
		elif error == "Captcha already used or timed out.":
			print("Site Error: Captcha already used or expired.")
			return error
		elif error == "This nickname is a registered member.<br>Wrong Password!":
			print("Site Error: The nickname is registered already, please login with correct password, if it is yours")
			return error
		elif error == "Sorry, currently members only!":
			print("Site Error: Chat is in members only mode, try again later")
			return error
		elif error == "Invalid/expired session":
			print("Site Error: session expired or invalid")
			return error
		else:
			return error

def get_Cookies(websiteHeader):
	header = str(websiteHeader)
	regex = "\'Set-Cookie\': \'(.*?)\',"
	cookieSearch = re.search(regex, header)
	if cookieSearch:
		cookie = cookieSearch.group(1)
		return cookie
	else:
		print("Error: Could not find any cookies.")
		return -1

def get_Session(cookie, websiteBody):
	body = websiteBody
	cookie += '; '
	regexOne = "chat_session=(.*?); "
	regexTwo = "<.*?frame name=\".*?\" src=\".*?session=(.*?)&lang=.*?\">"
	sessionSearchOne = re.search(regexOne, cookie)
	if sessionSearchOne:
		sessionOne = sessionSearchOne.group(1)
	else:
		print("Error: could not get session id")
		return -1
	sessionSearchTwo = re.search(regexTwo, body)
	if sessionSearchTwo != None:
		sessionTwo = sessionSearchTwo.group(1)
	else:
		print("Error: could not get a matched session id in the body")
		return -1
	if sessionOne == sessionTwo:
		return sessionOne
	else:
		print("Error: there might be some error with session ID.")
		return -1

def get_urls(website):
	websiteCopy = website
	viewUrl = postUrl = controlsUrl = None
	regexUrlView = "<.*?frame name=\"view\" src=\"(.*?session=(.*?)&lang=.*?)\">"
	viewUrlSearch = re.search(regexUrlView, websiteCopy)
	if viewUrlSearch:
		viewUrl = viewUrlSearch.group(1)
	else:
		print("Could not get url to redirect the view part of the site")

	regexUrlPost = "<.*?frame name=\"post\" src=\"(.*?session=(.*?)&lang=.*?)\">"
	postUrlSearch = re.search(regexUrlPost, websiteCopy)
	if postUrlSearch:
		postUrl = postUrlSearch.group(1)
	else:
		print("Could not get url to redirect the post part of the site")

	regexUrlControls = "<.*?frame name=\"controls\" src=\"(.*?session=(.*?)&lang=.*?)\">"
	controlsUrlSearch = re.search(regexUrlControls, websiteCopy)
	if controlsUrlSearch:
		controlsUrl = controlsUrlSearch.group(1)
	else:
		print("Could not get url to redirect the control part of the site")
	if viewUrl or postUrl or controlsUrl:
		return viewUrl, postUrl, controlsUrl
	else:
		print("Error: There are issues getting any necessary urls")
		return -1, -1, -1

def change_To_Message(website):
	websiteCopy = website
	regexWholeMessage = "<div id=\"messages\">(.*)</div><a id=\"bottom\">"
	regexMakeMultiline = "(?<=<\/div>)<"
	messageSection = re.search(regexWholeMessage, website).group(1)
	makeMultiline = re.sub(regexMakeMultiline, '\n<', messageSection)
	messages = makeMultiline
	for i in range(5):
		if i == 0:
			regex = "<.*?>"
			subValue = ''
		elif i == 1:
			regex = "&lt;" #make this <
			subValue = '<'
		elif i == 2:
			regex = "&gt;" #make this >
			subValue = '>'
		elif i == 3:
			regex = "&nbsp;" #make this a space
			subValue = ' '
		elif i == 4:
			regex = "&quot;"
			subValue = '\"'
		messages = re.sub(regex, subValue, messages)
	return messages

def last_Messages(messages, ignorefile, sendFile):
	allMessage = messages
	lastMessage = ''
	for i in range(5):
		if i == 0:
			messageRegex = ".*?\n.*?\n.*?\n.*?\n(.*?\n)"
		if i == 1:
			messageRegex = ".*?\n.*?\n.*?\n(.*?\n)"
		if i == 2:
			messageRegex = ".*?\n.*?\n(.*?\n)"
		if i == 3:
			messageRegex = ".*?\n(.*?\n)"
		if i == 4:
			messageRegex = "(.*?\n)"
		messageSearch = re.search(messageRegex, allMessage)
		if messageSearch:
			match = 0
			messageFound = messageSearch.group(1)
			ignore = open(ignorefile)
			for line in ignore:
        			if line == messageFound:
       	     				match = 1
			send = open(sendFile)
			for line in send:
				if line == messageFound:
					match = 1
			if match != 1:
				lastMessage = lastMessage + messageFound
	return lastMessage

def convert_To_Messages(lastMessages):
	messages = lastMessages
	for i in range(5):
		if i == 0:
			regex = "^.*?-.*?(?=-)" #replace with nothing
			replace = ""
		if i == 1:
			regex = "^- (?=.*? -)" #replace with [
			replace = "["
		if i == 2:
			regex = "(?<=^\[)(.*?) -" #replace with \g<1>]:
			replace = "\g<1>]:"
		if i == 3:
			regex = "^- (?=.*?)" #replace with *
			replace = "*"
		if i == 4:
			regex = "(?<=^\*)(.*)" #replace with \g<1>*
			replace = "\g<1>*"
		messages = re.sub(regex, replace, messages, flags=re.M)
	return messages

def message_Sent_One(convertedMessages):
	messages = convertedMessages
	for line in messages.splitlines():
    			print(line)
