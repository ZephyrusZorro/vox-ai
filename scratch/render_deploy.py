"""
Render API Deploy Script — diagnose & trigger deploy.
"""
import json
import sys
import time

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

API_KEY = "rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK"
SERVICE_ID = "srv-d7m7tnho3t8c73e19q30"
BASE = "https://api.render.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_service():
    """Get service info."""
    r = requests.get(f"{BASE}/services/{SERVICE_ID}", headers=HEADERS, timeout=30)
    print(f"[GET service] Status: {r.status_code}")
    if r.ok:
        data = r.json()
        print(json.dumps(data, indent=2, default=str)[:2000])
        return data
    else:
        print(f"Error: {r.text[:500]}")
        return None


def get_deploys(limit=5):
    """Get recent deploys."""
    r = requests.get(
        f"{BASE}/services/{SERVICE_ID}/deploys?limit={limit}",
        headers=HEADERS, timeout=30,
    )
    print(f"\n[GET deploys] Status: {r.status_code}")
    if r.ok:
        deploys = r.json()
        for d in deploys:
            deploy = d.get("deploy", d)
            print(f"  - {deploy.get('id', '?')}: status={deploy.get('status', '?')}, "
                  f"commit={deploy.get('commit', {}).get('message', '?')[:60]}, "
                  f"created={deploy.get('createdAt', '?')[:19]}")
        return deploys
    else:
        print(f"Error: {r.text[:500]}")
        return []


def get_env_vars():
    """Get environment variables (names only, not secrets)."""
    r = requests.get(
        f"{BASE}/services/{SERVICE_ID}/env-vars",
        headers=HEADERS, timeout=30,
    )
    print(f"\n[GET env-vars] Status: {r.status_code}")
    if r.ok:
        env_vars = r.json()
        for ev in env_vars:
            ev_data = ev.get("envVar", ev)
            key = ev_data.get("key", "?")
            val = ev_data.get("value", "***")
            # Don't print secret values, just show key + first few chars
            if key in ("DATABASE_URL", "CORS_ORIGIN", "ENVIRONMENT", "PORT", "FORCE_REDEPLOY_ID"):
                print(f"  {key} = {val[:80]}...")
            else:
                print(f"  {key} = {'(set)' if val and val != '***' else '(empty)'}")
        return env_vars
    else:
        print(f"Error: {r.text[:500]}")
        return []


def trigger_deploy():
    """Trigger a manual deploy with clear cache."""
    r = requests.post(
        f"{BASE}/services/{SERVICE_ID}/deploys",
        headers=HEADERS,
        json={"clearCache": "clear"},
        timeout=30,
    )
    print(f"\n[POST deploy] Status: {r.status_code}")
    if r.ok:
        data = r.json()
        deploy_id = data.get("id", "?")
        print(f"  Deploy triggered! ID: {deploy_id}")
        print(json.dumps(data, indent=2, default=str)[:1000])
        return deploy_id
    else:
        print(f"Error: {r.text[:500]}")
        return None


def check_deploy_status(deploy_id, max_wait=600):
    """Poll deploy status until it completes."""
    print(f"\n[Monitoring deploy {deploy_id}]")
    start = time.time()
    last_status = ""
    while time.time() - start < max_wait:
        r = requests.get(
            f"{BASE}/services/{SERVICE_ID}/deploys/{deploy_id}",
            headers=HEADERS, timeout=30,
        )
        if r.ok:
            data = r.json()
            status = data.get("status", "?")
            if status != last_status:
                elapsed = int(time.time() - start)
                print(f"  [{elapsed}s] Deploy status: {status}")
                last_status = status
            if status in ("live", "deactivated"):
                print(f"  ✅ Deploy is LIVE!")
                return True
            elif status in ("build_failed", "update_failed", "canceled"):
                print(f"  ❌ Deploy FAILED: {status}")
                return False
        time.sleep(10)
    print(f"  ⏰ Timed out after {max_wait}s")
    return False


if __name__ == "__main__":
    print("=" * 60)
    print("RENDER DEPLOY AUDIT & FIX")
    print("=" * 60)

    # Step 1: Service info
    print("\n── 1. Service Info ──")
    svc = get_service()

    # Step 2: Recent deploys
    print("\n── 2. Recent Deploys ──")
    deploys = get_deploys()

    # Step 3: Environment variables
    print("\n── 3. Environment Variables ──")
    env = get_env_vars()

    # Step 4: Trigger new deploy
    print("\n── 4. Triggering New Deploy ──")
    deploy_id = trigger_deploy()

    if deploy_id:
        # Step 5: Monitor
        print("\n── 5. Monitoring Deploy ──")
        success = check_deploy_status(deploy_id)
        if success:
            print("\n🎉 DEPLOY SUCCESSFUL — checking health...")
            time.sleep(5)
            try:
                r = requests.get("https://lifodial.onrender.com/health", timeout=60)
                print(f"Health: {r.status_code} → {r.text[:200]}")
            except Exception as e:
                print(f"Health check error (cold start?): {e}")
        else:
            print("\n❌ DEPLOY FAILED — check logs above")
    else:
        print("Could not trigger deploy")
