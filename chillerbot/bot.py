"""Модуль для реализации бота и API."""

from abc import ABC


class Bot:
    def process_message(self):
        pass


class CommandBot(ABC):
    def __init__(self, bot):
        self._bot = bot

    def receive(self):
        pass

    def send(self):
        pass


class CommandVk(CommandBot):
    pass
