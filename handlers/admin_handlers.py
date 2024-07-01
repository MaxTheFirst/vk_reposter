from bot_dispatcher import dp
from dispatcher import user_db, config
from states import UserStates
from aiogram import filters
from aiogram.types import Message
import textes
import keyboards


@dp.message_handler(filters.Text(config.password), state=[*UserStates.all_states, None], config_chat=False)
async def on_passwoard(message: Message):
    user_db.admin_id = message.chat.id
    await UserStates.menu.set()
    await message.answer(textes.MENU_TEXT, reply_markup=keyboards.commands)
