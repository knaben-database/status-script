import json
import os
import time
import subprocess
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import requests


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except Exception as e:
        return False
    return True


class Jackett:
    up = False
    ms = 0
    speed_percentage = 0.0

    __ms_range = {
        "min": 2000,
        "max": 10000,
        "down": 16000
    }

    __host = "http://127.0.0.1:9117"
    __hosts = [
        "http://127.0.0.1:9117",
        "http://192.168.1.137:9117"
    ]

    __passLoc = "/mnt/incognito/Documents/default2.tyx"
    __passLocs = [
        "/mnt/incognito/Documents/default2.tyx",
        "/home/***REMOVED***/Documents/default2.tyx"
    ]

    __cookie = {"name": "Jackett", "value": ""}

    __full_indexers = {}
    __indexers = {}

    __save_path = ""

    def check(self):
        self.up = self.__check_basics()
        if not self.up:
            return

        # Try 2 times to grab the indexers
        indexers = self.__get_indexers()
        if not indexers:
            self.__login()
            indexers = self.__get_indexers()
            if not indexers:
                self.up = False
                return

        self.__full_indexers = indexers
        # To save a bit of energy, just do this handle the indexers in the check
        self.__handle_indexers()
        self.__test()

        # Check if all indexers are down
        found_working = False
        for index in self.__indexers:
            if "up" in index and index["up"]:
                found_working = True
        self.up = found_working

        # Updating speed percentage
        self.speed_percentage = (self.__ms_range["max"] - max(self.ms - self.__ms_range["min"], 0)) / self.__ms_range["max"]

    def __test(self):
        longest_time = {
            "name": "",
            "ms": 0
        }

        c = 0
        for index in self.__indexers:
            url = self.__host + "/api/v2.0/indexers/" + index["id"] + "/test"
            print("Testing: " + index["name"] + " ...", end=" ")
            start = time.time()

            req = Request(url, method="POST")
            req.add_header("Cookie", self.__cookie["name"] + "=" + self.__cookie["value"])
            try:
                response = urlopen(req, timeout=16)
            except HTTPError as e:
                print("(Failed)\nFailed to connect to: ", url)
                print('Error code:', e.code)
                time_took = (time.time() - start) * 1000
                self.__indexers[c]["ms"] = time_took
                self.__indexers[c]["up"] = False
                error = e.read().decode("utf-8")
                if is_json(error) and "error" in json.loads(error):
                    JSON = json.loads(error)
                    self.__indexers[c]["last_error"] = JSON["error"]
                else:
                    self.__indexers[c]["last_error"] = str(e.code)
                c += 1
                continue
            except URLError as e:
                print("(Failed)\nFailed to reach server: ", url)
                print('Reason:', e.reason)
                time_took = (time.time() - start) * 1000
                self.__indexers[c]["ms"] = time_took
                self.__indexers[c]["up"] = False
                self.__indexers[c]["last_error"] = e.reason
                c += 1
                continue

            if 200 > response.getcode() or response.getcode() >= 300:
                print("(Failed)\n" + index["name"] + " Gave a non-200 response: Code " + str(response.getcode()))
                time_took = (time.time() - start) * 1000
                self.__indexers[c]["ms"] = time_took
                self.__indexers[c]["up"] = False
                self.__indexers[c]["last_error"] = index["name"] + " Gave a non-200 response: Code " + str(response.getcode())
                c += 1
                continue

            time_took = (time.time() - start) * 1000
            self.__indexers[c]["ms"] = time_took
            self.__indexers[c]["up"] = True
            print("(" + str(int(time_took)) + "ms)")
            if time_took > longest_time["ms"]:
                longest_time = {
                    "name": index["name"],
                    "ms": time_took
                }
            c += 1

        print("Slowest indexer: " + longest_time["name"] + " of " + str(int(longest_time["ms"])) + " ms")
        self.ms = longest_time["ms"]

        # Save the result
        self.__save_json(self.__indexers)

    def __handle_indexers(self):
        new_indexes = []
        for index in self.__full_indexers:
            if not index["configured"]:
                continue
            cats = []
            for cat in index["caps"]:
                #print("Comparing: " + str(cat["Name"].encode("ascii", "ignore")) + " > " + str(cat["Name"].encode("utf-8")))
                if len(cat["Name"].encode("utf-8")) > len(cat["Name"].encode("ascii", "ignore")):
                    continue
                cats.append(cat)
            index["caps"] = cats
            new_indexes.append(index)
        self.__indexers = new_indexes

    def __get_indexers(self):
        url = self.__host + "/api/v2.0/indexers?_=" + str(int(time.time() * 1000))

        req = Request(url, method="GET")
        req.add_header("Cookie", self.__cookie["name"] + "=" + self.__cookie["value"])
        try:
            response = urlopen(req, timeout=16)
        except HTTPError as e:
            print("Failed to connect to: ", url)
            print('Error code: ', e.code)
            self.up = False
            return False
        except URLError as e:
            print("Failed to reach server: ", url)
            print('Reason: ', e.reason)
            self.up = False
            return False

        content = response.read().decode("utf-8")
        if not is_json(content):
            return False
        return json.loads(content)

    def __init__(self, save_path=""):
        if save_path == "":
            print("Jackett class reqires a save path")
            exit(1)
        self.__save_path = save_path
        self.up = self.__check_basics()
        if self.up:
            self.__login()

    # Checking if the connection is up
    def __touch_connection(self, host):
        req = Request(host, method="HEAD")
        try:
            response = urlopen(req, timeout=16)
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

    # Checking if the password file exists
    def __touch_file(self, loc):
        return os.path.exists(loc)

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

        # Checking file locations
        success = False
        for loc in self.__passLocs:
            if self.__touch_file(loc):
                self.__passLoc = loc
                success = True
                break
        if not success:
            return False

        # Checking save location
        if not self.__touch_file(self.__save_path):
            return False

        return True

    def __login(self):
        passw = subprocess.run(['detyx', '-j', self.__passLoc],
                               stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        passw = bytes.fromhex(passw).decode('utf-8')
        passw = passw[::-1]

        payload = {'password': passw}
        user_agent = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K)"
        url = self.__host + '/UI/Dashboard'
        browser_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.mail.com/int/",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent
        }

        sess = requests.Session()
        sess.post(url, headers=browser_headers, data=payload)
        self.__cookie["value"] = sess.cookies[self.__cookie["name"]]

        return True

    def __save_json(self, content):
        with open(self.__save_path, 'w', encoding='utf8') as json_file:
            json.dump(content, json_file, indent=4, ensure_ascii=False)
