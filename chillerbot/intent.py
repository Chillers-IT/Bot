"""Модуль для определения контекста общения с пользователем."""

from typing import Optional, Union
import re

import pymorphy2
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.pipeline import Pipeline
from scipy.spatial import KDTree
import numpy as np


class Lemmatizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.morph: pymorphy2.MorphAnalyzer = pymorphy2.MorphAnalyzer()

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([self._clean_text(x) for x in X])

    def _clean_text(self, text: str, stop_word: list=stopwords.words('russian')):
        """
        Обработка теста для последующей векторизации.

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
            text_normalize.append(self.morph.parse(word)[0])
        for item in stop_word:
            try:
                text.remove(item)
            except ValueError:
                pass

        x = ' '.join(text).lower()
        return re.sub(r'[^a-z0-9а-я\s]', '', x)


class ClassifierIntent(BaseEstimator, ClassifierMixin):
    def __init__(self):
        super().__init__()
        self._tree: Optional[KDTree] = None
        self._y: Union[list, np.ndarray, None] = None

    def fit(self, X, y=None):
        # TODO: Может не совпасть тип.
        X = X.toarray()

        self._tree = KDTree(X)
        self._y = y
        return self

    def predict(self, X):
        if self._tree is None:
            raise NotFittedError()

        # TODO: Может не совпасть тип.
        X = X.toarray()

        proba, index = self._tree.query(X)
        return proba[0], self._y[index[0]]


def buildModel():
    return Pipeline([('t1', Lemmatizer()),
                     ('t2', TfidfVectorizer()),
                     ('cls', ClassifierIntent())])
