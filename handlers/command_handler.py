from telethon import events
from services import database_service

async def register_command_handlers(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"^\.AiOn(?: (\d+))?$"))
    async def handle_ai_on(event):
        chat_id_arg = event.pattern_match.group(1)
        target_chat_id = None

        if chat_id_arg:
            try:
                target_chat_id = int(chat_id_arg)
            except ValueError:
                await event.edit("ID User/Grup tidak valid.")
                return
        else:
            target_chat_id = event.chat_id

        if not target_chat_id: 
            await event.edit("Tidak bisa mendapatkan ID chat. Coba `.AiOn <id_chat>`.")
            return

        success = await database_service.activate_ai_for_chat(target_chat_id)
        if success:
            await event.edit(f"🤖 Gemini AI Diaktifkan untuk chat ID: `{target_chat_id}`")
        else:
            await event.edit(f"Gagal mengaktifkan AI untuk chat ID: `{target_chat_id}`. Cek log.")

    @client.on(events.NewMessage(outgoing=True, pattern=r"^\.AiOff(?: (\d+))?$"))
    async def handle_ai_off(event):
        chat_id_arg = event.pattern_match.group(1)
        target_chat_id = None

        if chat_id_arg:
            try:
                target_chat_id = int(chat_id_arg)
            except ValueError:
                await event.edit("ID User/Grup tidak valid.")
                return
        else:
            target_chat_id = event.chat_id

        if not target_chat_id:
            await event.edit("Tidak bisa mendapatkan ID chat. Coba `.AiOff <id_chat>`.")
            return

        success = await database_service.deactivate_ai_for_chat(target_chat_id)
        if success:
            await event.edit(f"🤖 Gemini AI Dinonaktifkan untuk chat ID: `{target_chat_id}`")
        else:
            await event.edit(f"Gagal menonaktifkan AI untuk chat ID: `{target_chat_id}`. Cek log.")

   
