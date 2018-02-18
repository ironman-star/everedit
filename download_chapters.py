# coding=utf-8
import pymysql
import requests
from bs4 import BeautifulSoup
import re
import os


def put_data_into_database(target, title, sql_id, db, path):
    response = requests.request('get', url=target)
    soup = BeautifulSoup(response.content, 'html.parser')
    word = soup.find('div', id='BookText').text.replace('\xa0', ' ').replace('   ', '\n')
    book_id = path.split('/')[3]
    path = path[1:]
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(path+sql_id+'.txt', 'w')as f:
        f.write(word)
    cursor = db.cursor()
    sql_command = "insert into chapter_list (book_id, title, chapter_id) values (%s,'%s',%s);" % (
        book_id, title, sql_id)
    try:
        cursor.execute(sql_command)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        print('something is wrong')


def download_single_novel(content_url, path):
    response1 = requests.get(content_url).content

    soup1 = BeautifulSoup(response1, 'html.parser')
    main_chapter = BeautifulSoup(str(soup1.find('div', id='main')), 'html.parser')
    all_chapter = main_chapter.find_all('a')
    database = pymysql.connect("localhost", "root", "zxc19901225", "novel", charset="utf8")
    for chapter in all_chapter:
        chapter_number = re.search('\d+', str(chapter)).group(0)
        title = BeautifulSoup(str(chapter), 'html.parser').text
        url = content_url + chapter_number + '.html'
        put_data_into_database(url, title, chapter_number, database, path)


if __name__ == '__main__':
    db = pymysql.connect('localhost', 'root', 'zxc19901225', 'novel', charset='utf8')
    cursor = db.cursor()
    mysql_command = 'select book_local from novel_list;'
    cursor.execute(mysql_command)
    novel_local = cursor.fetchall()
    local_list = []
    for tuples in novel_local:
        for local in tuples:
            print('start download of', local)
            url = 'https://m.uuxs.la' + local
            download_single_novel(url, local)
            print('done!')