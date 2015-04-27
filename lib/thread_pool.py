#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Typo3 Enumerator - Automatic Typo3 Enumeration Tool
# Copyright (c) 2015 Jan Rude
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

import threading
from queue import Queue

class ThreadPoolSentinel:
	pass

class ThreadPool:
	"""
	Generic Thread Pool used for searching extensions and changelog/readme.
	Any found extension or changelog/readme goes to the result queue:
		work_queue:				Working queue
		result_queue:			Result queue
		active_threads:			Number of active threads
		thread_list:			List of worker threads
	"""
	def __init__(self):
		self.__work_queue = Queue()
		self.__result_queue = Queue()
		self.__active_threads = 0
		self.__thread_list = []

	def add_job(self, job):
		# Load job in queue
		self.__work_queue.put(job)

	def get_result(self):
		active_threads = self.__active_threads
		while (active_threads) or (not self.__result_queue.empty()):
			result = self.__result_queue.get()
			if isinstance(result, ThreadPoolSentinel): # One thread was done
				active_threads -= 1
				self.__result_queue.task_done()
				continue

			else: # Getting an actual result
				self.__result_queue.task_done()
				yield result

	def start(self, threads, wildcard_request=False):
		if self.__active_threads:
			raise Exception('Threads already started.')
		
		if not wildcard_request:
			# Create thread pool
			for _ in range(threads):
				worker = threading.Thread(
					target=_work_function,
					args=(self.__work_queue, self.__result_queue))
				worker.start()
				self.__thread_list.append(worker)
				self.__active_threads += 1
		else:
			# Create thread pool
			for _ in range(threads):
				worker = threading.Thread(
					target=_wildcard_work_function,
					args=(self.__work_queue, self.__result_queue, wildcard_request))
				worker.start()
				self.__thread_list.append(worker)
				self.__active_threads += 1

		# Put sentinels to let the threads know when there's no more jobs
		[self.__work_queue.put(ThreadPoolSentinel()) for worker in self.__thread_list]

	def join(self): # Clean exit
		self.__work_queue.join()
		[worker.join() for worker in self.__thread_list]
		self.__active_threads = 0
		self.__result_queue.join()

def _work_function(job_q, result_q):
	"""Work function expected to run within threads."""
	while True:
		job = job_q.get()

		if isinstance(job, ThreadPoolSentinel): # All the work is done, get out
			result_q.put(ThreadPoolSentinel())
			job_q.task_done()
			break

		function = job[0]
		args = job[1]
		try:
			result = function(*args)
			if not(result == None):
				result_q.put(result)
		except Exception as e:
			print('_work_function says:\n', e)
		finally:
			job_q.task_done()

def _wildcard_work_function(job_q, result_q, init_request):
	"""Work function expected to run within threads."""
	while True:
		job = job_q.get()

		if isinstance(job, ThreadPoolSentinel): # All the work is done, get out
			result_q.put(ThreadPoolSentinel())
			job_q.task_done()
			break

		function = job[0]
		args = str(job[1])
		try:
			result = function(args)
			if not(result == None) and not(result[0] == init_request):
				result_q.put(result[1])
		except Exception as e:
			print('_wildcard_work_function says:\n', e)
		finally:
			job_q.task_done()