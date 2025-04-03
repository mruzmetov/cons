from aiogram import Router, types
from aiogram.filters import Command

from user.database.get import get_user_info

router = Router()

@router.message(Command("balance"))
async def command_balance(message: types.Message):
    user = await get_user_info(message.from_user.id)
    await message.answer(
        f"💰 Sizning balansingiz: ${user[3]:.2f}\n"
        f"👥 Taklif qilingan do'stlaringiz: {user[4]}\n\n"
        "💡 Balansingizni botda keyingi yangilanishlarida ishlatishingiz mumkin bo'ladi."
    )


# Callback handlers
@router.callback_query(lambda call: call.data == "balance")
async def callback_balance(callback: types.CallbackQuery):
    user = await get_user_info(callback.from_user.id)
    await callback.message.answer(
        f"Sizning balansingiz: $ {user[3]:.2f}\n"
        f"Taklif qilingan do'stlaringiz: {user[4]}"
    )
    await callback.answer()

