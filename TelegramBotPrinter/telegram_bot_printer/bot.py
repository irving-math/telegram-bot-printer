import logging
from abc import abstractmethod, ABCMeta
from typing import List, Type

from telegram.update import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters

log = logging.getLogger(__name__)


class BotAction(metaclass=ABCMeta):
    def __init__(self, update: Update = None, context: CallbackContext = None):
        self.update = update
        self.context = context

    def send_message(self, message: str):
        log.debug('Sending message "{}"'.format(message))
        self.update.message.reply_text(message)

    @abstractmethod
    def action(self):
        pass


class BotCommand(BotAction, metaclass=ABCMeta):
    @property
    @abstractmethod
    def command_name(self) -> str:
        pass

    @property
    @abstractmethod
    def pass_args(self) -> bool:
        pass


class BotMessageTrigger(BotAction, metaclass=ABCMeta):
    @property
    @abstractmethod
    def filter(self) -> filters:
        pass


class TelegramBotConfig:
    def __init__(
        self,
        commands: List[Type[BotCommand]],
        message_triggers: List[Type[BotMessageTrigger]],
        token_bot: str,
    ):
        self.commands = commands
        self.token_bot = token_bot
        self.message_triggers = message_triggers


class TelegramBot:
    def __init__(self, bot_config: TelegramBotConfig):
        self.bot_config = bot_config
        self.updater = Updater(self.bot_config.token_bot, use_context=True)

    def register_commands(self):
        dp = self.updater.dispatcher
        for command in self.bot_config.commands:
            action_name = command().command_name
            dp.add_handler(
                CommandHandler(
                    action_name, self.create_fn(command), pass_args=command().pass_args
                )
            )

    @staticmethod
    def create_fn(command):
        def inner_function(updater, context):
            try:
                command(updater, context).action()
            except:
                log.exception("An error occurred when executed command.")

        return inner_function

    def register_message_triggers(self):
        dp = self.updater.dispatcher
        for trigger in self.bot_config.message_triggers:
            filter_trigger = trigger().filter
            dp.add_handler(MessageHandler(filter_trigger, self.create_fn(trigger)))

    def init(self):
        self.register_commands()
        self.register_message_triggers()
        self.updater.start_polling()
