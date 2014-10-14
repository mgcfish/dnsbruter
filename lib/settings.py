#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 Jan Rude
"""

# Maximum number of threads (avoiding connection issues and/or DoS)
MAX_NUMBER_OF_THREADS = 150

# HTTP User-Agent header value. Useful to fake the HTTP User-Agent header value at each HTTP request
# Default: Mozilla/5.0
user_agent = {'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}

# Default number of concurrent threads
# Recommend: 80 (or network will be noticeable slower)
THREADS = 150

# Default timeout
# Default: 2.5
TIMEOUT = 2.5

# Input and output queues
subdomain_queue = ""
vhost_queue = ""
out_queue = ""

# List with subdomains
SUBDOMAIN_LIST = []

# List with vhost_subdomains
VHOST_LIST = []

# Wordlist
WORDLIST = "subdomains_big.txt"

# Wildcard domain IP
WILDCARD_IP = ""

# default response of wildcard domain
DEFAULT_RESPONSE = ""

# Current domain
DOMAIN = ""
