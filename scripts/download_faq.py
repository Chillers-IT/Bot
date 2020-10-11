"""Модуль для скачивания вопросов-ответов."""


import lxml.html
import requests
from fake_useragent import UserAgent


def download_ml():
    """Загружает FAQ по Machine Learning
    с https://machinelearningmastery.com/faq/.
    """

    ua_str = UserAgent().chrome
    url = 'https://machinelearningmastery.com/faq/'
    r = requests.get(url, headers={"User-Agent": ua_str})
    html_code = r.content
    tree = lxml.html.fromstring(html_code)
    el = tree.xpath("//div[@class='ufaq-faq-list']")
    print(el[0])



if __name__ == '__main__':
    download_ml()