import cv2
import requests
import json
import random

url = "http://192.168.1.100:18000/api/v1/devices/channelstream?device=1&channel=1&protocal=FLV"
response = requests.get(url)
result = json.loads(response.text)
cap = cv2.VideoCapture(result['EasyDarwin']['Body']['URL'])
#cap = cv2.VideoCapture(url)


def show_video(caps):
    while caps.isOpened():
        ret, frame = caps.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    caps.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    show_video(cap)

