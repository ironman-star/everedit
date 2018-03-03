import pymysql
import sys
import os


def connect_db():
    conn = pymysql.connect("localhost", "root", "zxc19901225", "novel", charset="utf8")
    return conn


def get_dir_path(book_name):
    conn = connect_db()
    cursor = conn.cursor()
    sql_command = """select book_local from novel_list where book_name='%s'""" % book_name
    cursor.execute(sql_command)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    dir_path = '/home' + data[0]
    return dir_path


def get_chapter_title(book_name):
    dir_path=get_dir_path(book_name)
    book_id=dir_path.split('/')[-2]
    conn = connect_db()
    cursor = conn.cursor()
    sql_command = """select chapter_id, title from chapter_list where book_id='%s'""" % book_id
    cursor.execute(sql_command)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    temp={}
    for item in data:
        temp[str(item[0])] = item[1]
    return temp


if __name__ == '__main__':
    book_name = sys.argv[1]
    dir_path = get_dir_path(book_name)
    file_names = os.listdir(dir_path)
    id_chapter = get_chapter_title(book_name)
    with open(book_name + '.txt', 'w') as result_file:
        for item in file_names:
            with open(dir_path + '/' + item, 'r') as f:
                chapter_id = item.replace('.txt', '')
                chapter_title = id_chapter[chapter_id]
                print('resolving', chapter_title)
                result_file.write(chapter_title + '\n')
                result_file.write(f.read())
                result_file.write('\n')
