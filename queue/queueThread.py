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

# q.task_done()，每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，以提示q.join()是否停止阻塞，让线程向前执行或者退出；
# q.join()，阻塞，直到queue中的数据均被删除或者处理。为队列中的每一项都调用一次。


class ThreadUrl(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		while True:
			# grabs host from queue
			host = in_queue.get()
			print(self.getName(), "start")
			
			# grabs urls of hosts and then grabs chunk of web page
			url = urllib.request.urlopen(host)
			chunk = url.read()
			
			# place chunk into out queue
			out_queue.put(chunk)
			print(self.getName(), "end")
			# signals to queue job is done
			in_queue.task_done()


class ThreadData(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		while True:
			# grabs host from queue
			chunk = out_queue.get()
			print(self.getName(), "start")
			
			# parse the chunk
			soup = BeautifulSoup(chunk, features="html.parser")
			print(soup.findAll('title'))
			print(self.getName(), "end")
			# signals to queue job is done
			out_queue.task_done()


def main():
	# spawn a pool of threads, and pass them queue instance
	for i in range(3):
		t = ThreadUrl()
		t.setDaemon(True)
		t.start()
	
	# populate queue with data
	for host in hosts:
		in_queue.put(host)
		print(host)
	
	for i in range(3):
		dt = ThreadData()
		dt.setDaemon(True)
		dt.start()
	
	# wait on the queue until everything has been processed
	# 这两个join()函数的运行顺序不能调换
	# out_queue.join()
	in_queue.join()
	print("out_queue", out_queue.empty())
	print("in queue end")
	out_queue.join()
	print("out queue end")


start = time.time()
main()
print("Elapsed Time: ", time.time() - start)
