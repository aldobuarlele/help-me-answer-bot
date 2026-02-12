import asyncio
import os
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.repository.database import Database
from src.services.ai_service import AiService
from src.core.engine import Orchestrator
from src.utils.logger import setup_logger

async def test_logic():
    load_dotenv()
    log = setup_logger("Test_Gatekeeper")
    log.info("--- STARTING PHASE 3: GATEKEEPER TEST ---")

    config = load_config()
    db = Database(config.database.path)
    await db.initialize()
    ai = AiService(config, os.getenv("GROQ_API_KEY"))
    
    engine = Orchestrator(config, db, ai)
    test_user = 99999

    log.info("Sending Message 1...")
    resp1 = await engine.handle_message(test_user, "Hi, siapa namamu?")
    log.info(f"Response 1 Status: {'SUCCESS' if 'Maaf' not in resp1 else 'FAILED'}")

    log.info("Sending Message 2 (Immediate)...")
    resp2 = await engine.handle_message(test_user, "Apa kabar?")
    log.info(f"Response 2 Result: {resp2}")
    
    if "tunggu" in resp2:
        log.info("SUCCESS: Cooldown logic is working.")
    else:
        log.error("FAILED: Cooldown logic bypassed!")

    log.info("--- PHASE 3 TESTING COMPLETED ---")

if __name__ == "__main__":
    asyncio.run(test_logic())