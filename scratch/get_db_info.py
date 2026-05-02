import requests, json
HEADERS = {"Authorization": "Bearer rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK", "Accept": "application/json"}
DB_ID = "dpg-d7qqnpnlk1mc73cnrd2g-a"

r = requests.get(f"https://api.render.com/v1/postgres/{DB_ID}/connection-info", headers=HEADERS, timeout=30)
print("Connection Info:", r.status_code)
if r.ok:
    print(json.dumps(r.json(), indent=2, default=str))
else:
    print(r.text[:500])

# Also get full postgres info
r2 = requests.get(f"https://api.render.com/v1/postgres/{DB_ID}", headers=HEADERS, timeout=30)
print()
print("Full Info:", r2.status_code)
if r2.ok:
    data = r2.json()
    important_keys = ["internalConnectionString", "externalConnectionString", "psqlCommand", "databaseName", "databaseUser", "status"]
    for key in important_keys:
        val = data.get(key, "N/A")
        print("  " + key + ": " + str(val))
