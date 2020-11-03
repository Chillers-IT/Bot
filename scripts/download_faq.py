"""Модуль для скачивания вопросов-ответов."""


import lxml.html
import requests
from fake_useragent import UserAgent
import pandas as pd


def download_ml():
    """Загружает FAQ по Machine Learning
    с https://machinelearningmastery.com/faq/.
    """

    ua_str = UserAgent().firefox
    url = 'https://machinelearningmastery.com/faq/'
    r = requests.get(url, headers={"User-Agent": ua_str})
    html_code = r.content
    tree = lxml.html.fromstring(html_code)
    questions = tree.xpath("//div[@class='ufaq-faq-title ufaq-faq-toggle']")
    answers = tree.xpath("//div[@class='ewd-ufaq-post-margin ufaq-faq-post']")
    return questions, answers


def toDataset(q, a, path):
    """Создание csv из FAQ.

    Args:
        q (list): вопросы из FAQ.
        a (list): ответы из FAQ.
        path (str): путь для csv.
    """

    col1 = [''.join(i.itertext()) for i in q]
    col2 = [''.join(i.itertext()) for i in a]
    df = pd.DataFrame(data={'questions': col1, 'answers': col2})
    df.to_csv(path, index=False)


if __name__ == '__main__':
    q, a = download_ml()
    toDataset(q, a, '../datasets/example.csv')



