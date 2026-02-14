import time
from selenium.webdriver.common.by import By
from src.utils.logger import setup_logger

class WhatsAppListener:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.log = setup_logger("WA_Listener")
        self.XPATH_ROWS = "//div[@role='row']"
        self.XPATH_NAME = ".//span[@title]"
        self.XPATH_UNREAD_BADGE = ".//span[contains(@aria-label, 'nread')]"

    def scan_unread_messages(self):
        """
        Memindai setiap baris chat untuk mencari pesan belum dibaca dari VIP.
        """
        try:
            chat_rows = self.driver.find_elements(By.XPATH, self.XPATH_ROWS)
            detected_chats = []

            print(f"DEBUG: Ditemukan {len(chat_rows)} baris chat.") 

            for row in chat_rows:
                try:
                    name_element = row.find_element(By.XPATH, self.XPATH_NAME)
                    contact_name = name_element.get_attribute("title")
                    
                    unread_indicators = row.find_elements(By.XPATH, self.XPATH_UNREAD_BADGE)
                    
                    if len(unread_indicators) > 0:
                        self.log.info(f"DEBUG: Unread terdeteksi di '{contact_name}'")
                        
                        if self._is_whitelisted(contact_name):
                            self.log.info(f"[MATCH] Pesan VIP dari: {contact_name}")
                            detected_chats.append(contact_name)
                        else:
                            pass
                    
                except Exception as e:
                    continue

            return list(set(detected_chats))

        except Exception as e:
            self.log.error(f"Error scanning: {e}")
            return []

    def _is_whitelisted(self, name):
        whitelist = []
        if hasattr(self.config, 'whatsapp'):
            whitelist = self.config.whatsapp.whitelist
        elif isinstance(self.config, dict):
             whitelist = self.config.get('whatsapp', {}).get('whitelist', [])
        
        return name in whitelist