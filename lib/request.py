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

import socket
import requests
import dns.resolver
import dns.zone
import multiprocessing
from colorama import Fore
requests.packages.urllib3.disable_warnings()
import multiprocessing

class Request:
	"""
	This class is used to make all requests
	"""
	def __init__(self):
		pass

	def request_nameserver(self, domain_name):
		nameserver = dns.resolver.query(domain_name, 'NS', raise_on_no_answer=False, source_port=53)
		return nameserver

	def check_SPFRecord(self, nameserver):
		data = []
		for ns in nameserver:
			try:
				spf_query = dns.resolver.query(str(ns), 'TXT', source_port=53)
				for rdata in spf_query:
					data.append(str(rdata))
			except:
				pass
		return data

	def try_zonetransfer(self, nameserver, domain_name):
		node_text = []
		for ns in nameserver:
			try:
				zone = dns.zone.from_xfr(dns.query.xfr(str(ns), domain_name, lifetime = 3.0))
				return zone.nodes
			except Exception as e:
				print(' | ', e)
		return False

	def head_request(self, subdomain, domain_name):
		combined = subdomain + '.' + domain_name
		try:
			ip = socket.gethostbyname(combined)
			return (combined.center(18) + ' (' + str(ip) + ')')
		except socket.gaierror:
			return None
		except Exception as e:
			print(combined + ' says:', e)
			return None

	def get_request(self, domain_name):
	 	try:
	 		r = requests.get('http://' + domain_name, timeout=2, headers={'User-Agent' : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"}, allow_redirects=True)
	 		try:
	 			ip = socket.gethostbyname(domain_name)
	 		except Exception as e:
	 			print('Could not determine ip address:', e)
	 			ip = 'error'
	 		return [r.text, (domain_name.center(18) + ' (' + str(ip) + ')')]
	 	except requests.exceptions.Timeout:
	 		print(Fore.RED + '[x] Connection timed out' + Fore.RESET)
	 	except requests.exceptions.ConnectionError:
	 		pass
	 	except requests.exceptions.RequestException as e:
	 		print(domain_name + ' says:', e)
	 	return None