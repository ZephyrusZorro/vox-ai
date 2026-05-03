import requests, json

API_KEY = 'rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK'
SERVICE_ID = 'srv-d7m7tnho3t8c73e19q30'
BASE = 'https://api.render.com/v1'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}

# Get latest deploy
r = requests.get(f'{BASE}/services/{SERVICE_ID}/deploys', headers=HEADERS, params={'limit': 1})
deploy_data = r.json()[0]
deploy_id = deploy_data.get('id', '?')
status = deploy_data.get('status', '?')
print(f"Deploy ID: {deploy_id}")
print(f"Status: {status}")

# Revert build command — remove apt-get (Render Python runtime doesn't support it directly)
payload = {
    'serviceDetails': {
        'envSpecificDetails': {
            'buildCommand': 'pip install -r requirements.txt',
            'startCommand': 'uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 2',
        }
    }
}

r2 = requests.patch(f'{BASE}/services/{SERVICE_ID}', headers=HEADERS, json={**payload, 'Content-Type': 'application/json'})
HEADERS2 = {**HEADERS, 'Content-Type': 'application/json'}
r2 = requests.patch(f'{BASE}/services/{SERVICE_ID}', headers=HEADERS2, json=payload)
print(f"Reverted build command: {r2.status_code}")
if r2.ok:
    print("Build command reverted to: pip install -r requirements.txt")
