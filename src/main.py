import asyncio
import os
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.repository.database import Database
from src.services.ai_service import AiService
from src.core.engine import Orchestrator
from src.adapters.telegram_adapter import TelegramAdapter
from src.utils.logger import setup_logger

async def main():
    load_dotenv()
    log = setup_logger("Main")
    log.info("--- PERSONAL AI AGENT: SILENT QUEUE MODE ---")

    try:
        config = load_config()
        db = Database(config.database.path)
        await db.initialize()
        
        ai_service = AiService(config, os.getenv("GROQ_API_KEY"))
        orchestrator = Orchestrator(config, db, ai_service)
        
        telegram = TelegramAdapter(os.getenv("TELEGRAM_BOT_TOKEN"))
        
        telegram.register_handlers(orchestrator)

        log.info(f"Bot live dengan persona: {config.personas.active_persona}")
        await telegram.start_polling(orchestrator)

    except Exception as e:
        log.error(f"Error fatal: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass