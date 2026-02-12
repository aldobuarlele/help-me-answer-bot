import asyncio
import os
from src.utils.logger import setup_logger
from src.utils.config_loader import load_config
from src.repository.database import Database

async def run_test():
    log = setup_logger("Phase1_Test")
    log.info("--- STARTING PHASE 1 TESTING ---")

    try:
        config = load_config()
        log.info(f"SUCCESS: Config loaded for project: {config.app.name}")
    except Exception as e:
        log.error(f"FAILED: Config loader error: {e}")
        return

    try:
        db = Database(config.database.path)
        await db.initialize()
        if os.path.exists(config.database.path):
            log.info(f"SUCCESS: Database file created at {config.database.path}")
        else:
            log.error("FAILED: Database file not found")
    except Exception as e:
        log.error(f"FAILED: Database error: {e}")
        return

    try:
        from datetime import datetime
        test_user_id = 12345
        await db.update_user_stats(test_user_id, 1, datetime.now())
        stats = await db.get_user_stats(test_user_id)
        if stats and stats['user_id'] == test_user_id:
            log.info(f"SUCCESS: Data persistence verified for user {test_user_id}")
        else:
            log.error("FAILED: Could not retrieve data from database")
    except Exception as e:
        log.error(f"FAILED: Data persistence error: {e}")
        return

    log.info("--- PHASE 1 TESTING COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    asyncio.run(run_test())