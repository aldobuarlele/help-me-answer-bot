import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.utils.logger import setup_logger

class WhatsAppDriver:
    def __init__(self):
        self.log = setup_logger("WA_Driver")
        self.driver = None
        self.user_data_dir = os.path.join(os.getcwd(), "chrome_data")

    def start(self):
        self.log.info("Menyiapkan Chrome Driver...")
        
        options = Options()
        options.add_argument(f"user-data-dir={self.user_data_dir}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            self.driver.get("https://web.whatsapp.com")
            self.log.info("WhatsApp Web terbuka. Menunggu loading...")
            return self.driver
        except Exception as e:
            self.log.error(f"Gagal membuka browser: {e}")
            raise e

    def wait_for_login(self):
        """Menunggu sampai user melakukan scan QR code."""
        self.log.info("Silakan SCAN QR CODE jika belum login...")
        
        while True:
            try:
                if "WhatsApp" in self.driver.title:
                    pass
                
                time.sleep(3)
                return True
            except Exception as e:
                pass

    def close(self):
        if self.driver:
            self.driver.quit()
            self.log.info("Browser ditutup.")