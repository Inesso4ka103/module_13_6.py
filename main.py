from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)

kb1 = InlineKeyboardMarkup()
in_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.add(in_button)
kb1.add(in_button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать норму калорий')],
        [KeyboardButton(text='Формулы расчёта')]
    ], resize_keyboard=True
)

@dp.message_handler(text=['/start'])
async def start(message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте.')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161")
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = (10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])-161)
    await message.answer(f'Ваша норма каллорий: {norma}')
    await UserState.weight.set()
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer(f'Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

