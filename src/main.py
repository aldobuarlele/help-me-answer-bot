import asyncio
import sys

async def run_telegram_bot():
    from src.apps.telegram_bot import TelegramBotApp
    app = TelegramBotApp()
    await app.run()

async def run_wa_test():
    from src.apps.test_wa_session import WhatsAppSessionTest
    app = WhatsAppSessionTest()
    await app.run()

async def main():
    await run_wa_test()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSistem dimatikan.")
        sys.exit(0)