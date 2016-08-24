#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# DNS Bruter - Automatic Subdomain Bruteforcer
# Copyright (c) 2016 Jan Rude
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)
#-------------------------------------------------------------------------------

__version__ = "0.4.1.1"
__program__ = "DNS Bruter"
__description__ = 'Automatic Subdomain Bruteforcer'
__author__ = "https://github.com/whoot"

import sys
import os.path
import datetime
import argparse
from colorama import Fore, init, deinit, Style
from lib.domain import Domain
from lib.request import Request
from lib.zonetransfer import Zonetransfer
from lib.wildcard_test import Wildcard
from lib.bruteforcer import Bruteforcer
init()

class DNSBruter:
	def __init__(self):
		self.__domain_list = []
		self.__wordlist = []

	def run(self):
		parser = argparse.ArgumentParser(usage='dnsbruter.py [options]', add_help=False)
		group = parser.add_mutually_exclusive_group()
		group.add_argument('-f', '--file', dest='file')
		group.add_argument('-d', '--domain', dest='domain', type=str, nargs='+')
		parser.add_argument( "-w", "--wordlist", default='wordlists/popular_10000.txt')
		parser.add_argument( "-h", "--help", action="help")
		args = parser.parse_args()

		try:
			if args.domain:
				for dom in args.domain:
					self.__domain_list.append(Domain(dom))
			elif args.file:
				if not os.path.isfile(args.file):
					print(Fore.RED + "\n[x] File not found: " + args.file + "\n |  Aborting..." + Fore.RESET)
					sys.exit(-2)
				else:
					with open(args.file, 'r') as f:
						for line in f:
							self.__domain_list.append(Domain(line.strip('\n')))

			for domain in self.__domain_list:
				print('\n\n' + Fore.CYAN + Style.BRIGHT + '[ Checking ' + domain.get_name() + ' ]' + '\n' + "-"* 73  + Fore.RESET + Style.RESET_ALL)
				zonetransfer = Zonetransfer()
				zonetransfer.run(domain)
				if not domain.get_zonetransfer():
					wildcard = Wildcard()
					wildcard.test(domain)

				if not self.__wordlist:
					with open(args.wordlist, 'r') as wordlist:
						for line in wordlist:
							self.__wordlist.append(line.strip('\n'))
				
				bruteforcer = Bruteforcer()
				bruteforcer.run(domain, self.__wordlist)


		except KeyboardInterrupt:
			print("\nReceived keyboard interrupt.\nPress ctrl+c again to quit...")
			sys.exit(-1)
		finally:
			deinit()
			now = datetime.datetime.now()
			print('\n\n' + __program__ + ' finished at ' + now.strftime("%Y-%m-%d %H:%M:%S") + '\n')	


if __name__ == "__main__":
	print('\n' + 73*'=' + Style.BRIGHT)
	print(Fore.BLUE + ' ______  __   _ _______'.center(73))
	print('|     \ | \  | |______'.center(73))
	print('|_____/ |  \_| ______|'.center(73))
	print('						 '.center(73))
	print('______   ______ _     _ _______ _______  ______'.center(73))
	print('|_____] |_____/ |     |    |    |______ |_____/'.center(73))
	print('|_____] |    \_ |_____|    |    |______ |    \_'.center(73))
	print(Fore.RESET + Style.RESET_ALL)
	print(__description__.center(73))
	print(('Version ' + __version__).center(73))
	print((__author__).center(73))
	print(73*'=')
	main = DNSBruter()
	main.run()