import asyncio
import time
import random
import os
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.utils.config_loader import load_config
from src.repository.database import Database
from src.services.ai_service import AiService
from src.core.engine import Orchestrator
from src.adapters.whatsapp.driver import WhatsAppDriver
from src.adapters.whatsapp.listener import WhatsAppListener
from src.adapters.whatsapp.executor import WhatsAppExecutor
from src.utils.logger import setup_logger

class WhatsAppBotApp:
    def __init__(self):
        self.log = setup_logger("WA_App")
        load_dotenv()
        self.config = load_config()

    async def run(self):
        self.log.info("--- MEMULAI WHATSAPP BOT AUTO-PILOT ---")
        
        db = Database(self.config.database.path)
        await db.initialize()
        
        ai_service = AiService(self.config, os.getenv("GROQ_API_KEY"))
        orchestrator = Orchestrator(self.config, db, ai_service)

        wa_driver = WhatsAppDriver()
        driver = wa_driver.start()
        
        self.log.info("Menunggu 15 detik untuk loading WhatsApp Web...")
        await asyncio.sleep(15)

        listener = WhatsAppListener(driver, self.config)
        executor = WhatsAppExecutor(driver)

        self.log.info(f"Bot Siap! Whitelist: {self.config.whatsapp.whitelist}")
        self.log.info("Menunggu pesan masuk...")

        try:
            while True:
                vip_contacts = listener.scan_unread_messages()
                
                if vip_contacts:
                    self.log.info(f"🎯 Target ditemukan: {vip_contacts}")
                    
                    for contact in vip_contacts:
                        await self.process_contact(contact, executor, orchestrator)
                        
                        await asyncio.sleep(random.uniform(2, 5))
                else:
                    await asyncio.sleep(self.config.whatsapp.scan_interval)

        except KeyboardInterrupt:
            self.log.info("Bot dihentikan manual.")
        except Exception as e:
            self.log.error(f"Critical Error: {e}")
        finally:
            wa_driver.close()

    async def process_contact(self, contact_name, executor, orchestrator):
        try:
            if not executor.open_chat(contact_name):
                return

            last_message = executor.get_last_message()
            self.log.info(f"📩 Pesan dari {contact_name}: {last_message}")
            
            if not last_message or last_message == "[Non-Text Message]":
                self.log.warning("Pesan tidak terbaca/kosong. Skip.")
                executor.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                return

            user_id = abs(hash(contact_name)) % 100000000 

            status, response = await orchestrator.handle_message(user_id, last_message)

            if status is True:
                self.log.info(f"🤖 AI Menjawab: {response[:30]}...")
                executor.send_message(response)
                
                time.sleep(1)
                executor.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

            elif isinstance(status, bool) and status is False:
                if isinstance(response, int):
                    self.log.info(f"⏳ Cooldown aktif untuk {contact_name}. Tunggu {response} detik.")
                    
                    if response < 15: 
                        self.log.info("Cooldown sebentar, menunggu di dalam chat...")
                        await asyncio.sleep(response + 1)
                        status_retry, response_retry = await orchestrator.handle_message(user_id, last_message)
                        if status_retry is True:
                             self.log.info(f"🤖 AI Menjawab (Setelah Nunggu): {response_retry[:30]}...")
                             executor.send_message(response_retry)
                    
                    else:
                        self.log.info("Cooldown lama. Menandai pesan sebagai 'Read' dan menutup chat.")
                        time.sleep(2) 
                else:
                    self.log.info(f"⛔ Ditolak Gatekeeper: {response}")

                executor.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

        except Exception as e:
            self.log.error(f"Gagal memproses {contact_name}: {e}")
            try:
                executor.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            except:
                pass