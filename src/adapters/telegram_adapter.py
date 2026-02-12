import asyncio
from aiogram import Bot, Dispatcher, types
from src.utils.logger import setup_logger

class TelegramAdapter:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.log = setup_logger("Telegram_Adapter")
        self.pending_queue = {} 
    def register_handlers(self, orchestrator):
        @self.dp.message()
        async def handle_any_message(message: types.Message):
            user_id = message.from_user.id
            text = message.text
            
            status, result = await orchestrator.handle_message(user_id, text)
            
            if status is True:
                await message.answer(result)
            elif isinstance(result, int):
                self.log.info(f"User {user_id} masuk antrean. Tunggu {result} detik.")
                self.pending_queue[user_id] = text

    async def start_worker(self, orchestrator):
        """Worker background untuk memproses antrean secara otomatis."""
        while True:
            await asyncio.sleep(1)
            for user_id in list(self.pending_queue.keys()):
                text = self.pending_queue[user_id]
                status, result = await orchestrator.handle_message(user_id, text)
                
                if status is True:
                    await self.bot.send_message(user_id, result)
                    del self.pending_queue[user_id]
                    self.log.info(f"Pesan tertunda untuk {user_id} berhasil dikirim.")

    async def start_polling(self, orchestrator):
        self.log.info("Telegram Bot Polling Started...")
        asyncio.create_task(self.start_worker(orchestrator))
        await self.dp.start_polling(self.bot)