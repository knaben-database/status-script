# imports
import json
import os

# Includes
from jackett import Jackett
from proxy import Proxy
from elasticsearch import Elasticsearch


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
jackett = Jackett()
elasticsearch = Elasticsearch()

print(scriptPath)
