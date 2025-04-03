import aiosqlite
from aiogram import types
from user.config import DB_PATH, BONUS_AMOUNT


# Register user or get existing user (userni ro'yxatdan o'tkazing yoki mavjudini oling)
async def register_user(user: types.User, referred_by: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        # user mavjudligini tekshiring
        cursor = await db.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user.id,)
        )
        existing_user = await cursor.fetchone()    # foydalanuvchi mavjud bo`lsa

        if not existing_user:
            # Register new user (Yangi foydalanuvchini ro'yhatdan o'tkazish)
            await db.execute(
                """
                INSERT INTO users 
                (user_id, username, full_name, referred_by)
                VALUES (?, ?, ?, ?)""",
                (user.id, user.username, user.full_name, referred_by)
            )

            # (If this is a referral, record it) Agar bu referral bo'lsa, uni qayd qiling
            if referred_by:
                await db.execute(
                    """INSERT INTO referrals 
                    (referrer_id, referred_id)    --referrer_id ga -> referred_by qiymatini 
                    VALUES (?, ?)""",             #--referred_id ga -> user.id qiymatini kirit
                    (referred_by, user.id)
                )
                # (Update referrer's referral count) Taklif qiluvchi foydalanuvchilar sonini yangilash
                await db.execute(
                    "UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?",
                    (referred_by,)
                )
                # (Award bonus to referrer) Taklif qiluvchi balansini yangilash
                await db.execute(
                    "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                    (BONUS_AMOUNT, referred_by)
                )
                # (Mark bonus as awarded in referrals table) referrals jadvalida Mukofot berildi deb belgilash
                await db.execute(
                    "UPDATE referrals SET bonus_awarded = TRUE WHERE referrer_id = ? AND referred_id = ?",
                    (referred_by, user.id)
                )

            await db.commit()
            return True # New user registered 
        return False # User already exists (Foydalanuvchi allaqachon mavjud)
