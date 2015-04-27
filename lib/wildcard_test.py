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
import time
import hashlib
from colorama import Fore
from lib.request import Request

class Wildcard:
	"""
		This class checks if the domain is a wildcard domain.
	"""
	def __init__(self):
		print('\n[*] Starting wildcard detection:')

	def test(self, domain):
		request = Request()
		domain_name = domain.get_name()
		randomSubdomain = hashlib.sha224(str(time.time()).encode('utf-8')).hexdigest()[:12]
		response = request.get_request(randomSubdomain + '.' + domain_name)
		if response:
			domain.set_is_wildcard(response[0])
			print(Fore.RED + ' | ' + domain_name + ' is a wildcard domain' + Fore.RESET)
		else:
			print(Fore.GREEN + ' | ' + domain_name + ' is no wildcard domain' + Fore.RESET)