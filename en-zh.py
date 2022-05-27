import pyaudio
import wave
from aip import AipSpeech
import urllib.request
import hashlib
import random
import json
import time # 为了防止54003的频繁访问问题
import pyttsx3
from aip import AipSpeech
import wave, pygame
import time
import random
import sys
import os
os.close(sys.stderr.fileno())
# 用Pyaudio库录制音频
#   out_file:输出音频文件名
#   rec_time:音频录制时间(秒)

def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16  # 16bit编码格式
    CHANNELS = 1  # 单声道
    RATE = 16000  # 16000采样频率

    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT,  # 音频流wav格式
                    channels=CHANNELS,  # 单声道
                    rate=RATE,  # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始记录语音{0}秒后开始识别...".format(rec_time))

    frames = []  # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("结束识别")

    # 保存音频文件
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def audio_recog(recogFile):
    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()


    # 识别本地文件
    result = client.asr(get_file_content(recogFile), 'wav', 16000, {'dev_pid': 1737,})
    return result

def write_file(file,text):
    import time
    time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    f = open(file, 'a')
    f.write(time+':'+text+'\n')
    f.close()

audioFile="audio.wav"
textFile="识别结果.txt"

""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#*******************************************************************

class Trans:
    def __init__(self):
        self._app_id_ = r'20210522000837696'  # app_id
        self._app_key_ = r'Ao060hZrprWRW4jr8FH_' # app_key
        self.app_url = r'https://fanyi-api.baidu.com/api/trans/vip/translate'
        self.from_lang = 'en'
        self.to_lang = 'zh'

    def query(self, query_words):
        salt = random.randint(32768, 65536)
        sign = self._app_id_ + query_words + str(salt) + self._app_key_
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        query_words = urllib.request.quote(query_words)

        query_url = self.app_url + '?appid=' + self._app_id_ + '&q=' + query_words + '&from=' + \
                    self.from_lang + '&to=' + self.to_lang + '&salt=' + str(salt) + '&sign=' + sign

        request = urllib.request.urlopen(query_url).read()
        response = json.loads(request)['trans_result'][0]['dst']
        time.sleep(1)
        return response

#***********************************************************************************


def get_video(msg):
    APP_ID = '24255909'
    API_KEY = '7PPYsgpvNGpWgiOMMM4kc1OB'
    SECRET_KEY = 'F4tV2bwfc31UPIC2H0PoeLQucBhmu8nu'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(msg, 'zh', 1, {
        'vol': 5, 'per': 103, 'aue': 6
    })
    file_name = str(random.randint(1, 999999999)) + str(int(time.time())) + ".wav"
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(file_name, 'wb') as f:
            f.write(result)
        return file_name
    else:
        return None


'''
pip install wave
播放指定音频文件，例如：auid.wav
'''


def paly_mp3(file_name):
    fhandle = wave.open(file_name, "rb")
    params = fhandle.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    fhandle.close()
    pygame.mixer.init(framerate)
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    playTime = nframes / float(framerate)
    time.sleep(playTime)
    pygame.mixer.music.stop()
    # 播放完毕之后删除指定文件
    os.remove(file_name)

if __name__ == '__main__':
    while True:
        audio_record(audioFile, 5)
        textResult = audio_recog("audio.wav")
        if textResult['err_msg'] =="success.":
            # print(textResult['result'])
            c=str(textResult['result'])
            print(c)
            write_file(textFile,str(textResult['result']))
            trans = Trans()
            query_words = c
            results = trans.query(query_words)
            print(results)
            msg_list = [results]
            for msg in msg_list:
                file_name = get_video(msg)
                paly_mp3(file_name)




