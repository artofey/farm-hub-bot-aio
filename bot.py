from config import TOKEN, PROXY, TEXT, CHAT_ID

from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, loop=loop, parse_mode=types.ParseMode.HTML, proxy=PROXY)
dp = Dispatcher(bot)

def_list = []
lm_id = 0
lch_id = CHAT_ID


def get_def_msg():
    global def_list
    return '{}({})\n<b>{}</b>'.format(TEXT['ANS'], str(len(def_list)), ', '.join(def_list))


keyboard = types.InlineKeyboardMarkup()
keyboard.row_width = 2
keyboard.add(types.InlineKeyboardButton(text=TEXT['BTN_SWITCH'], callback_data='go'),
             types.InlineKeyboardButton(text=TEXT['BTN_DEF'], switch_inline_query='d'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(TEXT['START'])


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(' '.join(TEXT['HELP']))


async def send_def(chat_id, msg_text, kb):
    return await bot.send_message(chat_id=chat_id, text=msg_text, reply_markup=kb)


# повторная отправка текущего статуса по команде с изменением глобальной переменной с ID последнего сообщения
@dp.message_handler(commands=['bot'])
async def send_def_message(message: types.Message):
    result = await send_def(message.chat.id, get_def_msg(), keyboard)
    global lm_id, lch_id
    lm_id = result.message_id
    lch_id = result.chat.id


# повторная отправка текущего статуса и сброс списка защитников
# с изменением глобальной переменной с ID последнего сообщения
@dp.message_handler()
async def send_def_message_and_reset(message: types.Message):
    result = await send_def(message.chat.id, get_def_msg(), keyboard)
    global lm_id, def_list
    def_list = []
    lm_id = result.message_id


# обновление списка защитников
def update_def_list(user_name: str):
    global def_list
    if user_name in def_list:
        def_list.remove(user_name)
    else:
        def_list.append(user_name)


# если запрос от последнего сообщения с data = 'go'
@dp.callback_query_handler(lambda c: c.message.message_id == lm_id and c.data == 'go')
async def process_callback_btn_go(callback_query: types.CallbackQuery):
    update_def_list(callback_query.from_user.username)
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text=get_def_msg(),
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard)


# ответ на все нажатия кнопок
@dp.callback_query_handler(lambda c: c.data != 'go')
async def process_all_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)


@dp.inline_handler(lambda query: query.query == 'd')
async def inline_def(inline_query: types.InlineQuery):
    input_content = types.InputTextMessageContent("/g_def HUB")
    item1 = types.InlineQueryResultArticle(id='1', title='🛡 HUB', input_message_content=input_content)
    try:
        await bot.answer_inline_query(inline_query.id, results=[item1], cache_time=1)
    except Exception as e:
        print(e)


# сброс списка защитников и отправка сообщения
async def reset_def_list():
    global def_list, lch_id
    def_list = []
    await send_def(lch_id, get_def_msg(), keyboard)


# запускаем отправку сообщения по расписанию
time_do_it = [(1, 10), (9, 10), (17, 10), (21, 46)]
scheduler = AsyncIOScheduler()
for h, m in time_do_it:
    scheduler.add_job(reset_def_list, 'cron', hour=h, minute=m)
scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=60)
