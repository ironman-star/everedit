# coding=utf-8
from bs4 import BeautifulSoup
import requests
import re

topic = 'http://www.itokoo.com/read.php?tid='


def get_url_and_password(url):
    try:
        response = requests.get(url)
    except:
        print('retry')
        print(url)
        get_url_and_password(url)
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.find('a', text='百度网盘'):
            download = str(soup.find('a', text='百度网盘')).split('href=\"')[1].split('\"')[0]
        elif soup.find('a', text='百度云网盘'):
            download = str(soup.find('a', text='百度云网盘')).split('href=\"')[1].split('\"')[0]
        else:
            print('describe is wrong', url)
            return
        ph = re.compile('密码:')
        password = str(soup.find(text=ph)).split(':')[1].strip(' ').strip('\n')
        f = open('download.txt', 'a')
        f.write(download + '   ' + password + '\n')
        print(url, download, 'write success!')
    except Exception as e:
        print(e)
        print('wrong', url)
        pass


if __name__ == '__main__':
    for item in range(13000, 17000):
        true_url = topic + str(item)
        get_url_and_password(true_url)
    print('its end')
