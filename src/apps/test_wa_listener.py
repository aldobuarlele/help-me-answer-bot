import asyncio
import time
from src.utils.config_loader import load_config
from src.adapters.whatsapp.driver import WhatsAppDriver
from src.adapters.whatsapp.listener import WhatsAppListener

class WhatsAppListenerTest:
    async def run(self):
        print("--- TEST FASE 2: THE LISTENER (Deep Scan Mode) ---")
        
        try:
            config = load_config()
            print(f"Whitelist saat ini: {config.whatsapp.whitelist}")
        except Exception as e:
            print(f"Error loading config: {e}")
            return

        wa_driver = WhatsAppDriver()
        driver = wa_driver.start()
        
        listener = WhatsAppListener(driver, config)
        
        print("\nINSTRUKSI PENGUJIAN:")
        print("1. Pastikan ada pesan UNREAD dari kontak Whitelist (misal: 'Meta AI' atau 'mm').")
        print("2. Script akan melakukan deep scanning selama 60 detik.")
        print("---------------------------------------------------------")
        
        for i in range(20):
            print(f"\n[Scan ke-{i+1}] Memindai DOM...")
            
            vip_contacts = listener.scan_unread_messages()
            
            if vip_contacts:
                print(f"✅ DITEMUKAN PESAN DARI VIP: {vip_contacts}")
            else:
                print("... Tidak ada pesan baru dari whitelist.")
            
            time.sleep(3) 
            
        print("\n--- TEST SELESAI ---")
        wa_driver.close()

if __name__ == "__main__":
    test = WhatsAppListenerTest()
    asyncio.run(test.run())