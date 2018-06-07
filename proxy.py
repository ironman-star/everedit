# coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import re

ip = 'https://www.kuaidaili.com/free/inha/'

all_pro = []
for i in xrange(1, 20):
    print 'Get the page of', i
    try:
        response = requests.get(ip + str(i))
        print 'Get page success!'
    except:
        print 'Get the page of', i, 'failed.'
        break
    soup = BeautifulSoup(response.content, 'html.parser')
    trs = soup.tbody.findAll('tr')
    for item in trs:
        single_pro = dict()
        single_pro['IP'] = item.contents[1].string + ':' + item.contents[3].string
        single_pro['TYPE'] = item.contents[7].string
        all_pro.append(single_pro)
    print i, 'page is ok!'
with open('proxy.txt', 'w')as f:
    f.write(json.dumps(all_pro, indent=4))
