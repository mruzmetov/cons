from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from user.database.get import get_referral_link, get_top_referrers
from user.config import BONUS_AMOUNT

router = Router()


@router.message(Command("referral"))
async def cmd_referral(message: types.Message):
    referral_link = await get_referral_link(message.from_user.id)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="📤 Havolani ulashish",
        url=f"https://t.me/share/url?url={referral_link}&text=Do'stlarim uchun foydali bot!"
    ))

    await message.answer(
        f"👋 Do'stlaringizni taklif qiling va har bir taklif uchun ${BONUS_AMOUNT} bonus oling!\n\n"
        f"📎 Sizning taklif havolangiz:\n<code>{referral_link}</code>\n\n"
        "📢 Havolani do'stlaringizga yuboring yoki quyidagi tugma orqali ulashing:",
        reply_markup=builder.as_markup(),
        parse_mode=ParseMode.HTML
    )


@router.message(Command("top"))
async def cmd_top(message: types.Message):
    top_referrers = await get_top_referrers()

    if not top_referrers:
        await message.answer("🤷‍♂️ Hali hech qanday takliflar mavjud emas.")
        return

    text = "🏆 Eng yaxshi taklif qiluvchilar:\n\n"
    for i, (user_id, username, full_name, count, balance) in enumerate(top_referrers, 1):
        name = f"@{username}" if username else full_name
        text += f"{i}. {name} - {count} ta taklif (${balance:.2f})\n"

    await message.answer(text)


# Callback handler
@router.callback_query(lambda call: call.data == "referrals")
async def callback_referrals(callback: types.CallbackQuery):
    referral_link = await get_referral_link(callback.from_user.id)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="📤 Havolani ulashish",
        url=f"https://t.me/share/url?url={referral_link}&text=Do'stlarim uchun foydali bot!"
    ))

    await callback.message.answer(
        f"👋 Do'stlaringizni taklif qiling va har bir taklif uchun ${BONUS_AMOUNT} bonus oling!\n\n"
        f"📎 Sizning taklif havolangiz:\n<code>{referral_link}</code>",
        reply_markup=builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()