# coding=utf-8
import requests
import pymysql
import sys
from bs4 import BeautifulSoup


def get_single_page_novels(web_site, db):
    response = requests.get(web_site).content
    soup = BeautifulSoup(response, 'html.parser')
    ul_list = str(soup.find_all('ul', attrs={'class': 'item-list'}))
    soup = BeautifulSoup(ul_list, 'html.parser')
    novel_list = soup.find_all('li')
    cursor = db.cursor()
    for novel_item in novel_list:
        book_local = str(novel_item).split('"')[1]
        book_id = book_local.split('/')[3]
        novel_detail = BeautifulSoup(str(novel_item), 'html.parser').text
        book_type = novel_detail.split(' ')[0].replace('[', '').replace(']', '')
        book_name = novel_detail.split(' ')[1]
        writer = novel_detail.split(' ')[2]
        with open('novel_list.txt', 'a')as f:
            f.write(book_local)
            f.write('\n')
        sql_command = "insert into novel_list (book_id, book_name, book_type, writer, book_local)" \
                      "values(%s,'%s','%s','%s','%s')" % (book_id, book_name, book_type, writer, book_local)
        print(sql_command)
        try:
            cursor.execute(sql_command)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            print('something is wrong')


if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "zxc19901225", "novel", charset="utf8")
    pre_url = 'https://m.uuxs.la/toplist/allvisit-'
    for i in range(1, sys.argv[1]):
        url = pre_url + str(i)
        print('Start of', i, 'page.')
        get_single_page_novels(url, db)
