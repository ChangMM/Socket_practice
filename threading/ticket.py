#! /usr/bin/python
# -* coding: utf-8 -*
# 火车买票问题
import threading
from threading import Thread
import time
import os


def booth(tid):
	global total_tickets
	global lock
	while True:
		lock.acquire()
		if total_tickets > 0:
			total_tickets = total_tickets - 1
			print("Thread ID", tid, total_tickets, "tickets left.")
			time.sleep(1)
		else:
			print("Thread ID not tickets.")
			os._exit(0)
		lock.release()
		# time.sleep(1)


total_tickets = 100
lock = threading.Lock()
for i in range(10):
	newThread = Thread(target = booth, args = (i,))
	newThread.start()
