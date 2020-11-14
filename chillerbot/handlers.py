"""Модуль для реализации обработки событий в заданном контексте бота."""

from abc import ABC, abstractmethod
from collections.abc import Callable

from sklearn.pipeline import Pipeline

from chillerbot.constants import THRESHOLD


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
    def __init__(self, classifier: Pipeline,
                 predicate: Callable = lambda x: True):
        super().__init__()
        self._model = classifier
        self._predicate = predicate

    async def handle(self, message: str):
        proba, reply = self._model.predict([message])

        if self._predicate(proba):
            return reply
        else:
            return await super().handle(message)


class HandlerMock(Handler):
    async def handle(self, message: str):
        return 'Не знаю, что ответить.'


def createHandler(model):
    handler = HandlerFaq(model, lambda proba: 1 - proba > THRESHOLD)
    handler.set_next(HandlerMock())
    return handler
