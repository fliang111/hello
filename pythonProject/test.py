import cv2

url = "rtsp://admin:ax123456@192.168.1.123:554/h264/ch1/main/av_stream"
cap = cv2.VideoCapture(url)


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

