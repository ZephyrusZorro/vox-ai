"""Test all Supabase pooler regions to find the correct one."""
import socket
import sys

PROJECT_REF = "citniicxkmazxuosauxy"
PASSWORD = "g6JDhZ5S347PaAhx"

# All known Supabase AWS pooler regions
REGIONS = [
    "ap-southeast-1",  # Singapore
    "us-east-1",       # Virginia
    "us-west-1",       # California  
    "eu-west-1",       # Ireland
    "eu-central-1",    # Frankfurt
    "ap-northeast-1",  # Tokyo
    "ap-south-1",      # Mumbai
    "sa-east-1",       # Sao Paulo
    "ca-central-1",    # Canada
    "ap-southeast-2",  # Sydney
    "us-east-2",       # Ohio
    "us-west-2",       # Oregon
    "eu-west-2",       # London
    "eu-west-3",       # Paris
    "eu-north-1",      # Stockholm
    "ap-northeast-2",  # Seoul
]

try:
    import asyncpg
    import asyncio
    HAS_ASYNCPG = True
except ImportError:
    HAS_ASYNCPG = False

def test_dns(region):
    """Test if pooler hostname resolves."""
    host = f"aws-0-{region}.pooler.supabase.com"
    try:
        result = socket.getaddrinfo(host, 6543, socket.AF_INET)
        return result[0][4][0]
    except:
        return None

async def test_connection(region):
    """Actually try to connect to the pooler."""
    host = f"aws-0-{region}.pooler.supabase.com"
    user = f"postgres.{PROJECT_REF}"
    try:
        conn = await asyncio.wait_for(
            asyncpg.connect(
                host=host,
                port=6543,
                user=user,
                password=PASSWORD,
                database="postgres",
                ssl="require",
                statement_cache_size=0,
            ),
            timeout=10,
        )
        version = await conn.fetchval("SELECT version()")
        await conn.close()
        return f"OK - {version[:50]}"
    except Exception as e:
        return f"FAIL - {str(e)[:80]}"

print("Testing Supabase pooler regions...")
print("=" * 70)

# Phase 1: DNS resolution
print("\nPhase 1: DNS Resolution")
reachable = []
for region in REGIONS:
    ip = test_dns(region)
    if ip:
        print(f"  {region:25s} -> {ip}")
        reachable.append(region)
    else:
        print(f"  {region:25s} -> DNS FAIL")

# Phase 2: Try actual connections
if HAS_ASYNCPG and reachable:
    print(f"\nPhase 2: Connection Test (asyncpg)")
    
    async def test_all():
        for region in reachable:
            result = await test_connection(region)
            status = "CONNECTED" if result.startswith("OK") else "FAILED"
            print(f"  {region:25s} -> {status}: {result}")
            if result.startswith("OK"):
                url = f"postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-{region}.pooler.supabase.com:6543/postgres"
                print(f"\n  >>> CORRECT URL: {url}")
                return region
        return None
    
    winner = asyncio.run(test_all())
    if winner:
        print(f"\n  WINNER: {winner}")
    else:
        print("\n  No region worked. Trying direct connection...")
        # Try direct connection as fallback
        async def test_direct():
            try:
                conn = await asyncio.wait_for(
                    asyncpg.connect(
                        host=f"db.{PROJECT_REF}.supabase.co",
                        port=5432,
                        user="postgres",
                        password=PASSWORD,
                        database="postgres",
                        ssl="require",
                        statement_cache_size=0,
                    ),
                    timeout=15,
                )
                v = await conn.fetchval("SELECT version()")
                await conn.close()
                print(f"  Direct connection works! {v[:50]}")
                url = f"postgresql://postgres:{PASSWORD}@db.{PROJECT_REF}.supabase.co:5432/postgres"
                print(f"  >>> CORRECT URL: {url}")
            except Exception as e:
                print(f"  Direct connection also failed: {e}")
        
        asyncio.run(test_direct())
else:
    print("\nPhase 2: Skipped (asyncpg not available, DNS results above)")
    if reachable:
        print(f"\nReachable regions: {reachable}")
        print("Try these URLs:")
        for region in reachable[:3]:
            url = f"postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-{region}.pooler.supabase.com:6543/postgres"
            print(f"  {url}")
