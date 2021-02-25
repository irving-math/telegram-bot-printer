import importlib
import logging
import os
import tempfile
from abc import ABC, abstractmethod

from telegram_bot_printer.config import Config

log = logging.getLogger(__name__)
config = Config.get_configuration()
CLASS_SERVICE = config["project"]["printer_service"]
USER = config['project']['user_lp']


class Document:
    def __init__(self, path):
        self.path = path

    @classmethod
    def from_bytes(cls, bytes_object: bytes):
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.write(bytes_object)
        tf.close()
        document = Document(tf.name)
        document.path = tf.name


class PrinterService:
    service = None

    @classmethod
    def get_service(cls, printer_name=None):
        if cls.service is None:
            module = importlib.import_module(__name__)
            my_class = getattr(module, CLASS_SERVICE)
            cls.service = my_class(printer_name)
        return cls.service


class AbstractPrinter(ABC):
    def __init__(self, printer_name=None):
        self.printer_name = printer_name

    @abstractmethod
    def print(self, document: Document):
        pass


class LPPrinter(AbstractPrinter):
    def print(self, document: Document):
        log.info("Printing file: {}".format(document.path))
        if self.printer_name is not None:
            os.system("lpr -U {} {} {}".format(USER, self.printer_name, document.path))
        else:
            os.system("lpr -U {} {}".format(USER, document.path))
        log.info("Printing Done!")


class MockPrinter(AbstractPrinter):
    def print(self, document: Document):
        log.info("Printing file... Done!")
