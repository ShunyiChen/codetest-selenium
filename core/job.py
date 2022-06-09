import threading
import time


class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        # 用于暂停线程的标识
        self.__flag = threading.Event()
        self.__flag.set()  # 设置为True
        # 用于停止线程的标识
        self.__running = threading.Event()
        self.__running.set()  # 将running设置为True

    def run(self):
        while self.__running.is_set():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如果已经暂停的话
        self.__running.clear()  # 设置为False
