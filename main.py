import asyncio
from config import settings
from core.telegram_client import get_telegram_client
from handlers import command_handler, message_handler

async def main():
    client = get_telegram_client()

    print("Userbot sedang mencoba login...")
    await client.start(phone=settings.PHONE_NUMBER)

    me = await client.get_me()
    if me:
        print(f"Userbot berhasil login sebagai: {me.first_name} (ID: {me.id})")
    else:
        print("Gagal login atau mendapatkan informasi user. Periksa kredensial atau koneksi.")
        return

    await command_handler.register_command_handlers(client)
    await message_handler.register_message_handlers(client)

    print("Userbot sekarang berjalan dan mendengarkan pesan...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Userbot dihentikan.")
    except Exception as e:
        print(f"Terjadi error tidak terduga: {e}")
