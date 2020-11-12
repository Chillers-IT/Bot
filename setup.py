from setuptools import setup
from setuptools.command import install, develop


class PostInstallCommand(install):
    def run(self):
        import nltk
        install.run(self)
        nltk.download('stopwords')


class PostDevelopCommand(develop):
    def run(self):
        import nltk
        develop.run(self)
        nltk.download('stopwords')


setup(name='chillerbot',
      version='0.1',
      packages=['chillerbot'],
      install_requires=['vkbottle', 'aiohttp', 'nltk', 'scikit-learn',
                        'pandas', 'pymorphy2'],
      cmd_class={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand
      })
