import os
import subprocess
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import requests


class Jackett:
    up = False

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

    __cookie = ""

    def __init__(self):
        self.up = self.__check_basics()
        if self.up:
            self.__login()

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
        self.__cookie = sess.cookies['Jackett']

        return True
