#!/usr/bin/env python
# -*- coding: utf-8 -*-

############ Version information ##############
__version__ = "0.3"
__program__ = "DNSBruter v" + __version__
__description__ = 'DNS Subdomain Bruteforcer'
__author__ = "it.sec (JaRu)"
__licence__ = "BSD Licence"
__status__ = "Development"
###############################################

import time
import socket
import datetime
import argparse
import warnings
from colorama import init, Fore, Style
warnings.filterwarnings(action="ignore", message=".*was already imported", category=UserWarning)
warnings.filterwarnings(action="ignore", category=DeprecationWarning)
from lib import settings
from lib import loadWordlist
from lib import zonetransfer
from lib import wildcard
from lib import bruteforcer
init()

# Main
def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--domain', dest='domain', type=str, nargs='+', help='Target domains to test.')
	parser.add_argument('-w', '--wordlist', dest='wordlist', default="wordlist_axfr_alexa_top_1mil_2014-02.txt", help='Subdomain wordlist (default: subdomains_big.txt)')
	parser.add_argument('-t', '--threads', dest='threads', default=settings.THREADS, type=int, help='Threads for socket connections (default: 7)')
	parser.add_argument('-to', '--timeout', dest='timeout', default=settings.TIMEOUT, type=int, help='Timeout for socket connections (default: 10)')
	parser.add_argument('--user_agent', dest='user_agent', metavar='USER-AGENT (default: Mozilla/5.0)')
	args = parser.parse_args()

	try:
		if args.threads > settings.MAX_NUMBER_OF_THREADS:
			print Fore.RED + "Warning! Threads are set to", args.threads,"(max value is 10)\nThis can cause connection issues and/or DoS\nAborting...." + Fore.RESET
			sys.exit(-2)

		settings.THREADS = args.threads

		socket.setdefaulttimeout(args.timeout)

		if args.wordlist:
			settings.WORDLIST = args.wordlist

		if args.user_agent:
			settings.user_agent.update({'User-Agent':args.user_agent})

		for domain in args.domain:
			settings.WILDCARD_IP = ""
			settings.DOMAIN = domain
			do_zonetrans = zonetransfer.try_zonetransfer()
			if do_zonetrans == False:
				is_wildcard = wildcard.check_domain()
				if is_wildcard == True:
					wildcard.get_defaultResponse()
				bruteforcer.init_search()

	except KeyboardInterrupt:
		print Fore.RED + "\nReceived keyboard interrupt.\nQuitting..." + Fore.RESET
		exit(1)
	except Exception, e:
		import traceback
		print ('generic exception: ', traceback.format_exc())

	finally:
		print '\n'
		now = datetime.datetime.now()
		print __program__ + ' finished at ' + now.strftime("%Y-%m-%d %H:%M:%S") + '\n'
		Style.RESET_ALL
		return True

if __name__ == "__main__":
	import sys
	print(Style.BRIGHT + '\n' + 50*'*')
	print('\t' + __program__ )
	print('\t' + __description__)
	print('\t' + '(c)2014 by ' + __author__)
	print('\t' + 'Status:\t' + __status__)
	print('\t' + 'For legal purposes only!')
	print(50*'*')
	sys.exit( not main( sys.argv ) )
