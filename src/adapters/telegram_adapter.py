from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from src.utils.logger import setup_logger

class TelegramAdapter:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.log = setup_logger("Telegram_Adapter")

    def register_handlers(self, orchestrator_callback):
        """
        Di sini kita mendaftarkan fungsi apa yang dipicu 
        saat ada pesan masuk.
        """
        
        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            await message.answer("Halo! Saya asisten personal Anda. Ada yang bisa dibantu?")

        @self.dp.message()
        async def handle_any_message(message: types.Message):
            user_id = message.from_user.id
            text = message.text
            
            self.log.info(f"Pesan masuk dari {user_id}: {text}")
            
            response = await orchestrator_callback(user_id, text)
            
            await message.answer(response)

    async def start_polling(self):
        self.log.info("Bot Telegram mulai mendengarkan pesan (Polling)...")
        await self.dp.start_polling(self.bot)