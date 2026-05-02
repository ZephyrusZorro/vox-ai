import requests, json
HEADERS = {"Authorization": "Bearer rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK", "Accept": "application/json"}

# 1. Recent deploys
r = requests.get("https://api.render.com/v1/services/srv-d7m7tnho3t8c73e19q30/deploys?limit=5", headers=HEADERS, timeout=30)
print("RECENT DEPLOYS:", r.status_code)
for d in r.json():
    dep = d.get("deploy", d)
    did = dep.get("id", "?")
    status = dep.get("status", "?")
    msg = str(dep.get("commit", {}).get("message", "?"))[:50]
    created = str(dep.get("createdAt", "?"))[:19]
    print(f"  {did}: status={status} | {msg} | {created}")

# 2. Env vars
print("\nENV VARS:")
r2 = requests.get("https://api.render.com/v1/services/srv-d7m7tnho3t8c73e19q30/env-vars", headers=HEADERS, timeout=30)
for ev in r2.json():
    evd = ev.get("envVar", ev)
    key = evd.get("key", "?")
    val = evd.get("value", "")
    if key == "DATABASE_URL":
        print(f"  {key} = {val[:30]}...{val[-20:]}")
    elif key in ("ENVIRONMENT", "PORT", "CORS_ORIGIN", "FORCE_REDEPLOY_ID"):
        print(f"  {key} = {val}")
    else:
        print(f"  {key} = {'(set)' if val else '(empty)'}")
