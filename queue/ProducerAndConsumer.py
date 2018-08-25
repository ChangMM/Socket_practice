# 生产者消费者模式，慢速生产快速消费
from threading import Thread
import time
from queue import Queue
from collections import deque
from colorama import Fore, Style

# 创建队列，设置队列最大数限制为3个
queue = Queue(3)
tasks = deque([1, 2, 3, 4, 5, 6, 7, 8])


#生产者线程
class ProducerThread(Thread):
    def run(self):
        # 原材料准备，等待被生产
        global queue
        global tasks
        while True:
            try:
                # 从原材料左边开始生产
                time.sleep(1)  # 休眠随机时间
                item = tasks.popleft()
                queue.put(item)
                print(Fore.YELLOW, self.getName(), "生产者正在生产", item, "队列元素数:", queue.qsize(), Style.RESET_ALL)
            # 如果原材料被生产完，生产线程跳出循环
            except IndexError:
                print(Fore.RED, self.getName(), "原材料已被生产完毕", Style.RESET_ALL)
                break


#消费者线程
class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            # 通过get(),这里将队列减去了1
            item = queue.get()
            queue.task_done()
            if item is None:
                # print(item)
                break
            print(Fore.CYAN, self.getName(), "消费者正在消费", item, "现在队列内元素数目:", queue.qsize(), Style.RESET_ALL)


# 入口方法，主线程
def main():
    for i in range(2):
        # 把两个生产线程列为用户线程，确保生产者生产完所有项目
        producer = ProducerThread()
        producer.setDaemon(False)
        # 启动线程
        producer.start()

    for i in range(4):
        consumer = ConsumerThread()
        # 把四个消费者线程列为守护线程，否则主线程结束之后不会销毁该线程，程序不会停止，影响实验结果
        consumer.setDaemon(True)
        # 启动线程
        consumer.start()
    global queue
    # 这里休眠一秒钟，等到队列有值，否则队列创建时是空的，主线程直接就结束了，实验失败，造成误导
    time.sleep(1)
    # 接收信号，主线程在这里等待队列被处理完毕后再做下一步
    queue.join()
    # 给个标示，表示主线程已经结束
    print("主线程结束")


if __name__ == '__main__':
    main()
