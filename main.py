import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from user.config import BOT_TOKEN
from user.database.create import init_db
from user.handlers import start, referral, balance
from user.logger import logger



async def main():
    #Botni sozlash
    bot = Bot(
        token=BOT_TOKEN, 
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    #Dispatcher yaratish
    dp = Dispatcher(storage = MemoryStorage())

    #Routerlarni qo'shish
    dp.include_router(start.router)
    dp.include_router(referral.router)
    dp.include_router(balance.router)

    
    try:
        await init_db()  # Ma'lumotlar bazasini yaratish
        logger.info("DataBase yaratildi")
    except Exception as error:
        logger.info(f"DataBase yaratishda xatolik: {error}")
    
    try:
        await dp.start_polling(bot)
    except Exception as error:
        print(f"Kutilmagan xatolik: {error}")
    finally:
        await bot.session.close()
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("dasturchi tomonidan bot to'xtatildi")
    except Exception as e:
        print(f"Halokatli xatolik: {e}")
