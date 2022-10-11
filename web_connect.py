import requests
import crawler
import regex

#Deals with login and site connection request to gather all values.
def connect_To_Site(webhostname, websiteNick, websitePassword, websiteColor):
	#Making get request to site to get necessary values.
	firstRequest = crawler.get_Request_Login(webhostname)
	if firstRequest == -1:
		print("Critical Error: There is some issue connecting to", webhostname, ". Please try again later")
		return -1
	else:
		firstResponseHeader = firstRequest.headers
		firstResponseBody = firstRequest.text

	nc = regex.find_nc(firstResponseBody)
	challenge = regex.find_Challenge(firstResponseBody)
	captchaImageData = regex.get_Captcha_Image(firstResponseBody)
	captchaImageB64 = regex.get_B64_From_Image(captchaImageData)
	captchaImage = regex.make_Image_Of_B64(captchaImageB64)
	
	cookie = regex.get_Cookies(firstResponseHeader)

	#Making the post request with login values.
	postRequest, session = crawler.post_Request_Login(webhostname, cookie, nc, websiteNick, websitePassword, challenge, captchaImage, websiteColor)
	if postRequest == -1:
		print("Critical Error: There is some issue connecting to", webhostname, ". Please try again later")
		return -1
	else:
		return postRequest, session

#To get the message updates.
def view_Latest_Message(websiteHost, session, cookie, first, ignorefile):
	websitename = websiteHost
	getResponse = crawler.get_Request(websitename, session, cookie)
	if getResponse == -1:
		print("Critical Error: There is some issue connecting to", webhostname, ". Please try again later")
		return -1
	else:
		siteBody = getResponse.text
		errorCheck = regex.error_Check(siteBody)
		if errorCheck == 0:
			messages = regex.change_To_Message(siteBody)

			#if just connected then ignore the rest
			if first == 1:
				return messages
			sendFile = 'send.txt'
			lastMessages = regex.last_Messages(messages, ignorefile, sendFile)
			convertedMessages = ''
			if lastMessages != '':
				send = open(sendFile, 'a')
				send.write(lastMessages)
				send.close()
				convertedMessages = regex.convert_To_Messages(lastMessages)
				messageSentOne = regex.message_Sent_One(convertedMessages)
		else:
			return -1
		
def sent_Message(websiteHost, session, cookie, target, message):
	websitehostname = websiteHost
	postRequest, session = crawler.post_Request(websitename, cookie, nc, websiteNick, websitePassword, challenge, captchaImage, websiteColor)
	if postRequest == -1:
		print("Critical Error: There is some issue connecting to", webhostname, ". Please try again later")
		return -1
	else:
		return postRequest