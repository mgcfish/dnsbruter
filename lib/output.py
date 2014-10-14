#!/usr/bin/env python

"""
Copyright (c) 2014 Jan Rude
"""

from Queue import Queue
from threading import Thread,Lock
from lib import settings

# Output thread
def output_thread():
	while settings.out_queue is not settings.out_queue.empty():
		try:
			full_domain = settings.out_queue.get()
			print(full_domain)
			settings.out_queue.task_done()
		except Exception, e:
			print "Oops! Got:", e
