import cv2
import gi
import random
import requests
import json
import os

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

box = [50, 60, 200, 410, 0.99, 'person']
color = [random.randint(0, 255) for _ in range(3)]


def server():
    url = "http://192.168.1.100:18000/api/v1/devices/channelstream?device=1&channel=1&protocal=FLV"
    response = requests.get(url)
    result = json.loads(response.text)
    cap = cv2.VideoCapture(result['EasyDarwin']['Body']['URL'])
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            fontanel = 2
            c1, c2 = (box[0], box[1]), (box[2], box[3])
            frame = cv2.rectangle(frame, c1, c2, color, fontanel, cv2.LINE_AA)
            cv2.imshow('frame',frame)
            # out.write(frame)
            # data = frame.tostring()

            # url = "http://localhost:10008/api/v1/stream/start"
            # respond = requests.post(url=url, data=data)
            # print(respond.text)
    cap.release()
    # out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    server()
