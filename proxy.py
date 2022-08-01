import json
import os


# This is for TPB proxies
class Proxy:
    up = False

    __json = []
    __path = ""

    def __init__(self, path):
        if not os.path.exists(path):
            self.up = False
            return
        self.__path = path
        self.__load_json()

    def __load_json(self):
        f = open(self.__path)
        self.__json = json.load(f)
        f.close()

