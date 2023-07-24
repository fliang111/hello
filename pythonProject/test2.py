import requests
import json


def ttt():
    data = {
        "url": ""
    }
    url = "http://localhost:10008/api/v1/stream/start"
    respond = requests.post(url=url, data=json.dumps(data))
    print(respond.text)


if __name__ == '__main__':
    ttt()
