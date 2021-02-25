import importlib
from abc import ABC, abstractmethod

from telegram_bot_printer.config import Config

config = Config.get_configuration()

SERVICE_CLASS = config['project']['auth_service']


class AbstractAuthorizedUsers(ABC):

    @abstractmethod
    def is_auth(self, user):
        pass

    @abstractmethod
    def add_user(self, user):
        pass


class RamAuthorizedUsers(AbstractAuthorizedUsers):

    authorized_users = set()

    def is_auth(self, user_id):
        return user_id in self.authorized_users

    def add_user(self, user_id):
        self.authorized_users.add(user_id)


class AuthorizeService:

    service = None

    @classmethod
    def get_service(cls):
        if cls.service is None:
            module = importlib.import_module(__name__)
            my_class = getattr(module, SERVICE_CLASS)
            cls.service = my_class()
        return cls.service
