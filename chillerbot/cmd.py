import inspect
import argparse
import os
from configparser import ConfigParser

from pandas import read_csv

from chillerbot.bot import BotHttp, BotVk
from chillerbot.exceptions import ConfigError
from chillerbot.constants import CONFIG_FILE, DEFAULT_CONFIG
from chillerbot.handlers import createHandler
from chillerbot.intent import buildModel


def getDataset():
    try:
        path = os.environ['PATH_DATASET']
        faq = read_csv(path)
    except KeyError:
        raise EnvironmentError("PATH_DATASET: path to dataset is not specified")
    except FileNotFoundError:
        raise FileNotFoundError("Dataset not found: {}".format(path))
    return faq


def fitModel():
    df = getDataset()
    model = buildModel()
    model.fit(df['questions'].to_numpy(), df['answers'].to_numpy())
    return model


def loadConfig():
    config = ConfigParser()

    home = os.path.expanduser('~')
    path = os.path.join(home, CONFIG_FILE)

    if os.path.exists(path):
        config.read(path)
    else:
        for k in DEFAULT_CONFIG.keys():
            config[k] = DEFAULT_CONFIG[k]
        with open(path, 'w') as file:
            config.write(file)

    return config


class Actions:
    @classmethod
    def getActions(cls):
        return dict(inspect.getmembers(cls, inspect.isfunction))

    @staticmethod
    def vk():
        model = fitModel()
        handler = createHandler(model)

        config = loadConfig()

        try:
            token = config['vk']['token']
        except KeyError:
            raise ConfigError("Doesn't found vk token")

        bot = BotVk(token)
        bot.setHandler(handler)
        bot.run()

    @staticmethod
    def http():
        model = fitModel()
        handler = createHandler(model)

        bot = BotHttp()
        bot.setHandler(handler)
        bot.run()


def createParser(actions):
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=Actions.getActions().keys())
    return p
