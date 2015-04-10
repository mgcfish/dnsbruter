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

class Domain(object):
	"""
	This class stores following information about a domain:
		name: 					URL of the domain
		wordlist:				List of subdomains to check for
		nameserver:				List of domain nameserver
		zonetransfer:			Nameserver allows zonetransfer
		wildcard:				Domain accepts any subdomain
		subdomains:				List of found subdomains
	"""
	def __init__(self, name):
		self.__name = name
		self.__nameserver = []
		self.__zonetransfer = False
		self.__wildcard = False
		self.__subdomains = []

	def get_name(self):
		return self.__name

	def get_nameserver(self):
		return self.__nameserver

	def set_nameserver(self, ns):
		self.__nameserver.append(ns)
		
	def get_subdomains(self):
		return self.__subdomains

	def set_subdomains(self, subdomain):
		self.__subdomains.add(subdomain)

	def set_is_wildcard(self, response):
		self.__wildcard = response

	def get_is_wildcard(self):
		return self.__wildcard

	def set_zonetransfer(self):
		self.__zonetransfer = True

	def get_zonetransfer(self):
		return self.__zonetransfer