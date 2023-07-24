import cv2
import gi
import random
import requests
import json

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

box = [50, 60, 200, 410, 0.99, 'person']
color = [random.randint(0, 255) for _ in range(3)]


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        url = "http://192.168.1.100:18000/api/v1/devices/channelstream?device=1&channel=1&protocal=FLV"
        response = requests.get(url)
        result = json.loads(response.text)
        self.cap = cv2.VideoCapture(result['EasyDarwin']['Body']['URL'])
        # self.cap = cv2.VideoCapture("rtmp://192.168.1.107:19350/hls/stream_1_0")
        # http://192.168.1.107:18000/api/v1/devices/channelstream?device=1&channel=1&protocal=FLV
        # rtsp://admin:ax123456@192.168.1.123:554/h264/ch1/main/av_stream
        # self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.number_frames = 0
        self.fps = 25
        self.duration = 40000000.0
        # self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)) % 100  #
        # self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        """
            appsrc:使应用程序能够提供缓冲区写入管道; 
            block: 每块推送buffer块的最大字节;
            is-live：当前推送的是否直播数据；
            caps：过滤器
            rtph264pay:把H264 视频数据编码进RTP包
        """

        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=fast tune=zerolatency threads=4 ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96'.format(self.width,
                                                                                     self.height,
                                                                                     self.fps)

    def on_need_data(self, src, lenght):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                fontanel = 2
                c1, c2 = (box[0], box[1]), (box[2], box[3])
                frame = cv2.rectangle(frame, c1, c2, color, fontanel, cv2.LINE_AA)

                data = frame.tostring()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                reveal = src.emit('push-buffer', buf)
                # print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                #                                                                        self.duration,
                #                                                                        self.duration / Gst.SECOND))
                if reveal != Gst.FlowReturn.OK:
                    print(reveal)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)

        self.set_service("8555")
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.get_mount_points().add_factory("/test", self.factory)
        self.attach(None)
        data = {
            "Enable": 1,
            "OnDemand": 1,
            "Name": "通道01",
            "Protocol": "RTSP",
            "RtspUrl": "rtsp://192.168.1.107:8555/test",
            "Transport": "TCP",
            "Onvif": "",
            "EnableRecord": 1,
            "RecordUrl": "",
            "RecordPlan": "0",
            "EnableAudio": 0,
            "EnableCdn": 0,
            "CdnUrl": "",
            "ChannelNum": 0,
            "ParentDeviceID": 1,
            "Online": 0,
            "SnapUrl": ""
        }
        url = "http://192.168.1.107:18000/api/v1/addchannel"
        respond = requests.post(url=url, data=json.dumps(data))
        print(respond.text)


if __name__ == '__main__':
    GObject.threads_init()
    Gst.init(None)
    server = GstServer()
    loop = GObject.MainLoop()
    loop.run()
