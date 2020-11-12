import os

from pandas import read_csv

from chillerbot.handlers import HandlerFaq, HandlerMock
from chillerbot.bot import BotHttp, BotVk
from chillerbot.intent import buildModel
from chillerbot.constants import THRESHOLD


def getDataset():
    try:
        path = os.environ['PATH_DATASET']
        faq = read_csv(path)
    except KeyError:
        raise EnvironmentError("PATH_DATASET: path to dataset is not specified")
    except FileNotFoundError:
        raise FileNotFoundError("Dataset not found: {}".format(path))
    return faq


if __name__ == '__main__':
    df = getDataset()
    model = buildModel()
    model.fit(df['questions'].to_numpy(), df['answers'].to_numpy())

    handler = HandlerFaq(model, lambda proba: 1 - proba > THRESHOLD)
    handler.set_next(HandlerMock())
    # bot = BotVk('48d58aaf62f57f5a6738b1b81b7663694369c27b7d2eb4d90db67b3b1fd547781aa3db065a7f2ab380a68',
    #             handler)
    # bot.run()
    bot = BotHttp()
    bot.setHandler(handler)
    bot.run()
