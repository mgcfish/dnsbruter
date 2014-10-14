#!/usr/bin/env python

"""
Copyright (c) 2014 Jan Rude
"""

import time
import socket
import re
from Queue import Queue
from threading import Thread, Lock
from colorama import Fore
from lib import settings
from lib import loadWordlist
from lib import output

def init_search():
	settings.subdomain_queue = Queue()
	settings.out_queue = Queue()
	settings.vhost_queue = Queue()

	if not settings.SUBDOMAIN_LIST:
		loadWordlist.load()

	for subdomain in settings.SUBDOMAIN_LIST:
		settings.subdomain_queue.put(subdomain)

	try:
		print('\n[*] Bruteforcing ' + str(settings.subdomain_queue.qsize()) + ' subdomains...')
		while True:
			if settings.subdomain_queue.empty() == False:
				# preventing network overload
				time.sleep(0.8)
				for i in xrange(0, settings.THREADS):
					if settings.WILDCARD_IP:						
						t = Thread(target=dnsbruter_wildCard, args=())
					else:
						t = Thread(target=dnsbruter, args=())
					t.daemon = True
					t.start()
			else:
				break
	except KeyboardInterrupt:
		print Fore.RED + "\nReceived keyboard interrupt.\nQuitting..." + Fore.RESET
		exit(-1)
	settings.subdomain_queue.join()

	if settings.WILDCARD_IP:
		try:
			for subdomain in settings.VHOST_LIST:
				settings.vhost_queue.put(subdomain)
			while True:
				if settings.vhost_queue.empty() == False:
					# preventing network overload
					time.sleep(0.8)
					for i in xrange(0, settings.THREADS):
						t = Thread(target=vhostbruter_wildCard, args=())
						t.daemon = True
						t.start()
				else:
					break
		except KeyboardInterrupt:
			print Fore.RED + "\nReceived keyboard interrupt.\nQuitting..." + Fore.RESET
			exit(1)
		settings.vhost_queue.join()

# output gets displayed directly, therefore this is not used atm
	# queue_size = settings.out_queue.qsize()
	# if queue_size == 0:
	# 	print Fore.RED + '[x] Nothing found!' + Fore.RESET
	# else:
	# 	t = Thread(target=output.output_thread, args=())
	# 	t.daemon = True
	# 	t.start()
	# 	settings.out_queue.join()

def dnsbruter():
	subdomain = settings.subdomain_queue.get()
	try:
		ip = socket.gethostbyname(subdomain + "." + settings.DOMAIN)
		print(Fore.GREEN + "Entry:" + (subdomain + "." + settings.DOMAIN + ";" + ip) + Fore.RESET)
	except:
		pass
	settings.subdomain_queue.task_done()

def dnsbruter_wildCard():
	subdomain = settings.subdomain_queue.get()
	try:
		ip = socket.gethostbyname(subdomain + "." + settings.DOMAIN)
		if not (ip == settings.WILDCARD_IP):
			print(Fore.GREEN + "Entry:" + (subdomain + "." + settings.DOMAIN + ";" + ip) + Fore.RESET)
	except:
		settings.VHOST_LIST.append(subdomain)
	settings.subdomain_queue.task_done()

def vhostbruter_wildCard():
	subdomain = settings.vhost_queue.get()
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(settings.TIMEOUT)
		s.connect((settings.WILDCARD_IP, 80))
		s.settimeout(None)
		request = [
			"GET / HTTP/1.1",
			"Host: %s" % (subdomain + "." + settings.DOMAIN),
			"User-Agent: %s" % settings.user_agent['User-Agent'],
			"Accept: text/*",
			"Accept-Charset: ISO-8859-1,utf-8",
			"Connection: close",
		]
		request = "\r\n".join(request)
		request += "\r\n\r\n"
		s.send( request )

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
		if not (data == settings.DEFAULT_RESPONSE):
			#settings.out_queue.put
			print(Fore.GREEN + "Entry:" + (subdomain + "." + settings.DOMAIN + ";" + ip) + Fore.RESET)
		s.close()
	except Exception, e:
		print e
	settings.vhost_queue.task_done()
