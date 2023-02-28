from aiogram import Bot, Dispatcher, executor, types
from memory_profiler import profile

from bot import config
from bot.guide import talkmanager, user

api_token = config.load_from_env()

bot = Bot(token=api_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user.start(message.chat.id)
    with open('bot/messages/start.txt', 'r') as begin:
        text = begin.readlines()
    await message.answer('\n'.join(text))


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    with open('bot/messages/start.txt', 'r') as begin:
        text = begin.readlines()
    await message.answer('\n'.join(text))


@dp.message_handler(commands=['list'])
async def themes(message: types.Message):
    await message.answer(talkmanager.theme_list())


@dp.message_handler()
@profile
async def search_func(message: types.message):
    answer = talkmanager.conversation(message.text, message.chat.id)
    await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
