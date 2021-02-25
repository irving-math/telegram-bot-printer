import pathlib

import telegram
from telegram.ext import filters, Filters

from telegram_bot_printer.authorization_service import AuthorizeService
from telegram_bot_printer.bot import (
    BotCommand,
    BotMessageTrigger,
    TelegramBotConfig,
)
from telegram_bot_printer.config import Config
from telegram_bot_printer.log_config import *
from telegram_bot_printer.printer import PrinterService, Document

log = logging.getLogger(__name__)
config = Config.get_configuration()

CONFIG_NAMESPACE = "printer_bot"
DOWNLOADING_FILE_MESSAGE = config[CONFIG_NAMESPACE]["dowloading_file_message"]
PATH_FILES = config[CONFIG_NAMESPACE]["path_documents"]
PRINTED_FILE_MESSAGE = config[CONFIG_NAMESPACE]["file_printed_message"]
TOKEN_BOT = config[CONFIG_NAMESPACE]["token_bot"]
START_MESSAGE = config[CONFIG_NAMESPACE]["start_message"]
ALREADY_AUTH_MESSAGE = config[CONFIG_NAMESPACE]["auth_message_already_auth"]
PASSWORD = config[CONFIG_NAMESPACE]["password_bot"]
AUTH_OK_MESSAGE = config[CONFIG_NAMESPACE]["auth_message_auth_ok"]
PASS_WRONG_MESSAGE = config[CONFIG_NAMESPACE]["auth_message_pass_wrong"]
NOT_AUTHENTICATED_MESSAGE = config[CONFIG_NAMESPACE]["not_authentified_message"]
FILE_IS_BIG_MESSAGE = config[CONFIG_NAMESPACE]["file_is_big"]
FILE_SIZE_LIMIT = config[CONFIG_NAMESPACE]["file_size_limit"]


class StartCommand(BotCommand):
    def action(self):
        log.debug("User started conversation.")
        self.send_message(START_MESSAGE)

    @property
    def command_name(self):
        return "start"

    @property
    def pass_args(self):
        return False


class AuthCommand(BotCommand):
    def action(self):
        password_of_user = "".join(self.context.args)
        auth_service = AuthorizeService.get_service()
        chat_id = self.update.message.chat_id

        if auth_service.is_auth(chat_id):
            self.send_message(ALREADY_AUTH_MESSAGE)
            return
        password = PASSWORD
        if password == password_of_user:
            auth_service.add_user(chat_id)
            self.send_message(AUTH_OK_MESSAGE)
        else:
            self.send_message(PASS_WRONG_MESSAGE)

    @property
    def command_name(self):
        return "auth"

    @property
    def pass_args(self):
        return True


class PrintTrigger(BotMessageTrigger):
    @property
    def filter(self) -> telegram.ext.filters.Filters:
        return Filters.document

    def action(self, *args, **kwargs):
        chat_id = self.update.message.chat_id
        auth_service = AuthorizeService.get_service()
        if not auth_service.is_auth(chat_id):
            log.debug("User chat_id: {} not authenticated".format(chat_id))
            self.send_message(NOT_AUTHENTICATED_MESSAGE)
            return
        file_path = self.download_file()
        printer_service = PrinterService.get_service()
        document = Document(file_path)
        printer_service.print(document)
        self.send_message(PRINTED_FILE_MESSAGE)

    def download_file(self):
        file_id = self.update.message.document.file_id
        file_size = self.update.message.document.file_size
        original_file_name = self.update.message.document.file_name
        if file_size > FILE_SIZE_LIMIT:
            self.send_message(FILE_IS_BIG_MESSAGE)
            return
        self.send_message(DOWNLOADING_FILE_MESSAGE)
        file_path = self.get_file_path(self.update.message.document)
        new_file = self.context.bot.get_file(file_id)
        log.debug("Downloading file name: {}, saved in: {}".format(original_file_name, file_path))
        new_file.download(str(file_path))
        log.debug("File name: {}, is downloaded".format(file_path))
        return file_path

    @staticmethod
    def get_file_path(document):
        file_name = document.file_name
        current_path = pathlib.Path("__file__").parent.absolute()
        current_path_python = pathlib.Path(current_path)
        file_path = current_path_python / PATH_FILES / 'file_to_print{}.{}'.format(document.file_id, file_name[-3:])
        return file_path.resolve()


printer_bot_config = TelegramBotConfig(
    commands=[StartCommand, AuthCommand],
    message_triggers=[PrintTrigger],
    token_bot=TOKEN_BOT,
)

