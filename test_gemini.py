import httpx, asyncio

async def test():
    key = "AIzaSyBn3JBe4rZ9-6CNSuGhiZWyCDuVEBUOBeA"
    
    models = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    async with httpx.AsyncClient() as client:
        for m in models:
            res = await client.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent', 
                params={'key': key}, 
                json={'contents': [{'role': 'user', 'parts': [{'text': 'test'}]}]}
            )
            print(f"{m} -> {res.status_code}: {res.text}")

asyncio.run(test())
