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

    def _is_allowed(self, stats, current_count, now):
        if current_count >= self.config.bot_settings.max_daily_replies:
            return False, "kuota habis"

        last_reply_at = datetime.fromisoformat(stats['last_reply_at']) if isinstance(stats['last_reply_at'], str) else stats['last_reply_at']
        time_diff = (now - last_reply_at).total_seconds()
        
        if time_diff < self.config.bot_settings.reply_interval:
            return False, int(self.config.bot_settings.reply_interval - time_diff)

        return True, None
    
    async def handle_message(self, user_id: int, text: str):
        stats = await self.db.get_user_stats(user_id)
        now = datetime.now()
        
        if not stats:
            await self.db.update_user_stats(user_id, 0, datetime.fromtimestamp(0))
            stats = await self.db.get_user_stats(user_id)

        last_reset = datetime.strptime(stats['last_reset_date'], '%Y-%m-%d').date() if isinstance(stats['last_reset_date'], str) else stats['last_reset_date']
        current_count = stats['daily_count']
        if datetime.now().date() > last_reset:
            current_count = 0

        is_allowed, result = self._is_allowed(stats, current_count, now)
        
        if not is_allowed:
            return False, result

        try:
            persona = self.config.personas.definitions.get(self.config.personas.active_persona)
            response = await self.ai_service.get_response(text, system_instruction=persona)
            
            await self.db.update_user_stats(user_id, current_count + 1, now)
            return True, response
        except Exception as e:
            self.log.error(f"AI Error: {e}")
            return None, "Aduh, lagi pusing nih otaknya. Coba lagi bentar ya."