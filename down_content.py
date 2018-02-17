# coding=utf-8
import re
import requests
import pymysql
from bs4 import BeautifulSoup
import sys


def put_data_into_database(target, title, sql_id, db):
    response = requests.request('get', url=target)
    soup = BeautifulSoup(response.content, 'html.parser')
    word = soup.find('div', id='BookText').text.replace('\xa0', ' ').replace('   ', '\n')
    cursor = db.cursor()
    sql_command = "insert into novel_1 (id, title, content) values (%s,'%s','%s');" % (sql_id, title, word)
    try:
        cursor.execute(sql_command)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        print('something is wrong')


def download_single_novel(content_url):
    response1 = requests.get(content_url).content
    soup1 = BeautifulSoup(response1, 'html.parser')
    main_chapter = BeautifulSoup(str(soup1.find('div', id='main')), 'html.parser')
    all_chapter = main_chapter.find_all('a')
    db = pymysql.connect("localhost", "root", "zxc19901225", "novel", charset="utf8")
    for chapter in all_chapter:
        a = re.search('\d+', str(chapter)).group(0)
        title = BeautifulSoup(str(chapter), 'html.parser').text
        print(title)
        url = content_url + a + '.html'
        put_data_into_database(url, title, a, db)


if __name__ == '__main__':
    novel_url = sys.argv[1]
    download_single_novel(novel_url)
