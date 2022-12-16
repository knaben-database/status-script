import json
import socket
import time
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# This is for TPB proxies
class Proxy:
    up = False
    ms = 0
    speed_percentage = 0.0

    __ms_range = {
        "min": 1800,
        "max": 10000,
        "down": 16000
    }

    __json = []
    __path = ""

    __chosen = ""

    def __init__(self, path):
        if not os.path.exists(path):
            self.up = False
            return
        self.__path = path
        self.__json = self.__load_json()

    def check(self):
        if not os.path.exists(self.__path):
            self.up = False
            print(self.__path + " was not found!")
            return

        proxy_json = self.__load_json()
        proxies = proxy_json["proxies"]
        proxies.sort(key=lambda JSON: JSON["priority"])
        c = 0
        for proxy in proxies:
            url = ""
            if proxy["api"]:
                url = proxy['api_url'] + "/precompiled/data_top100_recent.json"
            elif proxy['https']:
                url = "https://" + proxy['url'] + "/recent"
            else:
                url = "http://" + proxy['url'] + "/recent"

            start = time.time()
            req = Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            try:
                r = urlopen(req, timeout=16)
                response = r.read().decode('utf-8')
            except HTTPError as e:
                print("Failed to connect to: ", url)
                print('Error code: ', e.code)
                proxies[c]["working"] = False
            except URLError as e:
                print("Failed to reach server: ", url)
                print('Reason: ', e.reason)
                proxies[c]["working"] = False
            except TimeoutError as e:
                print("Failed to reach server: ", url)
                print('Reason: ', "Timeout")
                proxies[c]["working"] = False
            except socket.timeout as e:
                print("Failed to reach server: ", url)
                print('Reason: ', "Timeout")
                proxies[c]["working"] = False
            else:
                if proxy["look_for"] in response:
                    proxies[c]["working"] = True
                else:
                    proxies[c]["working"] = False
            end = time.time()
            proxies[c]["ms"] = (end - start) * 1000
            c += 1

        # Check if all proxies are down
        found_working = False
        for proxy in proxies:
            if proxy["working"]:
                if not found_working:
                    self.ms = proxy["ms"]
                    self.speed_percentage = (self.__ms_range["max"] - max(proxy["ms"] - self.__ms_range["min"], 0)) / self.__ms_range["max"]
                    self.__chosen = proxy["url"]
                    print("Chosen       ↓↓↓")
                print("Working: " + proxy["url"])
                found_working = True
            else:
                print("DOWN: " + proxy["url"])
        self.up = found_working
        proxy_json["proxies"] = proxies
        proxy_json["last_updated"] = int(time.time())
        self.__save_json(proxy_json)

    def getSelected(self) -> str:
        return self.__chosen

    def __load_json(self):
        f = open(self.__path, "r")
        JSON = json.load(f)
        f.close()
        return JSON

    def __save_json(self, content):
        out_file = open(self.__path, "w")
        json.dump(content, out_file, indent=4)
        out_file.close()