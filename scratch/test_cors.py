import requests

BASE = 'https://lifodial.onrender.com'
headers = {
    'Origin': 'https://someclinic.com',
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'Content-Type',
}

# Test embed track (was returning 400 before fix)
r = requests.options(BASE + '/embed/agent-002/track', headers=headers, timeout=10)
acao = r.headers.get("Access-Control-Allow-Origin", "MISSING")
print(f"OPTIONS /embed/agent-002/track: {r.status_code} ACAO={acao}")

# Test embed config
r = requests.options(BASE + '/embed/agent-002/config', headers=headers, timeout=10)
acao = r.headers.get("Access-Control-Allow-Origin", "MISSING")
print(f"OPTIONS /embed/agent-002/config: {r.status_code} ACAO={acao}")

# Test widget.js
r = requests.options(BASE + '/widget.js', headers=headers, timeout=10)
acao = r.headers.get("Access-Control-Allow-Origin", "MISSING")
print(f"OPTIONS /widget.js: {r.status_code} ACAO={acao}")

# Test health endpoint (should NOT have * CORS)
r = requests.get(BASE + '/health', timeout=10)
print(f"GET /health: {r.status_code}")
