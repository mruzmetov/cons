import aiosqlite
from aiogram import Bot

from user.config import DB_PATH, BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

# Get user info
async def get_user_info(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(  # bu yerda u(users) va r(referrals) qisqartmalari
            """
            SELECT 
                u.user_id,                          --user[0]ning id raqami
                u.username,                         --user[1]ning telegram username i
                u.full_name,                        --user[2]To'liq ismi
                u.phone_number,                     --user[3] telefon raqami
                u.balance,                          --user[4]Balansi
                u.referral_count,                   --user[5]taklif qilgan odamlar soni
                r.username as referral_username,    --uni taklif qilgan odamning username i
                r.full_name as referrer_name        --uni taklif qilgan odaming to'liq ismi
            FROM users u 
            LEFT JOIN users r ON u.referred_by = r.user_id   --`users` jadvalni o'zi bilan bo'laymiz
            WHERE u.user_id = ?                              --Ma'lum bir foydalanuvchi uchun malumotni olib kelamiz
            """,
            (user_id,)
        )
        user = await cursor.fetchone()
        return user

# Get referral link
async def get_referral_link(user_id: int):
    return f"https://t.me/{(await bot.get_me()).username}?start={user_id}"

# Get top referrers
async def get_top_referrers(limit = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT user_id, username, full_name, referral_count, balance
            FROM users
            ORDER BY balance DESC, balance DESC
            LIMIT ?""",
            (limit,)
        )
        return await cursor.fetchone()

