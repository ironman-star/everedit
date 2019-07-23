# coding=utf-8
import requests
import json
# url = 'http://www.qq.com'
proxies = {'http': '118.31.220.3:8080'}
url = 'http://www.bisige8.com/forum.php'
params = {'x': '27835'}
headers = {'User-Agent': "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
response = requests.get(url, params=params, proxies=proxies, headers=headers)

print(response.status_code)
