from chillerbot.handlers import HandlerFaq, HandlerMock
from chillerbot.bot import BotHttp, BotVk


if __name__ == '__main__':
    handler = HandlerFaq()
    handler.set_next(HandlerMock())
    # bot = BotVk('48d58aaf62f57f5a6738b1b81b7663694369c27b7d2eb4d90db67b3b1fd547781aa3db065a7f2ab380a68',
    #             handler)
    # bot.run()
    bot = BotHttp()
    bot.setHandler(handler)
    bot.run()
