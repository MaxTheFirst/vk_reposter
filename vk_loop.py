from dispatcher import config, user_db, vk
from bot_logger import send_bebug
from asyncio import sleep


def word_in(words, text):
    for word in words:
        if word in text:
            return True
    return False


def check_post(text, key_words, stop_words):
    flag_key = True
    flag_stop = True
    if key_words:
        flag_key = word_in(key_words.split(','), text)
    if stop_words:
        flag_stop = not word_in(stop_words.split(','), text)
    return flag_key and flag_stop


async def vk_loop():
    while True:
        groups = user_db.groups
        if user_db.group_id != 0 and len(groups) > 0:
            for group in groups:
                try:
                    postes = await vk.get_posts(group.id, group.last_post_id)
                    if postes:
                        user_db.update_last_post(group.id, postes[-1][0])
                        debug_text = f'Сохранение {group.domain} пост {postes[-1][0]}. Ключевые слова: {group.key_words}. Стоп-слова: {group.stop_words}.'
                        await send_bebug(debug_text, group.domain, group.id, postes[-1][0])
                    for post, text in postes:
                        if check_post(text, group.key_words, group.stop_words):
                            await vk.repost(
                                owner_id=group.id,
                                post_id=post,
                                to_id=user_db.group_id
                            )
                            await send_bebug(f'Постинг {group.domain} пост {post}.', group.domain, group.id, post)
                            await sleep(config.timeout_post)
                except Exception:
                    pass
                await sleep(config.timeout)
        await sleep(config.timeout)
