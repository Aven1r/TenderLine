import asyncio
import logging
import sys
import os

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import CommandStart
from .api.crud import get_email, get_name_by_email, put_id_to_db

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6384810364:AAGeOaLunuqRv6csNECe3EAvBQ9uLpeyMx4"
bot = Bot(token=TOKEN)

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    email = State() 



@dp.message_handler(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.email)
    await message.answer(
        "Вас приветствует бот для уведомлений сервиса TenderLine. Введите свой email указанный при регистрации на сайте",
        reply_markup=ReplyKeyboardRemove(),
    )
    

async def validate_email(msg: Message) -> bool:
    print(msg)
    return await get_email(msg.text) == None


@dp.message_handler(validate_email, state=Form.email)
async def process_name_invalid(message: Message) -> None:
    return await message.answer("Неверный формат email. Попробуйте еще раз")


@dp.message_handler(state=Form.email)
async def process_name(message: Message, state: FSMContext) -> None:
    print(message.text, '\n\n\n\n\n\n')
    email = await get_email(message.text)
    user_name = await get_name_by_email(message.text)
    await put_id_to_db(message.from_id, message.text)
    await message.answer(f"Здравствуйте, {user_name}! Теперь вы подписаны на уведомления ")
    await state.finish()


async def send_hi_message(telegram_id: int) -> None:
    await bot.send_message(telegram_id, "Пришло уведомление")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


def start_bot():
    asyncio.create_task(main())
