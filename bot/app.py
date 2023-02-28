from aiogram import Bot, Dispatcher, executor, types

from bot.guide import talkmanager

bot = Bot(token = '1747747627:AAGxFv9VQEQm7fL81Uu9Vjx5KNjWKyCRL7k' )#Инициализация бота
dp = Dispatcher(bot)#Определение диспетчера

@dp.message_handler(commands=['start'])#Хэндлер для функции start
async def hi_func(message: types.Message):
    await message.answer("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['list'])  # функция показывает список доступных тем
async def hi_func(message: types.Message):

    await message.answer('список существующих тем:\n')


@dp.message_handler()#Хэндлер для функции считывания
async def search_func(message: types.message):
    talkmanager.conversation(message.text, 145)
    
#Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)