from textes import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_btn = InlineKeyboardButton(MENU, callback_data=MENU_CMD)
menu = InlineKeyboardMarkup(1).add(menu_btn)

commands = InlineKeyboardMarkup().add(
    InlineKeyboardButton(MAIN_GROUP, callback_data=MAIN_GROUP_CMD)
).add(
    InlineKeyboardButton(ADD_GROUPS, callback_data=ADD_GROUPS_CMD)
).add(
    InlineKeyboardButton(DEL_GROUPS, callback_data=DEL_GROUPS_CMD)
).add(
    InlineKeyboardButton(ADD_WORD, callback_data=ADD_WORD_CMD)
).add(
    InlineKeyboardButton(ADD_STOP_WORD, callback_data=ADD_STOP_WORD_CMD)
).add(
    InlineKeyboardButton(DEL_WORD, callback_data=DEL_WORD_CMD)
).add(
    InlineKeyboardButton(DEL_STOP_WORD, callback_data=DEL_STOP_WORD_CMD)
)
