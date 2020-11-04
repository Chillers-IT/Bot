"""Модуль для реализации бота."""

from abc import ABC, abstractmethod

import vkbottle
from aiohttp import web

from chillerbot.handlers import Handler, HandlerMock


class Bot(ABC):
    """Основной класс бота.

    Args:
        handler (Handler): обработчик сообщений.
    """

    def __init__(self, handler: Handler = HandlerMock()):
        self._handler = handler
        self._rule_handlers = dict()

    def setHandler(self, handler: Handler):
        self._handler = handler

    def on(self, text):
        def func(rule_func):
            self._rule_handlers[text] = rule_func
            return rule_func
        return func

    async def process(self, message: str):
        if message in self._rule_handlers:
            return await self._rule_handlers[message](message)
        return await self._handler.handle(message)

    @abstractmethod
    def run(self):
        pass


class BotHttp(Bot):
    """Реализация бота для протокола Http.

    Args:
        handler (Handler): обработчик сообщений.
    """

    def __init__(self, handler: Handler = HandlerMock()):
        Bot.__init__(self, handler)
        self._app = web.Application()
        self._app.router.add_route("POST", "/", self.executor)

    async def executor(self, request: web.Request):
        text = await request.text()
        answer = await self.process(text)
        return web.Response(text=answer)

    def run(self):
        """Запускает сервер http для обработки запросов."""

        web.run_app(app=self._app)


class BotVk(Bot):
    def __init__(self, token: str, handler: Handler = HandlerMock()):
        Bot.__init__(self, handler)
        self._vk_bot = vkbottle.Bot(token)
        self._vk_bot.on.message_handler.add_handler(self.wrapper, lower=True)

    async def wrapper(self, ans: vkbottle.Message):
        return await self.process(ans.text)

    def run(self):
        self._vk_bot.run_polling(skip_updates=False)
