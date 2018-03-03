# coding=utf-8
import requests
from multiprocessing.dummy import Pool as ThreadPool
import time


def getsource(url):
    html = requests.get(url)


if __name__ == '__main__':
    urls = []
    for i in range(50, 500, 50):
        newpage = 'http://tieba.baidu.com/f?kw=python&ie=utf-8&pn=' + str(i)
        urls.append(newpage)

    # 单线程计时
    time1 = time.time()
    for i in urls:
        print(i)
        getsource(i)
    time2 = time.time()

    print('单线程耗时 : ' + str(time2 - time1) + ' s')

    # 多线程计时
    pool = ThreadPool(4)
    time3 = time.time()
    results = pool.map(getsource, urls)
    # pool.close()
    # pool.join()
    time4 = time.time()
    print('多线程耗时 : ' + str(time4 - time3) + ' s')
