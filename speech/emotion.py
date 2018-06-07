# coding=utf-8
import requests
import json
import urllib3
# api_key = 'Jea6911P80dA0_ssZh2PB5OGVa3UEydY'
# api_secret = 'S4ktX1oHIYM4y0oYma8PeNU0ggRwAotU'
# url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
baidu_api_key = 'EFyvZdR9hTRLq8WashTfOD2u'
baidu_api_secret = 'cCDW3uiiQqYqYp1rYC8vUMTLzWWNtxpQ'
# data = {
#     'api_key': api_key,
#     'api_secret': api_secret,
#     'image_file': open('8.jpg', 'rb')
# }
# header = {'Content-Type': 'application/json'}
#
# response = requests.post(url=url, headers=header, params=data)
# print(response.content)
# request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
# params = "{\"image\":\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"face_field\":\"faceshape,facetype\"}"
#
# access_token = '[调用鉴权接口获取的token]'
# request_url = request_url + "?access_token=" + access_token
# request = urllib2.Request(url=request_url, data=params)
# request.add_header('Content-Type', 'application/json')
# response = urllib2.urlopen(request)
# content = response.read()
# if content:
#     print content