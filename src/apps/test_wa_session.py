import asyncio
import time
from src.adapters.whatsapp.driver import WhatsAppDriver

class WhatsAppSessionTest:
    async def run(self):
        print("--- TEST FASE 1: SESSION PERSISTENCE ---")
        
        wa = WhatsAppDriver()
        
        print("\n[STEP 1] Membuka Browser...")
        driver = wa.start()
        
        print("INSTRUKSI:")
        print("1. Jika muncul QR Code, SCAN SEKARANG dengan HP Anda.")
        print("2. Script akan menunggu 30 detik untuk memastikan login tersimpan.")
        
        await asyncio.sleep(30) 
        
        print("\n[STEP 2] Menutup Browser untuk tes persistensi...")
        wa.close()
        
        await asyncio.sleep(5)
        
        print("\n[STEP 3] Membuka Kembali (Re-Run)...")
        print("Ekspektasi: Browser terbuka LANGSUNG masuk chat list TANPA QR Code.")
        
        wa.start()
        
        await asyncio.sleep(15)
        wa.close()
        print("--- TEST SELESAI ---")

if __name__ == "__main__":
    test_app = WhatsAppSessionTest()
    asyncio.run(test_app.run())