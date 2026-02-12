import asyncio
import os
import sys
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.repository.database import Database
from src.services.ai_service import AiService
from src.core.engine import Orchestrator
from src.adapters.telegram_adapter import TelegramAdapter
from src.utils.logger import setup_logger

async def terminal_input_loop(orchestrator: Orchestrator):
    """Loop untuk menerima input langsung dari terminal Mac Anda."""
    loop = asyncio.get_event_loop()
    MY_CLI_ID = 1
    
    print("\n[CLI] Terminal Interaction Active. Type your message below:")
    while True:
        user_input = await loop.run_in_executor(None, sys.stdin.readline)
        user_input = user_input.strip()
        
        if user_input.lower() in ['exit', 'quit']:
            break
            
        if user_input:
            response = await orchestrator.handle_message(MY_CLI_ID, user_input)
            print(f"\n[AI Response to CLI]: {response}\n")

async def main():
    load_dotenv()
    log = setup_logger("Main_Entry")
    log.info("--- STARTING DUAL-INPUT AI AGENT ---")

    config = load_config()
    db = Database(config.database.path)
    await db.initialize()

    ai_service = AiService(config, os.getenv("GROQ_API_KEY"))
    orchestrator = Orchestrator(config, db, ai_service)

    telegram = TelegramAdapter(os.getenv("TELEGRAM_BOT_TOKEN"))
    telegram.register_handlers(orchestrator.handle_message)

    log.info("System is live! You can chat via Telegram or Terminal.")
    
    await asyncio.gather(
        telegram.start_polling(),
        terminal_input_loop(orchestrator)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSystem shut down by user.")