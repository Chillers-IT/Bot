"""Модуль для реализации обработки событий в заданном контексте бота."""

import os
from abc import ABC, abstractmethod

from sklearn import metrics

import chillerbot.intent as intent
import chillerbot.constants as constants


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
    def __init__(self):
        super().__init__()
        self._classifierIntent = intent.ClassifierIntent()
        self._threshold = constants.THRESHOLD

    async def handle(self, message: str):
        question = self._classifierIntent.transform_pipeline1\
                       .transform([message]).toarray()

        cos = 1 - metrics.pairwise_distances(self._classifierIntent.df_X,
                                             question,
                                             metric='cosine')
        if cos.max() > self._threshold:
            index_value = cos.argmax()
            return self._classifierIntent.answers.loc[cos.argmax()]
        else:
            return await super().handle(message)


class HandlerMock(Handler):
    async def handle(self, message: str):
        return 'Не знаю, что ответить.'
