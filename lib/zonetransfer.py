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

import re
import dns.name
from colorama import Fore
from lib.request import Request

class Zonetransfer:
	"""
		This class will try a zone-transfer for a domain.
		If it is successful, subdomain bruteforcing will not be needed,
		because every subdomain will be known.
	"""
	def __init__(self):
		pass

	def run(self, domain):
		domain_name = domain.get_name()
		request = Request()
		nameserver = request.request_nameserver(domain_name)
		print('[+] DNS name server are:')
		for ns in nameserver:
			domain.set_nameserver(ns)
			print (' | ', str(ns))

		request = Request()
		print('\n[*] Trying zone transfer for each nameserver:')
		spf_record = request.check_SPFRecord(domain.get_nameserver())
		if spf_record:
			print(Fore.GREEN + ' |  SPF Record: ' + Fore.RESET)
			for data in transfer:
				print(' | ' + data)

		nodes = request.try_zonetransfer(domain.get_nameserver(), domain_name)
		if not nodes:
			print(Fore.RED + ' |  Transfer failed')
			print(' |  Probably blocked from ' + domain_name + Fore.RESET)
		else:
			domain.set_zonetransfer()
			for n in nodes.keys():
				node_text = nodes[n].to_text(n)
				#check IN A
				checkInAOutput = checkInA(node_text)
				if checkInAOutput is not None:
					print((Fore.GREEN + ' |  ' + str(n) + '.' + domain_name ).ljust(40) + ' -- ' + checkInAOutput + Fore.RESET)
				else:
				#check IN CNAME
					checkInCNAMEOutput = checkInCNAME(node_text, nodes)
					if checkInCNAMEOutput is not None:
						print((Fore.GREEN + ' |  ' + str(n) + '.' + domain_name).ljust(40) + ' -- ' + checkInCNAMEOutput + Fore.RESET)



# Check IN A records from zone transfer
def checkInA(node_text):
	try:
		InA = re.search("IN A (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", node_text)
		ip_address = InA.group(0).split("IN A ")[1]
		return ip_address
	except:
		return None


# Check IN CNAME records from zone transfer
def checkInCNAME(node_text, nodes):
	try:
		InCNAME = re.search("IN CNAME (.*)", node_text)
		alias = InCNAME.group(0).split("IN CNAME ")[1]
		#IP address found
		if re.match("(\d{1,3}\.)", alias):
			return alias
		# cname is a subdomain
		elif re.match(".*[a-x]\.", alias):
			return ("subdomain found (" + alias + ")")
		#cname is another cname
		else:
			try:
				alias_name = dns.name.Name([alias])
				alias_IP = nodes[alias_name].to_text(alias_name)
				checkCname = checkInA(alias_IP)
				if checkCname is None:
					return checkInCNAME(alias_IP, nodes)
				else:
					return checkCname
			except:
				return (Fore.RED + "unknown host (" + alias + ")" + Fore.RESET)
	# node has no IN CNAME
	except:
		return None