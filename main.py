# imports
import json
import os

# Includes
from jackett import Jackett
from proxy import Proxy
from elasticsearch import Elasticsearch
from colors import colorsBetween, Color


def load_json(path):
    f = open(path)
    JSON = json.load(f)
    f.close()
    return JSON


# /mnt/incognito/var/www/pi2/python/status-script
scriptPath = os.path.dirname(os.path.realpath(__file__))

# /mnt/incognito/var/www/pi2
document_root = scriptPath + "/../.."

# Loading status json
statusJSON = load_json(document_root + "/json/status.json")

# Loading classes
proxy = Proxy(document_root + "/json/proxies.json")
jackett = Jackett(document_root + "/json/indexers.json")
elasticsearch = Elasticsearch()

for x in range(1):
    # Checking proxies
    proxy.check()
    statusJSON["services"]["proxy"]["info_color"] = colorsBetween("#FF0000", "#00FF00", proxy.speed_percentage)
    statusJSON["services"]["proxy"]["up"] = proxy.up
    # Checking database
    elasticsearch.check()
    statusJSON["services"]["database"]["info_color"] = colorsBetween("#FF0000", "#00FF00", elasticsearch.speed_percentage)
    statusJSON["services"]["database"]["up"] = elasticsearch.up
    # Checking Jackett
    jackett.check()
    statusJSON["services"]["livesearch"]["info_color"] = colorsBetween("#FF0000", "#00FF00", jackett.speed_percentage)
    statusJSON["services"]["livesearch"]["up"] = jackett.up

    print()
    print("Summary:")
    print(statusJSON["services"]["proxy"]["info_color"])
    print(statusJSON["services"]["database"]["info_color"])
    print(statusJSON["services"]["livesearch"]["info_color"])
