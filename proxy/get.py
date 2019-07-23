# coding=utf-8
import json
import requests
import time

with open('proxy.txt', 'r') as f:
    proxy_list = json.load(f)
url = 'http://www.bisige8.net/forum.php?x=1723721'
for item in proxy_list:
    proxy = dict()
    proxy[item['TYPE']] = item['IP']
    s = requests.session()
    s.get(url, proxies=proxy)
    # response = requests.get(url, proxies=proxy)
    # print(response)
    print(proxy, 'ok')
    time.sleep(1)
