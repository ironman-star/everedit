# coding=utf-8
from pyaudio import PyAudio, paInt16
import numpy as np
import wave
import requests
import json
import base64
import time


class Recoder:
    def __init__(self):
        self.NUM_SAMPLES = 2000  # pyAudio内部缓存的块的大小
        self.SAMPLING_RATE = 8000  # 取样频率
        self.LEVEL = 3000  # 声音保存的阈值
        self.COUNT_NUM = 100  # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
        self.SAVE_LENGTH = 8  # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样

    def start_recoder(self):
        pa = PyAudio()
        stream = pa.open(format=paInt16,
                         channels=1,
                         rate=self.SAMPLING_RATE,
                         input=True,
                         frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        print('开始录音...')
        while True:
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum(audio_data > self.LEVEL)
            # todo print(np.max(audio_data))此处应该有输出说话的一些参数
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1

            if save_count < 0:
                save_count = 0

            if save_count > 0:
                # 将要保存的数据存放到save_buffer中
                save_buffer.append(string_audio_data)
            else:
                # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                if len(save_buffer) > 0:
                    filename = "test2.wav"
                    self.save_wave_file(filename, save_buffer)
                    save_buffer = []
                    print(filename, "saved")
                    bdr = BaiduRest("mike_test_for_python")
                    return bdr.get_text(filename)

    def save_wave_file(self, filename, data):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(b''.join(data))
        wf.close()


class BaiduRest:
    def __init__(self, cu_id):
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        self.get_voice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        self.up_voice_url = 'http://vop.baidu.com/server_api'
        self.cu_id = cu_id
        self.token = self.get_token()
        return

    def get_token(self):
        try:
            with open('token.json', 'r') as f:
                data = json.load(f)
            if int(time.time()) < data['time'] + data['expires_in']:
                print('从文件中获取token成功.')
                return data['access_token']
            else:
                print('Token已过期,正在重新获取...')
        except:
            print('Json file is  missing, reload.')
        token_url = self.token_url % ("W15XB5M9h8S566Z6PByqfsqR", "f708b35697899cf82008c3d843cb3066")
        r_str = requests.get(token_url).content
        token_str = json.loads(r_str)
        token_str['time'] = int(time.time())
        with open('token.json', 'w') as f:
            f.write(json.dumps(token_str, indent=4))
            print('获取Token成功.')
        return self.get_token()

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
    def get_text(self, filename):
        data = dict()
        data['format'] = 'wav'
        data['rate'] = 8000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token
        wav_fp = open(filename, 'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        response = requests.post(self.up_voice_url, post_data)
        data = json.loads(response.content.decode('utf-8'))
        print('获取语音信息:', data['err_msg'])
        if data['err_msg'] == 'speech quality error.':
            return None
        return ",".join(data['result'])


if __name__ == '__main__':
    recorder = Recoder()
    while True:
        print(recorder.start_recoder())