from aiogram import types, Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from user.database.get import get_user_info
from user.database.register import register_user
from user.keyboards import get_main_keyboard
from user.logger import logger
from user.config import BONUS_AMOUNT, BOT_TOKEN

router = Router()
bot = Bot(token=BOT_TOKEN)

@router.message(CommandStart)
async def start_command(message: types.Message):
    args = message.text.split()
    referred_by = None

    #Check is start parameter contains referral id (start parametrida havola identificatori mavjudligini tekshiring)
    if len(args) > 1 and args[1].isdigit():
        referred_by = int(args[1])

    # Register user (or update info if already exists)
    is_new_user = await register_user(message.from_user, referred_by)

    if is_new_user and referred_by:
        """Notify referrer about successful referral"""
        try:
            await bot.send_message(
                referred_by,
                f"🎉 Sizning do'stingiz {message.from_user.full_name} botga a'zo bo'ldi!\n"
                f"Sizga ${BONUS_AMOUNT} bonus qo'shildi."
            )
        except Exception as e:
            logger.error(f"Notify referrer about: {e}")

    # Prepare response (javob tayyorlang)
    user = await get_user_info(message.from_user.id)
    text = f"👋 Salom, {message.from_user.full_name}!\n\n"

    if is_new_user and referred_by:
        referrer_info = f"Sizni {user[6] or user[7]} taklif qildi"
        text += referrer_info + "\n\n"
    elif is_new_user:
        text += "🤖 Bu bot orqali do'stlaringizni taklif qilib bonus ishlab olishingiz mumkin!\n\n"

    text += (
        f"Joriy balans: {user[4]:.2f}\n"
        f"Takliflar soni: {user[5]}\n\n"
        "📢 Do'stlaringizni taklif qilish uchun quyidagi havoladan foydalaning:"
    )
    keyboard = await get_main_keyboard(message.from_user.id) #tugmalarni chaqirish
    await message.answer(
        text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
