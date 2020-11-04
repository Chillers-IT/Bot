"""Модуль для определения контекста общения с пользователем."""
import os
import re

import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

morph = pymorphy2.MorphAnalyzer()


def clean_text(text: str, stop_word=stopwords.words('russian')
                                    + stopwords.words('english')):
    """
    Обработка теста для последующего сравнения.

    Происходит приведение к единому регистру, лемматизация слов и
    удаление стоп слов.

    Args:
        text: текст для нормализации.
        stop_word: список стоп слов. По умалчанию использует nltk.stopwords

    Returns:

    """
    text = text.split(' ')
    text_normalize = []
    for word in text:
        text_normalize.append(morph.parse(word)[0])
    for item in stop_word:
        try:
            text.remove(item)
        except ValueError:
            pass

    x = ' '.join(text).lower()
    return re.sub(r'[^a-z0-9а-я\s]', '', x)


class ClassifierIntent:
    """Классификация контекста."""

    def __init__(self):
        self.FAQ = pd.read_csv(os.getenv('PATH_DATASET'))
        self.FAQ['questions'] = self.FAQ['questions'].apply(clean_text)
        self.vectorizer = TfidfVectorizer()
        vectorized_questions = self.vectorizer.\
            fit_transform(self.FAQ['questions']).toarray()
        self.df_X = pd.DataFrame(vectorized_questions,
                                 columns=self.vectorizer.get_feature_names())

    def __call__(self, *args, **kwargs):
        return self.df_X
