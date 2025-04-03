import aiosqlite

from user.config import DB_PATH

async def init_db():      #Ma'lumotlar bazasini ishga tushirish
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                phone_number TEXT,
                username TEXT,
                full_name TEXT,
                balance REAL DEFAULT 0,
                referred_by TEXT DEFAULT NULL,
                referred_by_username TEXT,
                referral_count INTEGER DEFAULT 0,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS referrals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,           
                referrer_id INTEGER,                                    --taklif qilgan odam
                referred_id INTEGER,                                    --taklif qilingan odam
                bonus_awarded BOOLEAN DEFAULT FALSE,                    --bonus beriladi
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(user_id),
                FOREIGN KEY (referred_id) REFERENCES users(user_id)
            )
            ''')
        await db.commit()
