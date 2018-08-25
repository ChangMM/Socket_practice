# !/usr/bin/env python
from queue import Queue
import threading
import urllib.request
from bs4 import BeautifulSoup
import time

hosts = [
	"http://www.yahoo.com",
	"http://cn.bing.com",
	"https://xmt.cn/",
	"http://www.baidu.com",
	"http://www.apple.com"]

in_queue = Queue()
out_queue = Queue()


class ThreadUrl(threading.Thread):
	def __init__(self, in_q, out_q):
		threading.Thread.__init__(self)
		self.queue = in_q
		self.out_queue = out_q
	
	def run(self):
		while True:
			# grabs host from queue
			host = self.queue.get()
			
			# grabs urls of hosts and then grabs chunk of web page
			url = urllib.request.urlopen(host)
			chunk = url.read()
			
			# place chunk into out queue
			self.out_queue.put(chunk)
			
			# signals to queue job is done
			self.queue.task_done()


class DatamineThread(threading.Thread):
	def __init__(self, out_q):
		threading.Thread.__init__(self)
		self.out_queue = out_q
	
	def run(self):
		while True:
			# grabs host from queue
			chunk = self.out_queue.get()
			
			# parse the chunk
			soup = BeautifulSoup(chunk, features="html.parser")
			print(soup.findAll('title'))
			# signals to queue job is done
			self.out_queue.task_done()


def main():
	# spawn a pool of threads, and pass them queue instance
	for i in range(5):
		t = ThreadUrl(in_queue, out_queue)
		t.setDaemon(True)
		t.start()
	
	# populate queue with data
	for host in hosts:
		in_queue.put(host)
	
	for i in range(5):
		dt = DatamineThread(out_queue)
		dt.setDaemon(True)
		dt.start()
	
	# wait on the queue until everything has been processed
	# 这两个的顺序不能调换
	in_queue.join()
	out_queue.join()


start = time.time()
main()
print("Elapsed Time: ", time.time() - start)
