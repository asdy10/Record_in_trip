import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand

from data import config
from filters import IsUser
from keyboards.default.markups import *
from loader import dp, db, bot
import filters
import logging

from utils.db.get_set_info import get_user, create_user

filters.setup(dp)

WEBAPP_HOST = "127.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5002))


@dp.message_handler(IsUser(), commands='start')
async def cmd_start_admin(message: types.Message):
    cid = message.from_user.id
    if get_user(cid):
        await message.answer('Для оформления билета выберете в меню пункт «Забронировать»')
    else:
        create_user(cid, message.from_user.username)
        await message.answer('Привет, я бот для бронирования поездки. Для оформления билета выберете в меню пункт «Забронировать»')


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()
    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)
    await dp.bot.set_my_commands(commands=[BotCommand('reg', 'Забронировать')])


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':
    if "HEROKU" in list(os.environ.keys()):
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
