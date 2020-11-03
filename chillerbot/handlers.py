"""Модуль для реализации обработки событий в заданном контексте бота."""

from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self):
        self._handler = None

    async def __call__(self, message: str):
        return await self.handle(message)

    def set_next(self, handler):
        self._handler = handler
        return handler

    @abstractmethod
    async def handle(self, message: str):
        if self._handler is not None:
            return await self._handler.handle(message)

        return None


class HandlerFaq(Handler):
    async def handle(self, message: str):
        if message == 'привет':
            return u'ну здаров'
        else:
            return await super().handle(message)


class HandlerMock(Handler):
    async def handle(self, message: str):
        return 'Не знаю, что ответить.'
