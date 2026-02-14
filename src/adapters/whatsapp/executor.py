import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import setup_logger

class WhatsAppExecutor:
    def __init__(self, driver):
        self.driver = driver
        self.log = setup_logger("WA_Executor")
        self.XPATH_INPUT_BOX = "//div[@contenteditable='true'][@data-tab='10']"
        self.XPATH_MSG_IN = "//div[contains(@class, 'message-in')]" 
        self.XPATH_MSG_TEXT = ".//span[contains(@class, 'selectable-text')]"

    def open_chat(self, contact_name):
        """Membuka chat dengan mengklik nama di sidebar."""
        try:
            self.log.info(f"Mencoba membuka chat: {contact_name}")
            
            xpath_contact = f"//span[@title='{contact_name}']"
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, xpath_contact))
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)
            
            element.click()
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.XPATH_INPUT_BOX))
            )
            
            time.sleep(1) 
            return True
        except Exception as e:
            self.log.error(f"Gagal membuka chat {contact_name}: {e}")
            return False

    def get_last_message(self):
        """Mengambil teks pesan terakhir dari lawan bicara."""
        try:
            time.sleep(2)
            
            bubbles = self.driver.find_elements(By.XPATH, self.XPATH_MSG_IN)
            if not bubbles:
                self.log.warning("Tidak ada pesan masuk terbaca.")
                return ""
            
            last_bubble = bubbles[-1]
            text_element = last_bubble.find_element(By.XPATH, self.XPATH_MSG_TEXT)
            return text_element.text
        except Exception as e:
            self.log.warning(f"Gagal baca teks pesan terakhir: {e}")
            return "[Non-Text Message]"

    def send_message(self, message):
        """Mengetik dan mengirim pesan dengan gaya manusia."""
        try:
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_INPUT_BOX))
            )
            input_box.click() 
            
            self.log.info(f"Mengetik balasan: {message}")
            
            for char in message:
                input_box.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(0.5)
            input_box.send_keys(Keys.ENTER)
            
            self.log.info("Pesan BERHASIL dikirim.")
            return True
        except Exception as e:
            self.log.error(f"Gagal kirim pesan: {e}")
            return False