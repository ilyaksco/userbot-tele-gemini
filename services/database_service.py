import inspect
from core.supabase_client import get_supabase_client
from config import settings 

AI_TARGETS_TABLE_NAME = "ai_targets"
CONVERSATION_HISTORY_TABLE_NAME = "conversation_history"

async def activate_ai_for_chat(chat_id: int) -> bool:
    supabase = await get_supabase_client()
    try:
        response = await supabase.table(AI_TARGETS_TABLE_NAME)\
            .upsert({"chat_id": chat_id, "is_active": True})\
            .execute()
        if response and hasattr(response, 'data') and response.data:
            return True
        else:
            print(f"DB activate_ai_for_chat: Kemungkinan gagal, tidak ada data dikembalikan untuk chat_id {chat_id}. Response: {response}")
            return False
    except Exception as e:
        print(f"DB Error saat mengaktifkan AI untuk chat {chat_id}: {e}")
        return False

async def deactivate_ai_for_chat(chat_id: int) -> bool:
    supabase = await get_supabase_client()
    try:
        await supabase.table(AI_TARGETS_TABLE_NAME)\
            .update({"is_active": False})\
            .eq("chat_id", chat_id)\
            .execute()
        return True 
    except Exception as e:
        print(f"DB Error saat menonaktifkan AI untuk chat {chat_id}: {e}")
        return False

async def is_ai_active_for_chat(chat_id: int) -> bool:
    supabase = await get_supabase_client()
    try:
        response = await supabase.table(AI_TARGETS_TABLE_NAME)\
            .select("is_active")\
            .eq("chat_id", chat_id)\
            .limit(1)\
            .single()\
            .execute()
        if response and hasattr(response, 'data') and response.data and response.data.get("is_active"):
            return True
        return False
    except Exception as e:
        return False

async def add_message_to_history(chat_id: int, role: str, content: str) -> bool:
    if not content or not content.strip(): # Jangan simpan pesan kosong
        return False
    supabase = await get_supabase_client()
    try:
        await supabase.table(CONVERSATION_HISTORY_TABLE_NAME)\
            .insert({"chat_id": chat_id, "role": role, "content": content})\
            .execute()
        return True
    except Exception as e:
        print(f"DB Error saat menambahkan pesan ke histori untuk chat {chat_id}: {e}")
        return False

async def get_conversation_history(chat_id: int) -> list:
    supabase = await get_supabase_client()
    try:
        response = await supabase.table(CONVERSATION_HISTORY_TABLE_NAME)\
            .select("role, content")\
            .eq("chat_id", chat_id)\
            .order("timestamp", desc=True)\
            .limit(settings.CONVERSATION_HISTORY_LIMIT)\
            .execute()
        if response.data:
            # Urutan dari Supabase adalah terbaru dulu, kita butuh terlama dulu untuk Gemini
            return list(reversed(response.data)) 
        return []
    except Exception as e:
        print(f"DB Error saat mengambil histori percakapan untuk chat {chat_id}: {e}")
        return []

async def clear_conversation_history(chat_id: int) -> bool:
    supabase = await get_supabase_client()
    try:
        print(f"DB_SERVICE (clear_history): Mencoba menghapus histori untuk chat_id: {chat_id}")
        response = await supabase.table(CONVERSATION_HISTORY_TABLE_NAME)\
            .delete()\
            .eq("chat_id", chat_id)\
            .execute()

        # Log detail respons (data yang dihapus biasanya ada di response.data jika return=representation)
        deleted_data = getattr(response, 'data', [])
        deleted_count = len(deleted_data) if isinstance(deleted_data, list) else 'N/A (cek preferensi count)'

        print(f"DB_SERVICE (clear_history): Operasi delete untuk chat_id: {chat_id} dieksekusi. Jumlah data yg dikembalikan (mungkin yg dihapus): {deleted_count}. Respons: {response}")
        return True
    except Exception as e:
        print(f"DB_SERVICE (clear_history): Error saat menghapus histori untuk chat {chat_id}: {e}")
        import traceback
        traceback.print_exc()
        return False
