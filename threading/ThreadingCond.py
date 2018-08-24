import threading
import time


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True

        t.start()

    def run(self):  # Run the timer and notify waiting threads after each interval
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1  # 0 和 1来回切换
                print("main", self._flag)
                self._cv.notify()

    def wait_for_tick(self, name):  # Wait for the next tick of the timer
        with self._cv:
            last_flag = self._flag
            print(name, 'last_flag:', last_flag)
            while last_flag == self._flag:
                self._cv.wait()
                print(name, 'self_flag:', self._flag)


# Example use of the timer
ptimer = PeriodicTimer(1)
ptimer.start()


# Two threads that synchronize on the timer
def countdown(ticks):
    while ticks > 0:
        ptimer.wait_for_tick("Down")
        print('count-down', ticks)
        ticks -= 1


def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick("up")
        print('count-up', n)
        n += 1


threading.Thread(target=countdown, args=(10,)).start()
threading.Thread(target=countup, args=(5,)).start()
