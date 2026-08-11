from urllib import request, parse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time
import json
import os


class Elasticsearch:
    up = False
    ms = 0
    speed_percentage = 0.0

    __ms_range = {
        "min": 50,
        "max": 200,
        "down": 15000
    }

    __host = "http://127.0.0.1:9200"
    __hosts = [
        # If the script is running on the host
        "http://127.0.0.1:9200",
        # Connecting from local server
        "http://192.168.1.137:9200",
        # for kubernetes
        "http://elasticsearch:9200",
    ]

    __db = os.environ.get("ELASTICSEARCH_TORRENT_INDEX", "torrent_cache")

    def __init__(self):
        self.up = self.__check_basics()

    def check(self):
        self.up = self.__check_basics()
        if not self.up:
            return

        query = {
            "_source": False,
            "query": {
                "query_string": {
                    "query": "test"
                }
            }
        }
        url = self.__host + "/" + self.__db + "/_search"
        data = bytes(json.dumps(query).encode('utf-8'))
        start = time.time()
        req = Request(url, data=data, method="POST", headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            'content-type': 'application/json'
        })
        try:
            r = urlopen(req, timeout=16)
            response = json.loads(r.read().decode('utf-8'))
        except HTTPError as e:
            print("Failed to connect to: ", url)
            print('Error code: ', e.code)
            self.up = False
        except URLError as e:
            print("Failed to reach server: ", url)
            print('Reason: ', e.reason)
            self.up = False
        else:
            # TODO: What is even being checked here??
            if len(response) > 0:
                self.up = True
            else:
                print("Zero responses trying to search for \"test\":", url)
                self.up = False
        end = time.time()
        time_took = (end - start) * 1000
        self.ms = time_took

        # Updating speed percentage
        if time_took > self.__ms_range["down"]:
            self.up = False
        self.speed_percentage = (self.__ms_range["max"] - max(time_took - self.__ms_range["min"], 0)) / self.__ms_range["max"]

    # Private functions
    def __check_basics(self):
        # Checking hosts
        success = False
        for host in self.__hosts:
            if self.__touch_connection(host):
                self.__host = host
                success = True
                break
        if not success:
            return False
        return True

    # Checking if the connection is up
    def __touch_connection(self, host):
        req = Request(host, method="HEAD")
        try:
            response = urlopen(req)
        except HTTPError as e:
            print("Failed to connect to: ", host)
            print('Error code: ', e.code)
            return False
        except URLError as e:
            print("Failed to reach server: ", host)
            print('Reason: ', e.reason)
            return False
        else:
            return True
