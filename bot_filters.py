from dispatcher import user_db
from aiogram import filters, types


class IsConfigChat(filters.BoundFilter):
    key = 'config_chat'

    def __init__(self, config_chat):
        self.config_chat = config_chat

    async def check(self, message: types.Message) -> bool:
        return (message.chat.id == user_db.admin_id) == self.config_chat


class CallbackCmd(filters.BoundFilter):
    key = 'callback_cmd'

    def __init__(self, callback_cmd):
        if not isinstance(callback_cmd, list):
            callback_cmd = [callback_cmd]
        self.callback_cmd = callback_cmd

    async def check(self, callback: types.CallbackQuery):
        if callback.data:
            args = callback.data.split('_')
            if args[0] in self.callback_cmd:
                if len(args) > 1:
                    return {'args': args[1::]}
                else:
                    return True
        return False
