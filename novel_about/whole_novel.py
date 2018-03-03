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
    dir_path = '/home/novel/everedit' + data[0]
    return dir_path


def get_chapter_title(chapter_id):
    conn = connect_db()
    cursor = conn.cursor()
    sql_command = """select title from chapter_list where chapter_id='%s'""" % chapter_id
    cursor.execute(sql_command)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    chapter_title = data[0]
    return chapter_title


if __name__ == '__main__':
    book_name = sys.argv[1]
    dir_path = get_dir_path(book_name)
    file_names = os.listdir(dir_path)
    with open(book_name + '.txt', 'w') as result_file:
        for item in file_names:
            with open(dir_path + '/' + item, 'r') as f:
                chapter_id = item.replace('.txt', '')
                chapter_title = get_chapter_title(chapter_id)
                print('resolving', chapter_title)
                result_file.write(chapter_title + '\n')
                result_file.write(f.read())
                result_file.write('\n')
