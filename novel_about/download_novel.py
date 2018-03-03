# coding=utf8
from bs4 import BeautifulSoup
import requests
import sys


def get_soup(url):
    response = requests.request('get', url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_book_name(url):
    soup = get_soup(url)
    book_name = soup.find('span', class_='c3').text
    return book_name


def get_next_chapter(l_url, r_url):
    try:
        url = l_url + '/' + r_url
        soup = get_soup(url)
        next_r_chapter = soup.find('a', id='book-next').get('href')
    except:
        get_next_chapter(l_url, r_url)
    return next_r_chapter


def get_novel(l_url, r_url, book_name):
    url = l_url + '/' + r_url
    try:
        response = requests.request('get', url=url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1', id='BookTitle').text.strip(' ')
        word = soup.find('div', id='BookText').text.replace('\xa0', ' ').replace('   ', '\n')
        with open(book_name + '.txt', 'a') as f:
            f.write(title + '\n' + word + '\n\n')
            print(title, 'OK')
    except Exception as e:
        print(e)
        if r_url.find('index') != -1:
            print("It's the end.")
            return
        get_novel(l_url, r_url, book_name)
    r_url = get_next_chapter(l_url, r_url)
    if r_url.find('index') != -1:
        print("It's the end.")
        return
    get_novel(l_url, r_url, book_name)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = get_book_name(sys.argv[1])
        left_url = sys.argv[1].rsplit('/', 1)[0]
        right_url = sys.argv[1].rsplit('/', 1)[1]
        get_novel(left_url, right_url, name)
    print('End of download')
