from bot_dispatcher import dp
from states import UserStates
from aiogram.types import CallbackQuery, Message
from textes import *
import keyboards


menu_textes = {
    MAIN_GROUP_CMD: (UserStates.main_group, MAIN_GROUP_TEXT),
    ADD_GROUPS_CMD: (UserStates.add_groups, ADD_GROUPS_TEXT)
}


@dp.message_handler(commands=[START_COMMAND], state=None, config_chat=False)
async def start(message: Message):
    await message.answer(HELLOW)


@dp.message_handler(commands=[MENU_COMMAND], state=[*UserStates.all_states, None], config_chat=True)
async def menu(message: Message):
    await UserStates.menu.set()
    await message.answer(MENU_TEXT, reply_markup=keyboards.commands)


@dp.callback_query_handler(callback_cmd=MENU_CMD, state=UserStates.all_states)
async def back_menu(callback: CallbackQuery):
    await UserStates.menu.set()
    await callback.message.edit_text(MENU_TEXT, reply_markup=keyboards.commands)


@dp.callback_query_handler(callback_cmd=list(menu_textes.keys()), state=UserStates.menu)
async def read_cmd(callback: CallbackQuery):
    state, text = menu_textes[callback.data]
    await state.set()
    await callback.message.edit_text(text, reply_markup=keyboards.menu)
