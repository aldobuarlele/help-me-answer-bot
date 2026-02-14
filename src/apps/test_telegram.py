import asyncio
import os
from dotenv import load_dotenv
from src.adapters.telegram_adapter import TelegramAdapter

async def test_connection():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("ERROR: Token Telegram tidak ditemukan di .env")
        return

    adapter = TelegramAdapter(token)

    async def dummy_orchestrator(user_id, text):
        return f"Bot mendeteksi pesan: '{text}' dari User ID: {user_id}"

    adapter.register_handlers(dummy_orchestrator)

    print("SISTEM: Bot sedang berjalan. Silakan chat bot Anda di Telegram!")
    await adapter.start_polling()

if __name__ == "__main__":
    asyncio.run(test_connection())