"""
Simulate real user agent testing flow to catch ALL possible errors/warnings.
This tests the exact endpoints hit during a voice agent test session.
"""
import sys, json, time
try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

BASE = "https://lifodial.onrender.com"

print("="*80)
print("FULL AGENT TEST SIMULATION - ALL ENDPOINTS")
print("="*80)

# ── 1. List agents (main dashboard) ──
print("\n[1] GET /agents")
r = requests.get(f"{BASE}/agents", timeout=20)
print(f"  Status: {r.status_code}")
agents = r.json() if r.ok else []
print(f"  Agents: {len(agents)}")

# ── 2. Health check per agent ──
for a in agents:
    aid = a.get("id","?")
    print(f"\n[2] GET /agents/{aid}/health")
    r = requests.get(f"{BASE}/agents/{aid}/health", timeout=15)
    print(f"  Status: {r.status_code}")
    if r.ok:
        h = r.json()
        print(f"  -> {json.dumps(h)[:200]}")
    else:
        print(f"  -> ERROR: {r.text[:200]}")

# ── 3. Agent detail fetch ──
for a in agents:
    aid = a.get("id","?")
    print(f"\n[3] GET /agents/{aid}")
    r = requests.get(f"{BASE}/agents/{aid}", timeout=15)
    print(f"  Status: {r.status_code}")
    if r.ok:
        d = r.json()
        print(f"  name={d.get('agent_name','?')} voice={d.get('tts_voice','?')} lang={d.get('tts_language','?')} tts_model={d.get('tts_model','?')}")
        print(f"  llm_provider={d.get('llm_provider','?')} llm_model={d.get('llm_model','?')}")
        print(f"  stt_provider={d.get('stt_provider','?')} stt_model={d.get('stt_model','?')}")
    else:
        print(f"  -> ERROR: {r.text[:200]}")

# ── 4. Voice library (sarvam voices) ──
print(f"\n[4] GET /platform/tts/voices/sarvam?model=bulbul%3Av3")
r = requests.get(f"{BASE}/platform/tts/voices/sarvam", params={"model": "bulbul:v3"}, timeout=15)
print(f"  Status: {r.status_code}")
if r.ok:
    voices = r.json()
    vlist = voices.get("voices", [])
    print(f"  Voices: {len(vlist)}")
    for v in vlist:
        print(f"    {v.get('id','?')} ({v.get('gender','?')}) lang={v.get('language','?')}")

# ── 5. STT voices/languages ──  
print(f"\n[5] GET /platform/stt/languages")
r = requests.get(f"{BASE}/platform/stt/languages", timeout=15)
print(f"  Status: {r.status_code}")
if r.ok:
    print(f"  -> {r.text[:300]}")
elif r.status_code == 404:
    print(f"  -> 404 (endpoint doesn't exist)")

# ── 6. Embed/preview endpoints that widget.js hits ──
for aid in [a.get("id") for a in agents[:2]]:
    print(f"\n[6] GET /embed/{aid}/preview")
    r = requests.get(f"{BASE}/embed/{aid}/preview", timeout=15)
    print(f"  Status: {r.status_code}")
    if not r.ok:
        print(f"  -> {r.text[:200]}")

# ── 7. Widget.js ──
print(f"\n[7] GET /widget.js")
r = requests.get(f"{BASE}/widget.js", timeout=15)
print(f"  Status: {r.status_code}")
if r.ok:
    print(f"  Size: {len(r.text)} bytes")
else:
    print(f"  -> {r.text[:200]}")

# ── 8. Test TTS synthesis endpoint (dry run) ──
for a in agents[:2]:
    aid = a.get("id","?")
    print(f"\n[8] POST /agents/{aid}/synthesize (dry test)")
    r = requests.post(f"{BASE}/agents/{aid}/synthesize", 
                      json={"text": "Hello, this is a test.", "language": a.get("tts_language", "en-IN")},
                      timeout=20)
    print(f"  Status: {r.status_code}")
    if r.ok:
        ct = r.headers.get("Content-Type", "?")
        print(f"  Content-Type: {ct}, Size: {len(r.content)} bytes")
    else:
        print(f"  -> {r.text[:300]}")

# ── 9. Check for CORS ──
print(f"\n[9] OPTIONS /agents (CORS preflight)")
r = requests.options(f"{BASE}/agents", headers={
    "Origin": "https://lifodial.vercel.app",
    "Access-Control-Request-Method": "GET",
}, timeout=10)
print(f"  Status: {r.status_code}")
print(f"  ACAO: {r.headers.get('Access-Control-Allow-Origin', 'MISSING')}")
print(f"  ACAM: {r.headers.get('Access-Control-Allow-Methods', 'MISSING')}")

# ── 10. Dashboard endpoints ──
print(f"\n[10] GET /api/dashboard/stats")
r = requests.get(f"{BASE}/api/dashboard/stats", timeout=10)
print(f"  Status: {r.status_code}")
if r.status_code == 404:
    print("  -> 404 (not implemented)")

print(f"\n[10b] GET /api/call_logs?limit=5")
r = requests.get(f"{BASE}/api/call_logs", params={"limit": 5}, timeout=10)
print(f"  Status: {r.status_code}")
if r.status_code == 404:
    print("  -> 404 (not implemented)")

# ── 11. Auth endpoints ──
print(f"\n[11] POST /auth/clinic-login (test)")
r = requests.post(f"{BASE}/auth/clinic-login",
                   json={"email": "test@test.com", "password": "test"},
                   timeout=10)
print(f"  Status: {r.status_code}")
if r.status_code == 404:
    print("  -> 404 (not implemented - this causes fallback in Login.tsx)")
elif r.status_code == 422:
    print(f"  -> 422 validation error")
else:
    print(f"  -> {r.text[:200]}")

# ── 12. Tenants ──
print(f"\n[12] GET /tenants")
r = requests.get(f"{BASE}/tenants", timeout=10)
print(f"  Status: {r.status_code}")
if r.ok:
    data = r.json()
    if isinstance(data, list):
        print(f"  -> {len(data)} tenants")
    else:
        print(f"  -> {json.dumps(data)[:200]}")

print("\n" + "="*80)
print("SIMULATION COMPLETE")
print("="*80)
