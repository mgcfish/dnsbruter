#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# DNS Bruter - Automatic Subdomain Bruteforcer
# Copyright (c) 2015 Jan Rude
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program.
# If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)
#-------------------------------------------------------------------------------

from colorama import Fore
from lib.request import Request
from lib.thread_pool import ThreadPool

class Bruteforcer:
	"""
		This class will initiate the subdomain bruteforcing
	"""
	def __init__(self):
		pass

	def run(self, domain, wordlist):
		thread_pool = ThreadPool()
		domain_name = domain.get_name()
		is_wildcard = domain.get_is_wildcard()
		request = Request()
		results = []
		print('\n[*] Starting subdomain bruteforcing:')
		if not (is_wildcard):
			for subdomain in wordlist:
				thread_pool.add_job((request.head_request, (subdomain, domain_name)))
			thread_pool.start(20)

		else:
			for subdomain in wordlist:
				thread_pool.add_job((request.get_request, (subdomain + '.' + domain_name)))
			thread_pool.start(20, is_wildcard)

		for subdomain in thread_pool.get_result():
			print(Fore.GREEN + ' |  ' + str(subdomain[1][0]) + Fore.RESET)
