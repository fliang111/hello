import subprocess

import cv2
import requests
import json
import random

box = [50, 60, 200, 410, 0.99, 'person']
color = [random.randint(0, 255) for _ in range(3)]
def draw_something(frame):
    # 画框， 注意：若画的线太细经过缩放线可能消失
    frame = cv2.rectangle(frame, (260, 230), (1660, 690), (0, 0, 255), 2)
    # 图片缩放a
    frame = cv2.resize(frame, (1280, 720))
    return frame


#rtmp = "rtmp://192.168.1.102:1935/live/livestream"
rtmp = "rtmp://10.151.31.149/live/livestream"

Start = 0  # 从第Start秒播放视频
#url = "http://192.168.1.101:18000/api/v1/devices/channelstream?device=2&channel=2&protocal=WEBRTC"
#url = "webrtc://192.168.1.101:18000/rtc/stream_2_0"
url = "rtsp://admin:hik12345@10.158.2.29:554/Streaming/Channels/501"
#response = requests.get(url)
#result = json.loads(response.text)
#video = cv2.VideoCapture(result['EasyDarwin']['Body']['URL'])
video = cv2.VideoCapture(url)

size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
sizeStr = str(size[0]) + 'x' + str(size[1])


command = ['ffmpeg',
    '-y', '-an',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', sizeStr,
    '-r', '25',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    rtmp]
pipe = subprocess.Popen(command
                        , shell=False
                        , stdin=subprocess.PIPE)
while video.isOpened():
    ret,frame = video.read()
    if ret:
        # fontanel = 2
        # c1, c2 = (box[0], box[1]), (box[2], box[3])
        # frame = cv2.rectangle(frame, c1, c2, color, fontanel, cv2.LINE_AA)
        pipe.stdin.write(frame.tostring())
video.release()
pipe.terminate()
