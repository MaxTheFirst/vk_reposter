from config_reader import Config
from db import DBManager
from vk_poster import VkPoster

config = Config()

user_db = DBManager()

vk = VkPoster(config.vk_token, config.posts_limit)
