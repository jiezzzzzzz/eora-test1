import asyncio
import logging
import config
import sqlite3
import os

from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

sqlite_connection = sqlite3.connect('cat_or_bread.db')
cursor = sqlite_connection.cursor()

query1 = "CREATE TABLE IF NOT EXISTS cat_or_bread_db (`id` INT NOT NULL,`user_id` INT NULL,`message1` VARCHAR(45) NULL,`message2` VARCHAR(45) NULL,PRIMARY KEY (`id`));"
cursor.execute(query1)
sqlite_connection.commit()
yes_variants = ('конечно', 'ага', 'пожалуй', 'да')
no_variants = ('нет, конечно', 'ноуп', 'найн', 'нет')


class DetectObject(StatesGroup):
    waiting_for_answer1 = State()
    waiting_for_answer2 = State()


async def start(message: types.Message):
    print(message)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer('Привет! Я помогу отличить кота от хлеба! Объект перед тобой квадратный?',
                         reply_markup=keyboard)
    await DetectObject.waiting_for_answer1.set()


async def first_question(message: types.Message, state: FSMContext):
    if message.text.lower() not in yes_variants + no_variants:
        await message.answer(f'Ничего не понял')
        return
    await state.update_data(first_choice=message.text.lower())
    if message.text.lower() in no_variants:
        await message.answer('Это кот, а не хлеб! Не ешь его!', reply_markup=types.ReplyKeyboardRemove())
        return
    await DetectObject.next()
    message1 = message.text
    user_id = message.from_user.id
    query = 'INSERT INTO cat_or_bread_db (user_id, message1) VALUES (%s, %s)'
    values = (user_id, message1)
    cursor.execute(query, values)
    sqlite_connection.commit()
    await message.answer('У него есть уши?')


async def second_question(message: types.Message, state: FSMContext):
    if message.text.lower() not in yes_variants + no_variants:
        await message.answer(f'Ничего не понял')
        return
    if message.text.lower() in no_variants:
        await message.answer('Это хлеб, а не кот! Ешь его!', reply_markup=types.ReplyKeyboardRemove())
        return
    user_data = await state.get_data()
    await message.answer(f'Это кот, а не хлеб! Не ешь его!', reply_markup=types.ReplyKeyboardRemove())
    message2 = message.text
    query = 'INSERT INTO cat_or_bread_db (message2) VALUES (%s)'
    value = (message2)
    cursor.execute(query, value)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()
    await state.finish()


def register_handlers_state(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(first_question, state=DetectObject.waiting_for_answer1)
    dp.register_message_handler(second_question, state=DetectObject.waiting_for_answer2)


logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_state(dp)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
