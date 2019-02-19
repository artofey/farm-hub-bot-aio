from config import TOKEN, PROXY, TEXT

from aiogram import Bot, Dispatcher, executor, types
import logging


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, proxy=PROXY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(TEXT['START'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=60)
