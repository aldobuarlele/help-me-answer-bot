import aiosqlite
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "data/state.db"):
        self.db_path = db_path

    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER PRIMARY KEY,
                    last_reply_at TIMESTAMP,
                    daily_count INTEGER DEFAULT 0,
                    last_reset_date DATE
                )
                """
            )
            await db.commit()

    async def get_user_stats(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM user_stats WHERE user_id = ?", (user_id,)
            ) as cursor:
                return await cursor.fetchone()

    async def update_user_stats(self, user_id: int, count: int, last_reply: datetime):
        async with aiosqlite.connect(self.db_path) as db:
            today = datetime.now().date()
            await db.execute(
                """
                INSERT INTO user_stats (user_id, last_reply_at, daily_count, last_reset_date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    last_reply_at = excluded.last_reply_at,
                    daily_count = excluded.daily_count,
                    last_reset_date = excluded.last_reset_date
                """,
                (user_id, last_reply, count, today),
            )
            await db.commit()