"""Модуль для реализации обработки событий в заданном контексте бота."""

import os
from abc import ABC, abstractmethod

from sklearn import metrics

import chillerbot.intent as intent


class Handler(ABC):
    def __init__(self):
        self._handler = None
        self._classifierIntent = intent.ClassifierIntent()
        self._threshold = float(os.environ.get("THRESHOLD"))

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
        question = intent.clean_text(message)

        tf = self._classifierIntent.vectorizer.transform([question]).toarray()
        cos = 1 - metrics.pairwise_distances(self._classifierIntent.df_X, tf,
                                             metric='cosine')
        if cos.max() > self._threshold:
            index_value = cos.argmax()
            print(self._classifierIntent.df_X.head())
            return self._classifierIntent.FAQ['answers'].loc[cos.argmax()]
        else:
            return await super().handle(message)


class HandlerMock(Handler):
    async def handle(self, message: str):
        return 'Не знаю, что ответить.'
