import requests, json
HEADERS = {"Authorization": "Bearer rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK", "Accept": "application/json", "Content-Type": "application/json"}

# List all services
r = requests.get("https://api.render.com/v1/services?limit=20", headers=HEADERS, timeout=30)
print("Services:", r.status_code)
for svc in r.json():
    s = svc.get("service", svc)
    sid = s.get("id", "?")
    name = s.get("name", "?")
    stype = s.get("type", "?")
    print(f"  {sid}: {name} type={stype}")

# Check for Render Postgres
print()
r2 = requests.get("https://api.render.com/v1/postgres?limit=10", headers=HEADERS, timeout=30)
print("Postgres DBs:", r2.status_code)
if r2.ok:
    dbs = r2.json()
    if dbs:
        for db in dbs:
            d = db.get("postgres", db)
            did = d.get("id", "?")
            name = d.get("name", "?")
            status = d.get("status", "?")
            print(f"  {did}: {name} status={status}")
    else:
        print("  No Postgres databases found")
        print("  Creating one now...")
        
        # Create a free Render Postgres
        create_resp = requests.post(
            "https://api.render.com/v1/postgres",
            headers=HEADERS,
            json={
                "name": "lifodial-db",
                "plan": "free",
                "region": "singapore",
                "version": "16",
                "databaseName": "lifodial",
                "databaseUser": "lifodial_user",
                "ownerId": "tea-d6nnrhvafjfc73airla0",
            },
            timeout=30,
        )
        print(f"  Create DB: {create_resp.status_code}")
        if create_resp.ok:
            db_data = create_resp.json()
            print(json.dumps(db_data, indent=2, default=str)[:1000])
        else:
            print(f"  Error: {create_resp.text[:500]}")
else:
    print(f"  Error: {r2.text[:200]}")
