# coding=utf-8
import pymysql
import requests
from bs4 import BeautifulSoup
import re
import os
from multiprocessing.dummy import Pool as ThreadPool
import time


def put_data_into_database(target, title, sql_id, path):
    """
    :param target: url of chapter
    :param title: title of chapter
    :param sql_id: saved file's name of chapter
    :param path: saved file's path of chapter
    :return: if didn't get the page (status code is not 200), interrupt.
    """
    # print('start of', sql_id)
    db = pymysql.connect("localhost", "root", "zxc19901225", "novel", charset="utf8")
    response = requests.request('get', url=target)
    if response.status_code != 200:
        print('Got error in getting page of', target)
        return True
    soup = BeautifulSoup(response.content, 'html.parser')
    word = soup.find('div', id='BookText').text.replace('\xa0', ' ').replace('   ', '\n')
    book_id = path.split('/')[3]
    path = path[1:]
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(path + sql_id + '.txt', 'w')as f:
        f.write(word)
    cursor = db.cursor()
    sql_command = "insert into chapter_list (book_id, title, chapter_id) values (%s,'%s',%s);" % (
        book_id, title, sql_id)
    try:
        cursor.execute(sql_command)
        db.commit()
        # print('end of', sql_id)
    except Exception as e:
        print(e, '----------url is', target)
        db.rollback()
        print('something is wrong')


def download_single_novel(content_url, path, exist_id_list):
    print('Starting')
    start_time = time.time()
    pool = ThreadPool(16)
    response1 = requests.get(content_url).content
    soup1 = BeautifulSoup(response1, 'html.parser')
    main_chapter = BeautifulSoup(str(soup1.find('div', id='main')), 'html.parser')
    all_chapter = main_chapter.find_all('a')
    count = 0
    for chapter in all_chapter:
        chapter_number = re.search('\d+', str(chapter)).group(0)
        if int(chapter_number) in exist_id_list:
            continue
        count += 1
        title = BeautifulSoup(str(chapter), 'html.parser').text
        url = content_url + chapter_number + '.html'
        pool.apply_async(put_data_into_database, [url, title, chapter_number, path])
        # if put_data_into_database(url, title, chapter_number, database, path):
        #     continue
    pool.close()
    pool.join()
    end_time = time.time()
    print('The end,', 'download', count, 'chapters, takes', end_time-start_time, 'seconds')


if __name__ == '__main__':
    db = pymysql.connect('localhost', 'root', 'zxc19901225', 'novel', charset='utf8')
    cursor = db.cursor()
    mysql_command = 'select book_local from novel_list;'
    cursor.execute(mysql_command)
    novel_local = cursor.fetchall()
    mysql_command = 'select chapter_id from chapter_list;'
    cursor.execute(mysql_command)
    exist_id_tuple = cursor.fetchall()
    exist_id_list = []
    for item in exist_id_tuple:
        for exist_id in item:
            exist_id_list.append(exist_id)
    local_list = []
    for tuples in novel_local:
        for local in tuples:
            url = 'https://m.uuxs.la' + local
            download_single_novel(url, local, exist_id_list)
