import time
from functools import wraps


def time_cal(func):
	'''
	计算函数的运行时间
	'''
	@wraps(func)
	def wrapper(*args, **kargs):
		start = time.time()
		result = func(*args, **kargs)
		end = time.time()
		print(func.__name__, "函数运行时间", end-start)
		return result
	return wrapper

@time_cal
def count(n):
	temp = 0
	for i in range(n):
		temp += i
	return temp


# 装饰内部加上 @wraps 可以避免函数的元信息丢失
print(time_cal.__doc__)
print(count(1000000))

# 获取原始的非装饰的函数
origin_count = count.__wrapped__
print(origin_count(1000000))
