from bot_dispatcher import dp
from vk_loop import vk_loop
from bot_logger import send_bebug
from handlers import *
from loguru import logger
import asyncio


def main():
    logger.disable("vkbottle")
    loop = asyncio.get_event_loop()
    loop.create_task(send_bebug('------\nSTART\n-----'))
    loop.create_task(dp.start_polling())
    loop.create_task(vk_loop())
    loop.run_forever()


if __name__ == '__main__':
    main()
