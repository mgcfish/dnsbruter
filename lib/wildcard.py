#!/usr/bin/env python

"""
Copyright (c) 2014 Jan Rude
"""

import time
import re
import socket
import hashlib
from colorama import Fore
from lib import settings

#check wildcard domains
def check_domain():
	print('\n[*] Starting wildcard detection...')
	randomSubdomain = hashlib.sha224(str(time.time())).hexdigest()[:12]
	try:
		ip = socket.gethostbyname(randomSubdomain + '.' + settings.DOMAIN)
	except:
		print(Fore.GREEN + '[+] ' + settings.DOMAIN + ' is no wildcard domain :)' + Fore.RESET)
		return False
	print(Fore.RED + '[x] ' + settings.DOMAIN + ' is a wildcard domain! (' + ip + ')' + Fore.RESET)
	settings.WILDCARD_IP = ip
	return True

def get_defaultResponse():
	request = [
		"GET / HTTP/1.1",
		"Host: %s" % settings.DOMAIN,
		"User-Agent: %s" % settings.user_agent['User-Agent'],
		"Accept: text/*",
		"Accept-Charset: ISO-8859-1,utf-8",
		"Connection: close",
	]
	request = "\r\n".join(request)
	request += "\r\n\r\n"
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((settings.DOMAIN, 80))
		s.send(request)
	except:
		print "Port 80 failed, trying 443..."
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((settings.DOMAIN, 443))
			s.send(request)
		except Exception, e:
			print "Error in wildcard.get_defaultResponse"
			print e

	data = ""
	while 1:
		block = s.recv(1024)
		if not block:
			break
		data += block

	regex = re.compile("Date:(.*)\r\n", re.IGNORECASE)
	searchTitle = regex.search(data)
	date = searchTitle.groups()
	data = data.replace(date[0], "")
	settings.DEFAULT_RESPONSE = data
