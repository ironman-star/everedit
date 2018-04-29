# coding=utf-8
import pymysql
import requests
from bs4 import BeautifulSoup
import re
import os
from multiprocessing.dummy import Pool as ThreadPool
import time


def put_data_into_database(target, title, sql_id, path):
    response = requests.request('get', url=target)
    if response.status_code != 200:
        print('Got error in getting page of', target)
        return True
    soup = BeautifulSoup(response.content, 'html.parser')
    word = soup.find('div', id='BookText').text.replace('\xa0', ' ').replace('   ', '\n')
    path = '/home'+path
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(path + sql_id + '.txt', 'w')as f:
        f.write('\n'+title+'\n')
        f.write(word)
    print(title, 'is OK!')


def download_single_novel(content_url, path, ):
    start_time = time.time()
    pool = ThreadPool(100)
    response1 = requests.get(content_url).content
    soup1 = BeautifulSoup(response1, 'html.parser')
    main_chapter = BeautifulSoup(str(soup1.find('div', id='main')), 'html.parser')
    all_chapter = main_chapter.find_all('a')
    count = 0
    for chapter in all_chapter:
        chapter_number = re.search('\d+', str(chapter)).group(0)
        title = BeautifulSoup(str(chapter), 'html.parser').text
        url = content_url + chapter_number + '.html'
        pool.apply_async(put_data_into_database, [url, title, chapter_number, path])
        # if put_data_into_database(url, title, chapter_number, database, path):
        #     continue
    pool.close()
    pool.join()
    end_time = time.time()
    print('Finish,', 'download', count, 'chapters, takes', end_time - start_time, 'seconds')


if __name__ == '__main__':
    url = 'https://m.uuxs.la/book/0/902/'
    local = './book/902/'
    # download_single_novel(url, local)
    dir_path = '/home/book/902/'
    file_names = os.listdir(dir_path)
    chapter_list = []
    for item in file_names:
	    item=item.replace('.txt', '')
	    chapter_list.append(int(item))
    with open('902' + '.txt', 'w') as result_file:
        for item in sorted(chapter_list):
            with open(dir_path + '/' + str(item)+'.txt', 'r') as f:
                result_file.write(f.read())
                result_file.write('\n')
