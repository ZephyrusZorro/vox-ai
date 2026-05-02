import requests, json, time
HEADERS = {"Authorization": "Bearer rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK", "Accept": "application/json", "Content-Type": "application/json"}
DB_ID = "dpg-d7qqnpnlk1mc73cnrd2g-a"

print("Waiting for Render Postgres to be ready...")
for i in range(30):
    r = requests.get(f"https://api.render.com/v1/postgres/{DB_ID}", headers=HEADERS, timeout=30)
    if r.ok:
        data = r.json()
        status = data.get("status", "?")
        print(f"  [{i*10}s] Status: {status}")
        
        if status == "available":
            print("\nDatabase is READY!")
            print(f"  Internal URL: {data.get('internalConnectionString', 'N/A')}")
            print(f"  External URL: {data.get('externalConnectionString', 'N/A')}")
            print(f"  Dashboard: {data.get('dashboardUrl', 'N/A')}")
            
            # The internal URL is what we need (same Render network = fast)
            internal = data.get("internalConnectionString", "")
            if internal:
                print(f"\n  >>> USE THIS FOR DATABASE_URL: {internal}")
            break
        
    time.sleep(10)
else:
    print("Timed out waiting for DB to be ready")
    # Still try to get connection info
    r = requests.get(f"https://api.render.com/v1/postgres/{DB_ID}/connection-info", headers=HEADERS, timeout=30)
    print(f"Connection info: {r.status_code}")
    if r.ok:
        print(json.dumps(r.json(), indent=2, default=str)[:500])
