import requests, json, time, sys

HEADERS = {"Authorization": "Bearer rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK", "Accept": "application/json"}
DEPLOY_ID = "dep-d7qprsa8qa3s73d1lc1g"
SERVICE_ID = "srv-d7m7tnho3t8c73e19q30"

print(f"Monitoring deploy {DEPLOY_ID}...")
start = time.time()
last_status = ""

while time.time() - start < 600:  # 10 min max
    try:
        r = requests.get(
            f"https://api.render.com/v1/services/{SERVICE_ID}/deploys/{DEPLOY_ID}",
            headers=HEADERS, timeout=30,
        )
        if r.ok:
            data = r.json()
            status = data.get("status", "?")
            if status != last_status:
                elapsed = int(time.time() - start)
                print(f"  [{elapsed}s] Status: {status}")
                last_status = status
            
            if status == "live":
                print("  DEPLOY IS LIVE!")
                # Quick health check
                time.sleep(5)
                try:
                    hr = requests.get("https://lifodial.onrender.com/health", timeout=60)
                    print(f"  Health: {hr.status_code} -> {hr.text[:200]}")
                except Exception as e:
                    print(f"  Health check: {e}")
                sys.exit(0)
            elif status in ("build_failed", "update_failed", "canceled"):
                print(f"  DEPLOY FAILED: {status}")
                # Get logs
                try:
                    lr = requests.get(
                        f"https://api.render.com/v1/services/{SERVICE_ID}/deploys/{DEPLOY_ID}/logs",
                        headers=HEADERS, timeout=30,
                    )
                    if lr.ok:
                        for line in lr.json()[-20:]:
                            print(f"    {line.get('message', '')}")
                except:
                    pass
                sys.exit(1)
    except Exception as e:
        print(f"  Poll error: {e}")
    
    time.sleep(15)

print("  TIMED OUT after 10 minutes")
sys.exit(1)
