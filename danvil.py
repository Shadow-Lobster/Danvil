import requests
import sys
import configparser
import time
import web_connect
import crawler
import regex
from requests_toolbelt.utils import dump

#Getting values from config.ini
configRead = configparser.ConfigParser()
configRead.read('config.ini')
webhostname = configRead.get('website', 'site')
websiteNick = configRead.get('website', 'nick')
websitePassword = configRead.get('website', 'password')
websiteColor = configRead.get('website', 'color')
owner = configRead.get('website', 'owner')

connected = 1
while connected == 1:
	postRequest, session = web_connect.connect_To_Site(webhostname, websiteNick, websitePassword, websiteColor)

	#Connection succeeded or not.
	if postRequest == -1:
		print("Critical error occured. Exiting..")
		sys.exit()
	else:
		postResponseHeader = postRequest.headers
		postResponseBody = postRequest.text

	#Check to make sure there are no errors.
	if regex.error_Check(postResponseBody) == 0:
		cookie = regex.get_Cookies(postResponseHeader)
		sessionID = regex.get_Session(cookie, postResponseBody)
		viewUrl, postUrl, controlsUrl = regex.get_urls(postResponseBody)
		connected = 0
		print(viewUrl, postUrl, controlsUrl)

#To view the http raw requests
data = dump.dump_all(postRequest)
print(data.decode('utf-8'))

first = 1
quit = 0
viewSiteUrl = webhostname + viewUrl
while quit != 1:
		time.sleep(5)
		#To make an ignore list to ignore the messages already present before connection.
		if first == 1:
			ignorefile = 'ignore.txt'
			messages = web_connect.view_Latest_Message(viewSiteUrl, session, cookie, first, ignorefile)
			ignore = open(ignorefile, 'w')
			ignore.write(messages)
			ignore.close()
			first = 0
		messages = web_connect.view_Latest_Message(viewSiteUrl, session, cookie, first, ignorefile)
		if messages == -1:
			print("Some error occured, exiting")
			sys.exit()
