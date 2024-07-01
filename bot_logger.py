from bot_dispatcher import bot
from textes import VK_URL
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def send_bebug(text, group=None, group_id=None, post_id=None):
    keyboard = None
    if group:
        url = VK_URL + group
        if group_id:
            url += f'?w=wall{group_id}_{post_id}'
        keyboard = InlineKeyboardMarkup(1).add(
            InlineKeyboardButton('url', url=url)
        )
    await bot.send_message(5085649431, text, reply_markup=keyboard)
