import asyncio
import os
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger
from src.services.ai_service import AiService

async def run_brain_test():
    load_dotenv()
    log = setup_logger("Phase2_Final")
    log.info("--- STARTING PHASE 2 INTEGRATION TEST (GROQ) ---")

    try:
        config = load_config()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            log.error("GROQ_API_KEY is missing in .env")
            return
    except Exception as e:
        log.error(f"Config error: {e}")
        return

    service = AiService(config, api_key)

    try:
        log.info(f"Testing with Model: {config.ai_settings.model_name}")
        response = await service.get_response("Say: Brain Integration Success.")
        log.info(f"AI Response: {response.strip()}")
        
        log.info("Testing with Persona...")
        persona = config.personas.definitions.get("engineer")
        persona_resp = await service.get_response("Who are you?", system_instruction=persona)
        log.info(f"Persona Response: {persona_resp.strip()}")
        
        log.info("--- PHASE 2 TEST COMPLETED SUCCESSFULLY ---")
    except Exception as e:
        log.error(f"Integration test failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_brain_test())