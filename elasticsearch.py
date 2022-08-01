from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class Elasticsearch:
    up = False

    __host = "http://127.0.0.1:9200"
    __hosts = [
        "http://127.0.0.1:9200",
        "http://192.168.1.137:9200"
    ]

    __db = "torrent_cache2"

    def __init__(self):
        self.up = self.__check_basics()

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
