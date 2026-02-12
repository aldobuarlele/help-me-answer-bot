import os
from dotenv import load_dotenv
from src.utils.logger import setup_logger

def bootstrap():
    load_dotenv()
    logger = setup_logger("Main")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in .env file")
        return

    logger.info("Environment variables loaded successfully")

if __name__ == "__main__":
    bootstrap()