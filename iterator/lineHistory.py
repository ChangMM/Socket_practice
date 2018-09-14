#  !/usr/bin/env  python
#  -*- coding:utf-8 -*-
# @Time   :  2018.
# @Author :  sakamoto
# @Email  :  meixingneyan@gmail.com
# @Note   : 
from collections import deque


class LineHistory:
    def __init__(self, lines, maxLen=3):
        self.lines = lines
        self.history = deque(maxlen = maxLen)
    
    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()


if __name__ == "__main__":
    with open("somefile.txt") as f:
        lines = LineHistory(f)
        for line in lines:
            if 'python' in line:
                print(line)
                # for lineno, hline in lines.history:
                    # print('{}:{}'.format(lineno, hline))
