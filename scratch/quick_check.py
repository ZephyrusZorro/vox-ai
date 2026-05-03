import requests
r = requests.get('https://lifodial.onrender.com/agents', timeout=15)
agents = r.json()
print(f'Total agents: {len(agents)}')
for a in agents:
    aid = a.get("id","?")
    name = a.get("agent_name","?")
    voice = a.get("tts_voice","?")
    lang = a.get("tts_language","?")
    llm_p = a.get("llm_provider","?")
    llm_m = a.get("llm_model","?")
    print(f'  {aid}: name={name} voice={voice} lang={lang} llm={llm_p}/{llm_m}')
