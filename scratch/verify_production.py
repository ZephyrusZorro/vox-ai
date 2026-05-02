import requests, json

BASE = "https://lifodial.onrender.com"

print("=" * 60)
print("PRODUCTION VERIFICATION")
print("=" * 60)

# 1. Health
print("\n1. Health Check")
r = requests.get(f"{BASE}/health", timeout=60)
print(f"   {r.status_code}: {r.text[:200]}")

# 2. Audit
print("\n2. Database Audit")
r = requests.get(f"{BASE}/debug/audit", timeout=60)
data = r.json()
for table, info in data.items():
    count = info.get("count", info.get("error", "?"))
    print(f"   {table}: {count}")

# 3. Clinics
print("\n3. Admin Clinics")
r = requests.get(f"{BASE}/admin/clinics", timeout=60)
print(f"   {r.status_code}: {r.text[:300]}")

# 4. Agents
print("\n4. Agents")
r = requests.get(f"{BASE}/agents", timeout=60)
agents = r.json()
print(f"   {r.status_code}: {len(agents)} agents")
for a in agents[:3]:
    name = a.get("agent_name", "?")
    tid = a.get("tenant_id", "?")
    print(f"     - {name} (tenant: {tid})")

# 5. Credits
print("\n5. Credits")
r = requests.get(f"{BASE}/credits", timeout=60)
print(f"   {r.status_code}: {r.text[:300]}")

# 6. Clinic login test
print("\n6. Clinic Login Test")
r = requests.post(f"{BASE}/auth/clinic-login", json={"email": "admin@apollo.lifodial.com", "password": "test"}, timeout=60)
print(f"   {r.status_code}: {r.text[:200]}")

# 7. Docs endpoint
print("\n7. Docs")
r = requests.get(f"{BASE}/docs", timeout=60)
print(f"   {r.status_code}: {'Available' if r.status_code == 200 else 'Not available'}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
