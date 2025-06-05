from supabase import create_async_client 
from config import settings

_async_supabase_client = None

async def get_supabase_client():
    global _async_supabase_client
    if _async_supabase_client is None:
        print("Membuat instance klien Supabase Async baru...")
        _async_supabase_client = await create_async_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        print(f"Instance Klien Supabase Async dibuat: {type(_async_supabase_client)}")
    return _async_supabase_client
