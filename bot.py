from config import TOKEN, PROXY, TEXT

from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, loop=loop,parse_mode=types.ParseMode.MARKDOWN, proxy=PROXY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(TEXT['START'])


@dp.message_handler(commands=['help'])
async def send_help(message):
    await message.reply(TEXT['HELP'])


@dp.inline_handler()
async def inline_def(inline_query):
    gi_list = ['HUB', 'TGK']
    input_contents = [types.InputContactMessageContent(f"/g_def {i}") for i in gi_list]
    item1 = types.InlineQueryResultArticle(id='1', title='🛡 HUB', input_message_content=input_contents[0])
    item2 = types.InlineQueryResultArticle(id='2', title='🛡 TGK', input_message_content=input_contents[1])
    await bot.answer_inline_query(inline_query.id, results=[item1], cache_time=1)
    await bot.answer_inline_query(inline_query.id, results=[item2], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=60)
