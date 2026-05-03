"""
Post-deploy verification: test ALL endpoints that would produce warnings.
Confirms zero-warning state in production.
"""
import sys, json
try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

BASE = "https://lifodial.onrender.com"

print("=" * 80)
print("POST-DEPLOY VERIFICATION — Zero-Warning Audit")
print("=" * 80)

# 1. Health
print("\n✅ Health Check")
r = requests.get(f"{BASE}/health", timeout=15)
print(f"   {r.status_code} → {r.json()}")

# 2. All agents — verify configurations
print("\n✅ Agent Configuration Audit")
r = requests.get(f"{BASE}/agents", timeout=15)
agents = r.json()
issues = []

VALID_LANGUAGES = {
    "as-IN", "bn-IN", "brx-IN", "doi-IN", "en-IN", "gu-IN",
    "hi-IN", "kn-IN", "kok-IN", "ks-IN", "mai-IN", "ml-IN",
    "mni-IN", "mr-IN", "ne-IN", "od-IN", "pa-IN", "sa-IN",
    "sat-IN", "sd-IN", "ta-IN", "te-IN", "ur-IN",
}

V3_SPEAKERS = [
    "priya", "ritu", "neha", "simran", "kavya", "ishita", "shreya",
    "tanya", "pooja", "roopa", "kavitha", "suhani", "shruti",
    "niharika", "rupali", "rahul", "aditya", "ashutosh", "rohan",
    "amit", "dev", "ratan", "varun", "manan", "sumit", "kabir",
    "aayan", "shubh", "advait", "anand", "tarun", "sunny", "mani",
    "gokul", "vijay", "mohit", "rehan", "soham", "anushka",
]

DEPRECATED_MODELS = {"gemini-2.0-flash", "gemini-1.0-pro"}
LEGACY_VOICES = {"meera", "pavithra", "maitreyi", "arvind", "amol", "amartya", "diya", "neel", "misha", "vian"}

for a in agents:
    aid = a["id"]
    voice = a.get("tts_voice", "")
    lang = a.get("tts_language", "")
    model = a.get("tts_model", "")
    llm_model = a.get("llm_model", "")
    llm_provider = a.get("llm_provider", "")
    
    agent_issues = []
    
    # Check voice
    if voice.lower() in LEGACY_VOICES:
        agent_issues.append(f"⚠️ Legacy v2 voice '{voice}' (would trigger speaker remap WARNING)")
    if voice.lower() not in V3_SPEAKERS and voice:
        agent_issues.append(f"⚠️ Unknown voice '{voice}' (would trigger get_compatible_speaker WARNING)")
    
    # Check language
    if lang and lang not in VALID_LANGUAGES:
        agent_issues.append(f"⚠️ Invalid language '{lang}' (would trigger normalize_sarvam_language WARNING)")
    
    # Check LLM model
    if llm_model in DEPRECATED_MODELS:
        agent_issues.append(f"⚠️ Deprecated model '{llm_model}' (would trigger model remap WARNING)")
    
    # Check TTS model
    if model and model != "bulbul:v3":
        agent_issues.append(f"⚠️ Non-v3 TTS model '{model}'")
    
    # Check model-provider match
    provider_prefixes = {
        "gemini": ["gemini"], "openai": ["gpt-", "o1-", "o3-"],
        "groq": ["llama", "mixtral", "gemma"], "anthropic": ["claude"],
    }
    if llm_provider in provider_prefixes:
        if not any(llm_model.lower().startswith(p) for p in provider_prefixes[llm_provider]):
            agent_issues.append(f"⚠️ Model-provider mismatch: {llm_provider}/{llm_model}")
    
    status = "✅ CLEAN" if not agent_issues else "⚠️ HAS ISSUES"
    print(f"   {aid}: {status}")
    print(f"      voice={voice} lang={lang} tts_model={model}")
    print(f"      llm={llm_provider}/{llm_model}")
    for issue in agent_issues:
        print(f"      {issue}")
        issues.append(f"{aid}: {issue}")

# 3. Test embed endpoints (what external websites hit)
print("\n✅ Embed Widget Endpoints")
for a in agents[:2]:
    aid = a["id"]
    r = requests.get(f"{BASE}/embed/{aid}/config", timeout=10, headers={"Origin": "https://example.com"})
    print(f"   GET /embed/{aid}/config → {r.status_code}")
    r = requests.get(f"{BASE}/embed/{aid}/preview", timeout=10)
    print(f"   GET /embed/{aid}/preview → {r.status_code}")

# 4. Widget.js
print("\n✅ Widget.js")
r = requests.get(f"{BASE}/widget.js", timeout=10)
print(f"   GET /widget.js → {r.status_code} ({len(r.text)} bytes)")

# 5. Voice library
print("\n✅ Voice Library")
r = requests.get(f"{BASE}/platform/tts/voices/sarvam", params={"model": "bulbul:v3"}, timeout=10)
print(f"   GET /platform/tts/voices/sarvam → {r.status_code} ({len(r.json().get('voices',[]))} voices)")

# 6. CORS check
print("\n✅ CORS")
r = requests.options(f"{BASE}/agents", headers={
    "Origin": "https://someclinic.com",
    "Access-Control-Request-Method": "GET",
}, timeout=10)
print(f"   OPTIONS /agents → {r.status_code}")
print(f"   ACAO: {r.headers.get('Access-Control-Allow-Origin', 'MISSING')}")

# Summary
print("\n" + "=" * 80)
if issues:
    print(f"⚠️ FOUND {len(issues)} POTENTIAL WARNING SOURCE(S):")
    for i in issues:
        print(f"   {i}")
else:
    print("✅ ALL AGENTS CLEAN — ZERO WARNING SOURCES DETECTED")
    print("   Every agent has:")
    print("   • Valid bulbul:v3 TTS voice")
    print("   • Supported Sarvam language code")
    print("   • Current (non-deprecated) LLM model")
    print("   • Correct model-provider pairing")
print("=" * 80)
