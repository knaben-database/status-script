# status-script

Script to update status.json and populate indexers.json with mapped categories

### status.json template

```json
{
  "services": {
    "proxy": {
      "name": "Proxy",
      "up": true,
      "info": "Running",
      "info_color": "#00FF00",
      "ms": 19.3
    },
    "database": {
      "name": "Database",
      "up": true,
      "info": "Running",
      "info_color": "#00FF00",
      "ms": 20.23
    },
    "livesearch": {
      "name": "Live Search",
      "up": true,
      "info": "Running",
      "info_color": "#00FF00",
      "ms": 200.00
    },
    "caching": {
      "name": "Caching",
      "up": false,
      "info": "Offline",
      "info_color": "#FF0000",
      "ms": null
    }
  },
  "description": "Currently ongoing issue with the database, we're working on it",
  "last_changed": 2354235346,
  "last_checked": 3242342345
}
```

### proxies.json template

```json
{
  "proxies": [
    {
      "url": "thepiratebay0.org",
      "https": true,
      "type": "old",
      "api": false,
      "api_url": null,
      "working": true,
      "ms": 213,
      "priority": 1,
      "look_for": "/\" title=\"Browse "
    },
    {
      "url": "thepiratebay.org",
      "https": true,
      "type": "new",
      "api": true,
      "api_url": "https://apibay.org",
      "working": true,
      "ms": 83,
      "priority": 2,
      "look_for": ",\"name\":\""
    },
    {
      "url": "thepiratebay10.org",
      "https": true,
      "type": "old",
      "api": false,
      "api_url": null,
      "working": true,
      "ms": 456,
      "priority": 3,
      "look_for": "/\" title=\"Browse "
    },
    {
      "url": "thehiddenbay.com",
      "https": true,
      "type": "old",
      "api": false,
      "api_url": null,
      "working": true,
      "ms": 321,
      "priority": 4,
      "look_for": "/\" title=\"Browse "
    }
  ],
  "last_updated": 1242342345,
  "last_checked": 1342342345
}
```

### Notes

 - Caching does not update from the script. This needs to be done manually instead