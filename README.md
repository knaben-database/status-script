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

### Notes

 - Caching does not update from the script. This needs to be done manually instead