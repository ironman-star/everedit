# coding = utf-8
import requests
import urllib2
import time
from bs4 import BeautifulSoup


def get_novel(url, header):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1', id='BookTitle')
    novel = soup.find('div', id='BookText')
    print response.status_code
    print url
    if response.status_code != 200:
        print 'repeat because of bad connect'
        time.sleep(2)
        get_novel(url, header)
    next_url = soup.find('a', id='book-next')
    url = str(next_url).replace('<a href="', header).split('" id=')[0]
    f = open('novel.txt', 'a')
    f.write(title.encode('gbk'))
    f.write(novel.encode('gbk'))
    return url


if __name__ == '__main__':
    url = 'http://m.uuxs.net/book/41/41914/14380677.html'
    header = 'http://m.uuxs.net/book/41/41914/'
    ch = 1
    while 1:
        name = url
        url = get_novel(url, header)
        print 'chapter', ch
        ch += 1
        if name == url:
            break
