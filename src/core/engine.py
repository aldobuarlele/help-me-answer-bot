import asyncio
from datetime import datetime, date
from src.utils.config_loader import RootConfig
from src.repository.database import Database
from src.services.ai_service import AiService
from src.utils.logger import setup_logger

class Orchestrator:
    def __init__(self, config: RootConfig, db: Database, ai_service: AiService):
        self.config = config
        self.db = db
        self.ai_service = ai_service
        self.log = setup_logger("Gatekeeper")

    async def handle_message(self, user_id: int, text: str) -> str:
        stats = await self.db.get_user_stats(user_id)
        now = datetime.now()
        today = date.today()

        if not stats:
            await self.db.update_user_stats(user_id, 0, datetime.fromtimestamp(0))
            stats = await self.db.get_user_stats(user_id)

        last_reset = datetime.strptime(stats['last_reset_date'], '%Y-%m-%d').date() if isinstance(stats['last_reset_date'], str) else stats['last_reset_date']
        current_count = stats['daily_count']
        
        if today > last_reset:
            current_count = 0
            self.log.info(f"Daily reset for user {user_id}")

        is_allowed, reason = self._is_allowed(stats, current_count, now)
        if not is_allowed:
            self.log.warning(f"Request REJECTED for {user_id}: {reason}")
            return f"Maaf, {reason}"

        self.log.info(f"Request APPROVED for {user_id}. Calling AI...")
        try:
            persona = self.config.personas.definitions.get(self.config.personas.active_persona)
            response = await self.ai_service.get_response(text, system_instruction=persona)
            
            await self.db.update_user_stats(user_id, current_count + 1, now)
            return response
        except Exception as e:
            self.log.error(f"Error in processing AI response: {e}")
            return "Maaf, terjadi gangguan teknis saat menghubungi AI."

    def _is_allowed(self, stats, current_count, now):
        if current_count >= self.config.bot_settings.max_daily_replies:
            return False, "kuota harian Anda sudah habis."

        last_reply_at = datetime.fromisoformat(stats['last_reply_at']) if isinstance(stats['last_reply_at'], str) else stats['last_reply_at']
        time_diff = (now - last_reply_at).total_seconds()
        
        if time_diff < self.config.bot_settings.reply_interval:
            wait_time = int(self.config.bot_settings.reply_interval - time_diff)
            return False, f"tunggu {wait_time} detik lagi sebelum mengirim pesan berikutnya."

        return True, None