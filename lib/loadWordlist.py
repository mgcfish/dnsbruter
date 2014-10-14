#!/usr/bin/env python

"""
Copyright (c) 2014 Jan Rude
"""

from os.path import isfile
from lib import settings

#loading wordlist in input_queue
def load():
	print('\n[*] Loading wordlist...')
	if not isfile(settings.WORDLIST):
		print(Fore.RED + "Subdomain wordlist not found: " + settings.WORDLIST)
		print(Fore.RESET)
		return False
	else:
		with open(settings.WORDLIST, 'r') as f:
			for line in f:
				settings.SUBDOMAIN_LIST.append(line.strip('\n'))
