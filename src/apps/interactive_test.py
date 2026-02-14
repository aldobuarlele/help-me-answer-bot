import asyncio
import os
import sys
from dotenv import load_dotenv
from src.utils.config_loader import load_config
from src.repository.database import Database
from src.services.ai_service import AiService
from src.core.engine import Orchestrator
from src.utils.logger import setup_logger

async def start_interactive_session():
    load_dotenv()
    config = load_config()
    log = setup_logger("Interactive_Test")
    
    db = Database(config.database.path)
    await db.initialize()
    
    ai_key = os.getenv("GROQ_API_KEY")
    if not ai_key:
        print("ERROR: GROQ_API_KEY tidak ditemukan di .env")
        return
        
    ai_service = AiService(config, ai_key)
    engine = Orchestrator(config, db, ai_service)
    
    MY_USER_ID = 12345678 
    
    print("\n" + "="*50)
    print(f"SISTEM: Personal AI Agent (Mode: {config.personas.active_persona})")
    print(f"LOGIKA: Interval {config.bot_settings.reply_interval} detik")
    print("STATUS: Siap menerima input. Ketik 'exit' untuk keluar.")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("Anda: ")
            
            if user_input.lower() in ['exit', 'quit', 'keluar']:
                print("\nSISTEM: Sesi berakhir. Sampai jumpa!")
                break
            
            if not user_input.strip():
                continue

            response = await engine.handle_message(MY_USER_ID, user_input)
            
            print(f"\nAI: {response}\n")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\nSISTEM: Mematikan sesi...")
            break
        except Exception as e:
            print(f"\nSISTEM ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(start_interactive_session())