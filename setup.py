from setuptools import setup
from setuptools.command.install import install
import atexit


def _post_install():
    import nltk
    nltk.download('stopwords')


class Install(install):
    def __init__(self, *args, **kwargs):
        super(Install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


setup(name='chillerbot',
      version='0.1',
      packages=['chillerbot'],
      install_requires=['vkbottle', 'aiohttp', 'nltk', 'scikit-learn',
                        'pandas', 'pymorphy2'],
      entry_points={
          'console_scripts': ['chillerbot=chillerbot.__main__:main'],
      })
