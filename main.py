#!/usr/bin/python3

# imports
import json
import os
import time

# Includes
from jackett import Jackett
from proxy import Proxy
from elasticsearch import Elasticsearch
from colors import colorsBetween, Color

def generate_json():
    return {
      "services": {
        "proxy": {
          "name": "Proxy",
          "up": True,
          "info": "Unknown",
          "info_color": "#666666",
          "ms": 57.90209770202637
        },
        "database": {
          "name": "Database",
          "up": True,
          "info": "Unknown",
          "info_color": "#666666",
          "ms": 6.021022796630859
        },
        "livesearch": {
          "name": "Live Search",
          "up": True,
          "info": "Unknown",
          "info_color": "#666666",
          "ms": 3938.007593154907
        },
        "caching": {
          "name": "Caching",
          "up": True,
          "info": "Running",
          "info_color": "#38bf38",
          "ms": None
        }
      },
      "description": "",
      "last_checked": int(time.time())
    }

def load_json(path):
    f = open(path)
    JSON = json.load(f)
    f.close()
    return JSON


def save_json(path, content: json):
    f = open(path, "w")
    json.dump(content, f, indent=4)
    f.close()


def percentageToInfo(percentage):

    # Range between 1.00 and 0.00
    percentage = max(percentage, 0.0)
    percentage = min(percentage, 1.0)

    if percentage > 0.8:
        return "Running"
    elif percentage > 0.6:
        return "Running"
    elif percentage > 0.4:
        return "Running slow"
    elif percentage > 0.25:
        return "Running VERY slow"
    else:
        return "Running VERY slow, be patient!"


# /mnt/incognito/var/www/pi2/python/status-script
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

# /mnt/incognito/var/www/pi2
#DOCUMENT_ROOT = SCRIPT_PATH + "/../.."
#STATUS_PATH = DOCUMENT_ROOT + "/json/status.json"
STATUS_PATH = os.environ.get("STATUS_PATH", "/shared-data/status.json")

# Loading classes
proxy = Proxy(os.environ.get("PROXIES_PATH", "/shared-data/proxies.json"))
jackett = Jackett("/shared-data/indexers.json")
elasticsearch = Elasticsearch()

while True:
    # Loading status json
    if not os.path.exists(STATUS_PATH):
        statusJSON: json = generate_json()
    else:
        statusJSON: json = load_json(STATUS_PATH)

    # Checking proxies
    proxy.check()
    statusJSON["services"]["proxy"]["info_color"] = colorsBetween("#FF0000", "#38BF38", proxy.speed_percentage) if proxy.up else "#FF0000"
    statusJSON["services"]["proxy"]["info"] = percentageToInfo(proxy.speed_percentage) if proxy.up else "Offline"
    statusJSON["services"]["proxy"]["up"] = proxy.up
    statusJSON["services"]["proxy"]["ms"] = proxy.ms

    # Checking database
    elasticsearch.check()
    statusJSON["services"]["database"]["info_color"] = colorsBetween("#FF0000", "#38BF38", elasticsearch.speed_percentage) if elasticsearch.up else "#FF0000"
    statusJSON["services"]["database"]["info"] = percentageToInfo(elasticsearch.speed_percentage) if elasticsearch.up else "Offline"
    statusJSON["services"]["database"]["up"] = elasticsearch.up
    statusJSON["services"]["database"]["ms"] = elasticsearch.ms

    # Checking Jackett
    jackett.check()
    statusJSON["services"]["livesearch"]["info_color"] = colorsBetween("#FF0000", "#38BF38", jackett.speed_percentage) if jackett.up else "#FF0000"
    statusJSON["services"]["livesearch"]["info"] = percentageToInfo(jackett.speed_percentage) if jackett.up else "Offline"
    statusJSON["services"]["livesearch"]["up"] = jackett.up
    statusJSON["services"]["livesearch"]["ms"] = jackett.ms

    # General
    statusJSON["last_checked"] = int(time.time())

    print()
    print("---- Summary ----")

    print("Proxy: ")
    print("   working: " + str(proxy.up))
    print("       url: " + proxy.getSelected())
    print("      ping: " + str(round(proxy.ms)) + "ms (" + str(round(proxy.speed_percentage * 100)) + "%)")

    print("Elasticsearch: ")
    print("   working: " + str(elasticsearch.up))
    print("      ping: " + str(round(elasticsearch.ms)) + "ms (" + str(round(elasticsearch.speed_percentage * 100)) + "%)")
    # TODO: db health

    print("Live search: ")
    print("   working: " + str(jackett.up))
    print("      ping: " + str(round(jackett.ms)) + "ms (" + str(round(jackett.speed_percentage * 100)) + "%)")
    indexers = jackett.getIndexers()
    print("  trackers: ", end="")
    c = 0
    for index in indexers:
        if c == 0:
            print(index["name"] + " - " + str(round(index["ms"])) + "ms - " + ("OK" if index["up"] else "Error: " + index["error"]))
        else:
            print("            " + index["name"] + " - " + str(round(index["ms"])) + "ms - " + ("OK" if index["up"] else "Error: " + index["error"]))
        c += 1

    # Saving result
    save_json(STATUS_PATH, statusJSON)

    # ZZZZZZZzzzzzzzzzzzZZZZZZZZZZzz
    print("\nZZZZZZZzzzzzzzzzzzZZZZZZZZZZzz")
    time.sleep(600)
