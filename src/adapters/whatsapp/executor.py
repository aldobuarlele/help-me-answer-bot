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

    def open_chat(self, contact_name):
        """Membuka chat dengan mengklik nama di sidebar."""
        try:
            self.log.info(f"Mencoba membuka chat: {contact_name}")
            xpath_contact = f"//span[@title='{contact_name}']"
            
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_contact))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)
            element.click()
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.XPATH_INPUT_BOX))
            )
            time.sleep(1.5) 
            return True
        except Exception as e:
            self.log.error(f"Gagal membuka chat {contact_name}: {e}")
            return False

    def get_last_message(self):
        """Mengambil teks pesan terakhir dengan strategi Multi-Selector."""
        try:
            bubbles = self.driver.find_elements(By.XPATH, self.XPATH_MSG_IN)
            if not bubbles:
                self.log.warning("Tidak ada bubble pesan masuk ditemukan.")
                return ""
            
            last_bubble = bubbles[-1]
            
            try:
                text_element = last_bubble.find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]")
                return text_element.text
            except:
                pass

            try:
                text_element = last_bubble.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
                span_text = text_element.find_element(By.XPATH, ".//span").text
                return span_text
            except:
                pass

            try:
                full_text = last_bubble.text
                lines = full_text.split('\n')
                longest_line = max(lines, key=len)
                return longest_line
            except:
                pass

            self.log.warning("Gagal mengekstrak teks dengan semua metode.")
            return "[Non-Text Message]"

        except Exception as e:
            self.log.error(f"Error fatal get_last_message: {e}")
            return "[Error Reading]"

    def send_message(self, message):
        """Mengetik dan mengirim pesan."""
        try:
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_INPUT_BOX))
            )
            input_box.click() 
            
            self.log.info(f"Mengetik: {message}")
            
            for char in message:
                try:
                    input_box.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.08)) 
                except:
                    pass
            
            time.sleep(0.5)
            input_box.send_keys(Keys.ENTER)
            
            self.log.info("Pesan terkirim.")
            return True
        except Exception as e:
            self.log.error(f"Gagal kirim pesan: {e}")
            return False