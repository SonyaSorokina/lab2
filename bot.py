import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from random import *

global x, run_vodit_bot, run_vodit_polsovatel, cur, l, r
x = 0
run_vodit_bot = False
run_vodit_polsovatel = False
r = 10
l = 1
cur = 5

API_TOKEN = 'токен'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
def vodit_bot(message, x):
    global run_vodit_bot
    if (int(message) > x):
        answ = "неправильно! загаданное число меньше"
    elif (int(message) < x):
        answ = "неправильно! загаданное число больше"
    else:
        answ = "вы угадали! \nнажмите на /start если хотите сыграть со мной снова!"
        run_vodit_bot = False
    return answ
def vodit_polsovatel(text):
    global run_vodit_polsovatel, cur, l, r
    if (text == "меньше"):
        r = cur - 1
        cur = (r + l) // 2
    elif (text == "больше"):
        l = cur + 1
        cur = (r + l) // 2
    elif (text == "ты угадал!!"):
        run_vodit_polsovatel = False
        cur = 5
        r = 10
        l = 1

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="я хочу угадывать"),
            types.KeyboardButton(text="я хочу загадывать")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await message.reply("доброго времени суток!\nвыберите действие и давайте играть\nавтор: Сорокина Соня ПИН222",
                        reply_markup=keyboard)

@dp.message_handler(text='я хочу угадывать')
async def zagadka(message: types.Message):
    global x, run_vodit_bot
    x = randint(1, 10)
    run_vodit_bot = True
    await message.answer("я загадал число от 1 до 10 включительно\nвведите число и я скажу угадали вы или нет")

@dp.message_handler(text='я хочу загадывать')
async def zagadka2(message: types.Message):
    kb2 = [
        [
            types.KeyboardButton(text="я загадал!"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb2)
    global run_vodit_polsovatel
    run_vodit_polsovatel = True
    await message.answer("я подожду немного\nнажмите на кнопочку как загадаете число от 1 до 10", reply_markup=keyboard)

@dp.message_handler()
async def ugadaika(message: types.Message):
    global x, run_vodit_bot, run_vodit_polsovatel
    if (run_vodit_bot == True):
        text = vodit_bot(message.text, x)
        await message.answer(text)
    elif (run_vodit_polsovatel == True):
        global cur
        kb3 = [
            [
                types.KeyboardButton(text="меньше"),
                types.KeyboardButton(text="больше"),
                types.KeyboardButton(text="ты угадал!!")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb3)
        vodit_polsovatel(message.text)
        if (run_vodit_polsovatel == True):
            await message.answer(cur, reply_markup=keyboard)
        else:
            await message.answer("спасибо за игру\nнажмите на /start если хотите сыграть со мной снова!")
    else:
        await message.answer("я не знаю что это за команда")

def start():
    executor.start_polling(dp, skip_updates=True)
