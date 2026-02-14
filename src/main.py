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

async def run_wa_listener_test():
    from src.apps.test_wa_listener import WhatsAppListenerTest
    app = WhatsAppListenerTest()
    await app.run()

async def run_wa_executor_test():
    from src.apps.test_wa_executor import WhatsAppExecutorTest
    app = WhatsAppExecutorTest()
    await app.run()

async def run_whatsapp_bot():
    from src.apps.whatsapp_bot import WhatsAppBotApp
    app = WhatsAppBotApp()
    await app.run()

async def main():
    await run_whatsapp_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSistem dimatikan.")
        sys.exit(0)