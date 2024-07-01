from .words_steps import text_steps
from .urls_utils import *
from bot_dispatcher import dp
from dispatcher import user_db
from db import DBManager
from states import UserStates
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import textes
import keyboards


@dp.callback_query_handler(callback_cmd=textes.UPDATE_CMD, state=UserStates.menu)
async def read_update_cmd(callback: CallbackQuery, state: FSMContext, args):
    mode = int(args[0])
    await state.update_data(mode=mode)
    await state.set_state(UserStates.read_url)
    text = await give_urls_text(
        text_begin=text_steps[mode][0],
        callback=callback
    )
    await callback.message.edit_text(text, reply_markup=keyboards.menu)


@dp.message_handler(state=UserStates.read_url)
async def read_update(message: Message, state: FSMContext):
    groups = await read_urls_in_db(message)
    if groups:
        group_id = list(groups.keys())[0]
        mode = (await state.get_data())['mode']
        await state.update_data(group=group_id)
        if mode < 2:
            text = text_steps[mode][1]
        else:
            is_key = (mode in [0, 2])
            words = user_db.get_words(group_id, is_key=is_key)
            if not words:
                await message.answer(textes.NO_WORD, reply_markup=keyboards.menu)
                return
            text = get_text_li(text_steps[mode][1], '. ', words)
        await state.set_state(UserStates.read_text)
        await message.answer(text, reply_markup=keyboards.menu)


@dp.message_handler(state=UserStates.read_text)
async def read_update(message: Message, state: FSMContext):
    if message.text:
        data = await state.get_data()
        mode = data['mode']
        group_id = data['group']
        words = message.text.split(',')
        is_key = (mode in [0, 2])
        is_append = (mode < 2)
        user_db.update_words(group_id, words, is_key, is_append)
        await message.answer(text_steps[mode][2], reply_markup=keyboards.menu)
