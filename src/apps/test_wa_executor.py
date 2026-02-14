import asyncio
import time
from src.adapters.whatsapp.driver import WhatsAppDriver
from src.adapters.whatsapp.executor import WhatsAppExecutor

class WhatsAppExecutorTest:
    async def run(self):
        print("--- TEST FASE 3: THE ACTUATOR (Uji Coba Kirim Pesan) ---")
        
        TARGET_CONTACT = "Meta AI"  
        
        wa = WhatsAppDriver()
        driver = wa.start()
        
        print("Menunggu 10 detik agar WhatsApp Web load sempurna...")
        time.sleep(10) 
        
        executor = WhatsAppExecutor(driver)
        
        print(f"\n[STEP 1] Mencari kontak '{TARGET_CONTACT}'...")
        if executor.open_chat(TARGET_CONTACT):
            print("✅ Chat terbuka.")
            
            print("\n[STEP 2] Membaca pesan terakhir...")
            last_msg = executor.get_last_message()
            print(f"📩 Pesan terakhir mereka: '{last_msg}'")
            
            print("\n[STEP 3] Mencoba membalas...")
            reply_text = "Halo, ini tes otomatis (Fase 3 Actuator). Abaikan ya."
            
            executor.send_message(reply_text)
            print("✅ Selesai mengetik.")
            
        else:
            print(f"❌ Gagal menemukan kontak '{TARGET_CONTACT}'.")
        
        print("\nMenunggu 5 detik sebelum tutup browser...")
        time.sleep(5)
        wa.close()

if __name__ == "__main__":
    test = WhatsAppExecutorTest()
    asyncio.run(test.run())