from .models import *


class DBManager():
    def __init__(self):
        db.create_tables([Settings, Chat])
        settings = Settings.select()
        if settings.count() == 0:
            self.settings = Settings.create()
        else:
            self.settings = settings[0]

    @property
    def admin_id(self):
        return self.settings.chat_id

    @admin_id.setter
    def admin_id(self, chat_id):
        self.settings.chat_id = chat_id
        self.settings.save()

    @property
    def group_id(self):
        return self.settings.group_id

    @group_id.setter
    def group_id(self, group_id):
        self.settings.group_id = group_id
        self.settings.save()

    @staticmethod
    def add_groups(ids: dict):
        groups_last = Chat.select()
        groups_last = [group.id for group in groups_last]
        data = [
            {'id': id, 'domain': ids[id]}
            for id in ids if ids not in groups_last
        ]
        Chat.insert_many(data).execute()

    @staticmethod
    def update_last_post(owner_id, last_post_id):
        Chat.update(last_post_id=last_post_id).where(
            Chat.id == owner_id).execute()

    @staticmethod
    def get_chat(owner_id) -> Chat:
        return Chat.get(Chat.id == owner_id)

    @staticmethod
    def delete_chat(owner_ids):
        for owner_id in owner_ids:
            DBManager.get_chat(owner_id).delete_instance()

    @property
    def groups(self) -> list[Chat]:
        return Chat.select()

    @staticmethod
    def get_words(owner_id=None, chat=None, is_key=True, is_all=False):
        if not chat:
            chat = DBManager.get_chat(owner_id)
        if is_all:
            return chat.key_words, chat.stop_words
        if is_key:
            words = chat.key_words
        else:
            words = chat.stop_words
        if not words:
            return []
        return words.split(',')

    @staticmethod
    def check_words(chat, words, is_key, is_append):
        last_words = DBManager.get_words(chat=chat, is_key=is_key)
        new_words = [word.strip() for word in words if word and (
            word in last_words) == (not is_append)]
        if is_append:
            return last_words + new_words
        return [word for word in last_words if word not in new_words]

    @staticmethod
    def update_words(owner_id, words, is_key=True, is_append=True):
        chat = DBManager.get_chat(owner_id)
        words = DBManager.check_words(chat, words, is_key, is_append)
        if words or not is_append:
            words = ','.join(words)
            if is_key:
                index = 'key_words'
            else:
                index = 'stop_words'
            Chat.update(**{index: words}).where(Chat.id == owner_id).execute()
