#!/usr/bin/python3
# coding=utf-8

import requests
import json
import base64


class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.获取token
        token_url = self.token_url % (api_key, api_secert)

        r_str = requests.get(token_url).content
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    # def getVoice(self, text, filename):
    #     # 2. 向Rest接口提交数据
    #     get_url = self.getvoice_url % (urllib.parse.quote(text), self.cu_id, self.token_str)
    #
    #     voice_data = urllib.request.urlopen(get_url).read()
    #     # 3.处理返回数据
    #     voice_fp = open(filename, 'wb+')
    #     voice_fp.write(voice_data)
    #     voice_fp.close()
    #     pass
    def getText(self, filename):
        data = {}
        data['format'] = 'wav'
        data['rate'] = 8000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename, 'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        response = requests.post(self.upvoice_url, post_data)
        print(json.loads(response.content.decode('utf-8'))['result'])


if __name__ == "__main__":
    api_key = "W15XB5M9h8S566Z6PByqfsqR"
    api_secert = "f708b35697899cf82008c3d843cb3066"
    # 初始化
    bdr = BaiduRest("mike_test_for_python", api_key, api_secert)
    bdr.getText("test.wav")
