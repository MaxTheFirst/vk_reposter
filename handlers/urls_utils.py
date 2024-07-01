from dispatcher import vk, user_db
from aiogram.types import Message, CallbackQuery
from asyncio import sleep
import textes
import keyboards


async def parse_vk_urls(text: str, is_one):
    urls = text.split(',')
    groups = {}
    for url in urls:
        if textes.VK_URL in url:
            if url[-1] == '/':
                url = url[:-1]
            domain = url.split('/')[-1]
            id = await vk.get_owner_id(domain)
            await sleep(3)
            if id:
                groups[id] = domain
                continue
        return url, False
    if is_one:
        return id, True
    return groups, True


async def read_vk_urls(message: Message, is_one=False):
    groups, flag = await parse_vk_urls(message.text, is_one)
    if flag:
        return groups
    await message.answer(groups + textes.GROUP_ERROR)
    return None


async def read_urls_in_db(message: Message):
    groups = await read_vk_urls(message)
    if groups:
        ids = [i.id for i in user_db.groups]
        for i in groups:
            if i not in ids:
                text = textes.VK_URL + groups[i] + textes.GROUP_NO
                await message.answer(text, reply_markup=keyboards.menu)
                return None
    return groups


def get_text_li(text, mid_text, args):
    for key, val in enumerate(args):
        text += '\n' + str(key+1) + mid_text + val
    return text


async def give_urls_text(text_begin, callback: CallbackQuery):
    groups = user_db.groups
    if groups.count() == 0:
        await callback.message.edit_text(textes.DEL_NO, reply_markup=keyboards.menu)
        return None
    domains = [group.domain for group in groups]
    return get_text_li(text_begin, '. ' + textes.VK_URL, domains)
