from functools import wraps
from inspect import signature
import logging
import time


# 带参数的装饰器
def logged(level, name = None, message = None):
	"""
	    Add logging to a function. level is the logging
	    level, name is the logger name, and message is the
	    log message. If name and message aren't specified,
	    they default to the function's module and name.
	"""
	def decoration(func):
		log_name = name if name else func.__module__
		log_message = message if message else func.__name__
		log = logging.getLogger(log_name)
		
		@wraps(func)
		def wrapper(*args, **kargs):
			log.log(level, log_message)
			print(level, log_message)
			return func(*args, **kargs)
		return wrapper
	return decoration


# 不带参数的装饰器
def time_cal(func):
	@wraps(func)
	def wrapper(*args, **kargs):
		start = time.time()
		result = func(*args, **kargs)
		end = time.time()
		print("The result is: ", result, ", cost time: ", end - start)
		return result
	return wrapper


# 检查参数类型的装饰器
def type_assert(*type_args, **type_kargs):
	def decoration(func):
		if not __debug__:
			return func
		
		sig = signature(func)
		# 使用bind_partial()方法来对提供的类型到参数名做部分绑定
		bound_types = sig.bind_partial(*type_args, **type_kargs)
		
		@wraps(func)
		def wrapper(*args, **kargs):
			bound_values = sig.bind(*args, **kargs)
			for name, value in bound_values.arguments.items():
				if name in bound_types:
					if not isinstance(value, bound_types[name]):
						raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
			return func(*args, **kargs)
		return wrapper
	return decoration


@logged(logging.DEBUG)
def test_log():
	print("This is a function to test logged decoration")


@time_cal
def test_time_cal():
	temp = 0
	for i in range(1000000):
		temp += i
	return temp


if __name__ == "__main__":
	test_log()
	test_time_cal()
