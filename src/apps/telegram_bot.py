import os
import asyncio
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.repository.database import Database
from src.services.ai_service import AiService
from src.core.engine import Orchestrator
from src.adapters.telegram_adapter import TelegramAdapter
from src.utils.logger import setup_logger

class TelegramBotApp:
    def __init__(self):
        load_dotenv()
        self.log = setup_logger("Telegram_App")
        self.config = load_config()

    async def run(self):
        self.log.info("--- STARTING DEDICATED TELEGRAM BOT ---")
        try:
            # Inisialisasi Database
            db = Database(self.config.database.path)
            await db.initialize()
            
            # Inisialisasi AI Service (Groq)
            ai_service = AiService(self.config, os.getenv("GROQ_API_KEY"))
            
            # Inisialisasi Orchestrator (Gatekeeper + Logic)
            orchestrator = Orchestrator(self.config, db, ai_service)
            
            # Inisialisasi Telegram Adapter
            telegram = TelegramAdapter(os.getenv("TELEGRAM_BOT_TOKEN"))
            telegram.register_handlers(orchestrator)

            self.log.info(f"Bot is online. Persona: {self.config.personas.active_persona}")
            await telegram.start_polling(orchestrator)
            
        except Exception as e:
            self.log.error(f"App Execution Error: {e}")