#!/usr/bin/env python

"""
Copyright (c) 2014 Jan Rude
"""

import time
from Queue import Queue
from os.path import isfile
from threading import Thread, Lock
from colorama import Fore
from lib import settings
import dns.resolver
import dns.zone

# This method lists the name servers for a domain and tries to perform a zone transfer
# If the zone transfer is successful, all subdomains get listed
# If a spf record is found, it will be shown
def try_zonetransfer():
	print('\n[+] DNS name server for "' + settings.DOMAIN + '" are:')
	nameserver = dns.resolver.query(settings.DOMAIN, 'NS')
	for ns in nameserver:
		print str(ns)
	
	# Check if SPF record exists
	print('\n[*] Trying zone transfer for each nameserver...')
	try:
		spf_query = dns.resolver.query(settings.DOMAIN, 'TXT')
		print(Fore.GREEN + '[+] SPF Record found!' + Fore.RESET)
		for rdata in spf_query:
			print ('Entry:SPFRecord;' + str(rdata))
	except:
		print (Fore.RED + '[x] No SPF Record found' + Fore.RESET)
	
	#try zone transfer
	for ns in nameserver:
		try:
			zone = dns.zone.from_xfr(dns.query.xfr(str(ns), settings.DOMAIN, lifetime = 3.0))
			time.sleep(1.3)
			print(Fore.GREEN + '[+] Success!' + Fore.RESET)
			names = zone.nodes.keys()
			for name in names:
				node_text = zone.nodes[name].to_text(name)
				#check IN A
				checkInAOutput = checkInA(node_text)
				if checkInAOutput is not None:
					print ('Entry:' + str(name) + '.' + settings.DOMAIN + ';' + checkInAOutput)
				else:
				#check IN CNAME
					checkInCNAMEOutput = checkInCNAME(node_text, zone.nodes)
					if checkInCNAMEOutput is not None:
						print ('Entry:' + str(name) + '.' + settings.DOMAIN + ';' + checkInCNAMEOutput)
			#if one zone transfer for a nameserver was successful, abort
			return True
		except:
			print(Fore.RED + '[x] Transfer failed for ' + str(ns))
	print('[x] Probably blocked from ' + settings.DOMAIN + Fore.RESET)
	return False

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
