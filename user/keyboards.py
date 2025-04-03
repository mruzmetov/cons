from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from user.database.get import get_referral_link


# Create keyboard with referral link
async def get_main_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="📤 Havolani ulashish",
        url = f"https://t.me/share/url?url={(await get_referral_link(user_id))}&text=Do'stlarim uchun foydali bot"
    ))
    builder.row(
        InlineKeyboardButton(text="💰 Balans", callback_data="balance"),
        InlineKeyboardButton(text="👥 Takliflar", callback_data="referrals")
    )
    return builder.as_markup()

def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )