import requests, json, time, sys
HEADERS = {"Authorization": "Bearer rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK", "Accept": "application/json", "Content-Type": "application/json"}
SERVICE_ID = "srv-d7m7tnho3t8c73e19q30"

# The internal Render Postgres URL (same datacenter = no network issues)
NEW_DB_URL = "postgresql://lifodial_user:RFCNbNBVark95d4WoL5pe6QjH1BWmsj7@dpg-d7qqnpnlk1mc73cnrd2g-a/lifodial"

# Step 1: Update DATABASE_URL
print("Step 1: Updating DATABASE_URL to Render internal Postgres...")
r = requests.put(
    f"https://api.render.com/v1/services/{SERVICE_ID}/env-vars/DATABASE_URL",
    headers=HEADERS,
    json={"value": NEW_DB_URL},
    timeout=30,
)
print(f"  Status: {r.status_code}")
if r.ok:
    print("  DATABASE_URL updated!")
else:
    print(f"  Error: {r.text[:200]}")
    sys.exit(1)

# Step 2: Trigger deploy
print("\nStep 2: Triggering deploy...")
r2 = requests.post(
    f"https://api.render.com/v1/services/{SERVICE_ID}/deploys",
    headers=HEADERS,
    json={"clearCache": "clear"},
    timeout=30,
)
print(f"  Status: {r2.status_code}")
if r2.ok:
    deploy = r2.json()
    deploy_id = deploy.get("id", "?")
    print(f"  Deploy ID: {deploy_id}")
else:
    print(f"  Error: {r2.text[:200]}")
    sys.exit(1)

# Step 3: Monitor deploy
print(f"\nStep 3: Monitoring deploy {deploy_id}...")
start = time.time()
last_status = ""
while time.time() - start < 600:
    try:
        r3 = requests.get(
            f"https://api.render.com/v1/services/{SERVICE_ID}/deploys/{deploy_id}",
            headers=HEADERS, timeout=30,
        )
        if r3.ok:
            status = r3.json().get("status", "?")
            if status != last_status:
                elapsed = int(time.time() - start)
                print(f"  [{elapsed}s] {status}")
                last_status = status
            
            if status == "live":
                print("  DEPLOY IS LIVE!")
                time.sleep(5)
                try:
                    hr = requests.get("https://lifodial.onrender.com/health", timeout=60)
                    print(f"  Health: {hr.status_code} -> {hr.text[:300]}")
                except Exception as e:
                    print(f"  Health check error: {e}")
                
                # Step 4: Test audit endpoint
                print("\nStep 4: Testing /debug/audit...")
                try:
                    ar = requests.get("https://lifodial.onrender.com/debug/audit", timeout=60)
                    print(f"  Audit: {ar.status_code} -> {ar.text[:500]}")
                except Exception as e:
                    print(f"  Audit error: {e}")
                
                sys.exit(0)
            elif status in ("build_failed", "update_failed", "canceled"):
                print(f"  DEPLOY FAILED: {status}")
                sys.exit(1)
    except Exception as e:
        print(f"  Error: {e}")
    time.sleep(15)

print("  TIMED OUT")
sys.exit(1)
