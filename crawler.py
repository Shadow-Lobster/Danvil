import requests
import time

def get_Request(hostname, session, cookie):
	website = hostname
	header = {	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Language' : 'en-US,en; q=0.9',
			'Cache-Control' : 'max-age=0',
			'Connection' : 'keep-alive',
			'Cookie' : cookie,
			'DNT' : '1',
			'Upgrade-Insecure-Requests' : '1',
			'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' }
	getRequest = session.get(website, headers = header)
	if getRequest.status_code == 200:
		return getRequest
	else:
		print("Error connecting to", website, ".\nStatus code: ", getRequest.status_code,'\n')
		i = 1
		while i <= 10:
			print("Retrying in 5 seconds...")
			time.sleep(5)
			print("Retry ", i," of 10")
			firstRequest = session.get(website, headers = header)
			if getRequest.status_code == 200:
				print("Connected to ", website)
				return getRequest
			else:
				print("Attempt", i, "failed. Status code:", getRequest.status_code, '\n')
			i += 1
		print("Error: aborting...")
		time.sleep(3)
		return -1
def post_Request(hostname, session, cookie, target, message):
	print("Please input the captcha code as displayed in the image \""+filename+"\"." )
	captcha = input("Enter the captcha code: ")
	postHeader = {	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Language' : 'en-US,en; q=0.9',
			'Cache-Control' : 'max-age=0',
			'Connection' : 'keep-alive',
			'Cookie' : cookie,
			'DNT' : '1',
			'Origin' : 'null',
			'Upgrade-Insecure-Requests' : '1',
			'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' }
	postData = { 'lang' : (None, 'en'),
		     'nc' : (None, nc),
		     'action' : (None, 'login'),
		     'nick' : (None, nick),
		     'pass' : (None, password),
		     'challenge' : (None, challenge),
		     'captcha' : (None, captcha),
		     'color' : (None, color) }
	session = requests.Session()
	postRequest = session.post(website, headers = postHeader, files = postData)
	if postRequest.status_code == 200:
		print("Connected to", website, "with nick", nick)
		return postRequest, session
	else:
		print("Error connecting to", website, ".\nStatus code: ", postRequest.status_code,'\n')
		i = 1
		while i <= 10:
			print("Retrying in 5 seconds...")
			time.sleep(5)
			print("Retry ", i," of 10")
			postRequest = session.post(website, headers = postHeader, files = postData, allow_redirects = False)
			if postRequest.status_code == 200:
				print("Connected to ", website)
				return postRequest, session
			else:
				print("Attempt ", i, " failed. Status code: ", postRequest.status_code, '\n')
			i += 1
		print("Error: aborting...")
		time.sleep(5)
		return -1

def get_Request_Login(hostname):
	website = hostname
	print(website)
	header = {	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Language' : 'en-US,en; q=0.9',
			'Cache-Control' : 'max-age=0',
			'Connection' : 'keep-alive',
			'DNT' : '1',
			'Upgrade-Insecure-Requests' : '1',
			'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' }
	firstRequest = requests.get(website, headers = header)
	if firstRequest.status_code == 200:
		print("Connected to ", website)
		return firstRequest
	else:
		print("Error connecting to", website, ".\nStatus code: ", firstRequest.status_code,'\n')
		i = 1
		while i <= 10:
			print("Retrying in 5 seconds...")
			time.sleep(5)
			print("Retry ", i," of 10")
			firstRequest = requests.get(website, headers = header)
			if firstRequest.status_code == 200:
				print("Connected to ", website)
				return firstRequest
			else:
				print("Attempt", i, "failed. Status code:", firstRequest.status_code, '\n')
			i += 1
		print("Error: aborting...")
		time.sleep(3)
		return -1

def post_Request_Login(hostname, cookie, nc, nick, password, challenge, filename, color):
	website = hostname
	print("Please input the captcha code as displayed in the image \""+filename+"\"." )
	captcha = input("Enter the captcha code: ")
	postHeader = {	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Language' : 'en-US,en; q=0.9',
			'Cache-Control' : 'max-age=0',
			'Connection' : 'keep-alive',
			'Cookie' : cookie,
			'DNT' : '1',
			'Origin' : 'null',
			'Upgrade-Insecure-Requests' : '1',
			'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' }
#	postData = border + "\r\nContent-Disposition: form-data; name=\"lang\"\r\n\r\nen\r\n" + border + "\r\nContent-Disposition: form-data; name=\"nc\"\r\n\r\n" + nc + "\r\n" + border + "\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\nlogin\r\n" + border + "\r\nContent-Disposition: form-data; name=\"nick\"\r\n\r\n" + nick + "\r\n" + border + "\r\nContent-Disposition: form-data; name=\"pass\"\r\n\r\n" + password + "\r\n" + border + "\r\nContent-Disposition: form-data; name=\"challenge\"\r\n\r\n" + challenge + "\r\n" + border + "\r\nContent-Disposition: form-data; name=\"captcha\"\r\n\r\n" + captcha + "\r\n" + border + "\r\nContent-Disposition: form-data; name=\"color\"\r\n\r\n" + color + "\r\n" + border + "--\r\n"
	postData = { 'lang' : (None, 'en'),
		     'nc' : (None, nc),
		     'action' : (None, 'login'),
		     'nick' : (None, nick),
		     'pass' : (None, password),
		     'challenge' : (None, challenge),
		     'captcha' : (None, captcha),
		     'colour' : (None, color) }
	session = requests.Session()
	postRequest = session.post(website, headers = postHeader, files = postData)
	if postRequest.status_code == 200:
		print("Connected to", website, "with nick", nick)
		return postRequest, session
	else:
		print("Error connecting to", website, ".\nStatus code: ", postRequest.status_code,'\n')
		i = 1
		while i <= 10:
			print("Retrying in 5 seconds...")
			time.sleep(5)
			print("Retry ", i," of 10")
			postRequest = session.post(website, headers = postHeader, files = postData, allow_redirects = False)
			if postRequest.status_code == 200:
				print("Connected to ", website)
				return postRequest, session
			else:
				print("Attempt ", i, " failed. Status code: ", postRequest.status_code, '\n')
			i += 1
		print("Error: aborting...")
		time.sleep(5)
		return -1
