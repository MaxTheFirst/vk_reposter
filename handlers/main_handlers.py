from .urls_utils import *
from bot_dispatcher import dp
from dispatcher import user_db
from db import DBManager
from states import UserStates
from aiogram.types import Message, CallbackQuery
import textes
import keyboards


@dp.message_handler(state=UserStates.main_group)
async def read_main_group(message: Message):
    id = await read_vk_urls(message, True)
    if id:
        user_db.group_id = id
        await message.answer(textes.MAIN_GROUP_OK, reply_markup=keyboards.menu)


@dp.message_handler(state=UserStates.add_groups)
async def add_groups(message: Message):
    groups = await read_vk_urls(message)
    last_groups = [group.id for group in user_db.groups]
    if groups:
        for group in groups:
            if group in last_groups:
                text = textes.VK_URL + groups[group] + textes.GROUP_YET
                await message.answer(text, reply_markup=keyboards.menu)
                return
        DBManager.add_groups(groups)
        await message.answer(textes.ADD_GROUPS_OK, reply_markup=keyboards.menu)


@dp.callback_query_handler(callback_cmd=textes.DEL_GROUPS_CMD, state=UserStates.menu)
async def mess_del(callback: CallbackQuery):
    text = await give_urls_text(textes.DEL_GROUPS_TEXT, callback)
    await UserStates.del_groups.set()
    await callback.message.edit_text(text, reply_markup=keyboards.menu)


@dp.message_handler(state=UserStates.del_groups)
async def del_groups(message: Message):
    groups = await read_urls_in_db(message)
    if groups:
        DBManager.delete_chat(groups)
        await message.answer(textes.DEL_GROUPS_OK, reply_markup=keyboards.menu)
