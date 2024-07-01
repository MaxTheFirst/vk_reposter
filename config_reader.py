from configparser import ConfigParser


CONFIG_FILE = 'config.ini'


class Config():
    def __init__(self) -> None:
        config = ConfigParser()
        config.read(CONFIG_FILE)
        self.tg_token = config['telegram']['token']
        self.password = config['telegram']['password']
        self.vk_token = config['vk']['access_token']
        self.posts_limit = config['vk']['posts_limit']
        self.timeout = int(config['vk']['timeout'])
        self.timeout_post = int(config['vk']['timeout_post'])
        self.restart_time = int(config['vk']['restart_time'])
