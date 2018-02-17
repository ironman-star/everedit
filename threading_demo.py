import threading
import queue
import time


class mn_access(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.thread_stop = False

    def run(self):  # 这个函数中存放用户自己的功能代码
        i = 1
        while not self.thread_stop:
            print("thread%d %s: i am alive hehe %d" % (self.ident, self.name, i))
            time.sleep(self.interval)
            i = i + 1

    def stop(self):
        self.thread_stop = True


if __name__ == "__main__":
    mn = mn_access(1)
    mn.start()  # 线程开始
    time.sleep(5)
    mn.stop()
