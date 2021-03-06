import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.executor import start_webhook

from market import get_data_from_message, save_market_to_db, get_all_markets
from config import *
import db


WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')
TOKEN = os.environ.get('TOKEN')
CHAT_ID = int(os.environ.get('CHAT_ID'))
CHAT_WARS_BOT_ID = 265204902

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

def_list = []
def_list = db.get_defers_list_from_db()
lm_id = 0


def get_def_msg():
    """ Формирвание сообщения списка защитников """
    global def_list
    return '{}({})\n<b>{}</b>'.format(TEXT['ANS'],
                                      str(len(def_list)),
                                      ', '.join(def_list))


keyboard = types.InlineKeyboardMarkup()
keyboard.row_width = 2
keyboard.add(types.InlineKeyboardButton(text=TEXT['BTN_SWITCH'],
                                        callback_data='go'),
             types.InlineKeyboardButton(text=TEXT['BTN_DEF'],
                                        switch_inline_query='d'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(TEXT['START'])


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(' '.join(TEXT['HELP']))


@dp.message_handler(commands=['all_markets'])
async def send_all_markets(message: types.Message):
    await message.reply(get_all_markets())


async def send_def(chat_id, msg_text, kb):
    result = await bot.send_message(chat_id=chat_id,
                                    text=msg_text,
                                    reply_markup=kb)
    global lm_id
    lm_id = result.message_id


@dp.message_handler(commands=['bot'])
async def send_def_message(message: types.Message):
    """ повторная отправка текущего статуса по команде с изменением
        глобальной переменной с ID последнего сообщения """
    await send_def(CHAT_ID, get_def_msg(), keyboard)


@dp.message_handler(lambda message: message.text
                    and message.text.startswith('Здесь ты можешь купить и продать разные ресурсы.')
                    and message.chat.id == int(CHAT_ID)
                    and message.forward_from.id == CHAT_WARS_BOT_ID)
async def send_replay_for_market_message(msg: types.Message):
    """ обработка сообщения от биржи в игре """
    try:
        market_data = get_data_from_message(msg)
    except Exception as err:
        await msg.reply(f'Ошибка при парсинге сообщения от биржи: \n {err}')
    else:
        try:
            save_market_to_db(market_data)
        except Exception as err:
            await msg.reply(f'Ошибка при сохранении данных этой биржи: \n {err}')
        else:
            await msg.reply(f'Спасибо. Биржа сохранена.')


def update_def_list(user_name: str):
    """ обновление списка защитников """
    global def_list
    if user_name in def_list:
        def_list.remove(user_name)
        db.del_defer_from_db(user_name)
    else:
        def_list.append(user_name)
        db.add_defer_to_db(user_name)


@dp.callback_query_handler(lambda c: c.message.message_id == lm_id and c.data == 'go')
async def process_callback_btn_go(callback_query: types.CallbackQuery):
    """ если запрос от последнего сообщения с data = 'go' """
    update_def_list(callback_query.from_user.username)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text=get_def_msg(),
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data != 'go')
async def process_all_callback(callback_query: types.CallbackQuery):
    """ ответ на все нажатия кнопок """
    await bot.answer_callback_query(callback_query.id)


@dp.inline_handler(lambda query: query.query == 'd')
async def inline_def(inline_query: types.InlineQuery):
    """ обработка инлайн меню """
    def_target = [("1", "🛡 HUB", types.InputTextMessageContent("/g_def HUB"))]
    items = []
    for id, title, i_m_c in def_target:
        items.append(types.InlineQueryResultArticle(id=id,
                                                    title=title,
                                                    input_message_content=i_m_c))
    try:
        await bot.answer_inline_query(inline_query.id,
                                      results=items,
                                      cache_time=1)
    except Exception as e:
        print(e)


async def reset_def_list():
    """ сброс списка защитников и отправка сообщения """
    global def_list
    def_list = []
    db.del_all_defers_from_db()
    await send_def(CHAT_ID, get_def_msg(), keyboard)


# запускаем отправку сообщения по расписанию
time_do_it = [(22, 10), (6, 10), (14, 10)]
scheduler = AsyncIOScheduler()
for h, m in time_do_it:
    scheduler.add_job(reset_def_list, 'cron', hour=h, minute=m)
scheduler.start()


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
