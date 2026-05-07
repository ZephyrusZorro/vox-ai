import time, requests

API_KEY = 'rnd_uOZChdOwSBBfyNjBK5oHk6NTqGIK'
SERVICE_ID = 'srv-d7m7tnho3t8c73e19q30'
BASE = 'https://api.render.com/v1'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}

print('Monitoring deploy...')
for i in range(40):
    r = requests.get(f'{BASE}/services/{SERVICE_ID}/deploys', headers=HEADERS, params={'limit': 1})
    if r.ok:
        d = r.json()[0]
        status = d.get('status', '?')
        print(f'  [{i*10}s] {status}')
        if status == 'live':
            print('Deploy is LIVE!')
            break
        if status in ('build_failed', 'update_failed', 'canceled'):
            print(f'Deploy FAILED: {status}')
            break
    time.sleep(10)
else:
    print('Timeout waiting for deploy')

# Quick verification after deploy
if status == 'live':
    print('\nVerifying...')
    r = requests.get('https://lifodial.onrender.com/health', timeout=10)
    print(f'  Health: {r.status_code}')
    
    # Check embed config includes first_message_mode
    r = requests.get('https://lifodial.onrender.com/embed/agent-002/config', timeout=10)
    if r.ok:
        cfg = r.json()
        print(f'  first_message_mode: {cfg.get("first_message_mode", "MISSING")}')
        print(f'  first_message present: {"first_message" in cfg}')
        print(f'  agent_name: {cfg.get("agent_name", "MISSING")}')
    else:
        print(f'  Config: {r.status_code}')
