import threading
import time
import random

L = []


def read():
	while 1:
		count = random.randint(0, 1)
		if count:
			L.append('Hello, darling,I love you')
			L.append('You are so sweet~')
		if L:
			evt.set()
			print('new rcvd sent to \'parse thread\'')
		time.sleep(2)


def parse():
	while 1:
		if evt.isSet():
			evt.clear()
			print(repr(len(L)) + ' messages to parse:')
			while L:
				print(L.pop(0))
			print('all msg prased,sleep 2s')
			time.sleep(2)
		else:
			print('no message rcved')
			time.sleep(2)


if __name__ == '__main__':
	evt = threading.Event()
	R = threading.Thread(target = read)
	P = threading.Thread(target = parse)
	R.start()
	P.start()
	time.sleep(2)
	R.join()
	P.join()
	print('end')
