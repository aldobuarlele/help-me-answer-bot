import asyncio
import sys

# Template 1: Telegram Chatbot App
async def run_chatbot():
    from src.apps.telegram_bot import TelegramBotApp
    app = TelegramBotApp()
    await app.run()

async def main():
    await run_chatbot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSistem dimatikan.")
        sys.exit(0)