# coding=utf-8
import requests
import datetime


def check_stock():
    url = 'https://bwh1.net/cart.php?a=add&pid=43'
    response = requests.get(url).content.decode('utf-8')
    if 'Out of Stock' not in response:
        print(datetime.datetime.now().strftime("%H:%M:%S"), 'has stock now !!!!!!!!!!!')
        exit(0)
    else:
        print(datetime.datetime.now().strftime("%H:%M:%S"), 'no stock.')
    check_stock()


if __name__ == '__main__':
    check_stock()
