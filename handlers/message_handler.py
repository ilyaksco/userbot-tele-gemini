from telethon import events
from services import database_service, gemini_service
from core.telegram_client import get_telegram_client
from utils.markdown_helper import ensure_valid_markdown 
import re

async def register_message_handlers(client):
    @client.on(events.NewMessage())
    async def handle_new_message(event):
        me = await client.get_me() 

        if event.sender_id == me.id:
            message_text_for_command = event.message.message if event.message else ""
            is_newchat_command_for_self = False
            target_chat_id_from_arg_for_self = None

            match_newchat_simple_for_self = re.match(r"^\s*\.newchat\s*$", message_text_for_command, re.IGNORECASE)
            match_newchat_with_arg_for_self = re.match(r"^\s*\.newchat\s+(\d+)\s*$", message_text_for_command, re.IGNORECASE)

            if match_newchat_simple_for_self:
                is_newchat_command_for_self = True
            elif match_newchat_with_arg_for_self:
                is_newchat_command_for_self = True
                target_chat_id_from_arg_for_self = int(match_newchat_with_arg_for_self.group(1))

            if is_newchat_command_for_self:
                print(f"MESSAGE_HANDLER: Menangani .newchat dari SENDER_ID_SAMA_DENGAN_ME_ID ({me.id}) - Teks: '{message_text_for_command}'")
                chat_to_clear = target_chat_id_from_arg_for_self if target_chat_id_from_arg_for_self else event.chat_id
                if not chat_to_clear:
                    response_msg = "Tidak bisa mendapatkan ID chat untuk .newchat."
                    if hasattr(event, 'respond'): await event.respond(response_msg)
                    else: await client.send_message(event.chat_id, response_msg)
                    return 

                success = await database_service.clear_conversation_history(chat_to_clear)
                response_message = f"🤖 Histori percakapan untuk chat ID `{chat_to_clear}` telah dibersihkan." if success else f"Gagal membersihkan histori untuk chat ID `{chat_to_clear}`."
                if hasattr(event, 'respond'): await event.respond(response_message)
                else: await client.send_message(event.chat_id, response_message)
                if success:
                    try: await event.delete() 
                    except Exception: pass
                return 

        if event.out or event.sender_id == me.id:
            return

        chat_id = event.chat_id
        ai_is_active = await database_service.is_ai_active_for_chat(chat_id)
        if not ai_is_active:
            return

        if event.is_group:
            should_respond_in_group = False
            if event.reply_to_msg_id:
                try:
                    replied_msg = await event.get_reply_message()
                    if replied_msg and replied_msg.sender_id == me.id:
                        print(f"GROUP_MSG_HANDLER: Pesan di grup ({chat_id}) adalah reply ke userbot. Akan diproses.")
                        should_respond_in_group = True
                    else:
                
                        return 
                except Exception as e:
                    return 
            else:
                return 
            if not should_respond_in_group:
                return

        if event.message and event.message.message:
            user_prompt = event.message.message.strip()
            if not user_prompt:
                return

            print(f"MESSAGE_HANDLER (REGULAR): Menerima pesan valid di chat ({chat_id}) dari sender {event.sender_id}: \"{user_prompt}\"")
            await database_service.add_message_to_history(chat_id, "user", user_prompt)

            async with client.action(chat_id, 'typing'):
                response_text = await gemini_service.get_gemini_response(chat_id, user_prompt) 

            if response_text:
                sanitized_response_text = ensure_valid_markdown(response_text)
                try:
                    await event.reply(sanitized_response_text, parse_mode='md')
                except Exception as e_markdown:
                    print(f"MARKDOWN_ERROR: Gagal mengirim dengan parse_mode='md': {e_markdown}. Mengirim sebagai teks biasa.")
                    await event.reply(response_text) 
