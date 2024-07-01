from peewee import *

db = SqliteDatabase('db/users_data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Settings(BaseModel):
    chat_id = IntegerField(default=0)
    group_id = IntegerField(default=0)
    flag = BooleanField(default=True)

    class Meta:
        db_table = 'settings'


class Chat(BaseModel):
    id = IntegerField(default=0)
    domain = CharField()
    last_post_id = IntegerField(default=0)
    key_words = TextField(True)
    stop_words = TextField(True)

    class Meta:
        db_table = 'chats'
