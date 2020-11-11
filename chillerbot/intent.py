"""Модуль для определения контекста общения с пользователем."""
import os
import re

import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class Lemmatizer(BaseEstimator, TransformerMixin):
    def __init__(self, this=True):
        self.this = this
        self.morph = pymorphy2.MorphAnalyzer()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self._clean_text(X)

    def _clean_text(self, text, stop_word=stopwords.words('russian')):
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


class ClassifierIntent:
    def __init__(self):
        try:
            path = os.environ['PATH_DATASET']
            self.FAQ = pd.read_csv(path)
        except KeyError:
            raise EnvironmentError("PATH_DATASET: path to dataset is not specified")
        except FileNotFoundError:
            raise FileNotFoundError("Dataset not found: {}".format(path))

        self.lemmatizer = Lemmatizer()

        transform_pipeline1 = Pipeline([
            ('first step', self.lemmatizer),
            ])

        # print(self.FAQ['questions'])
        transform_pipeline1.transform(self.FAQ['questions'])
        # print(self.FAQ['questions'])

        # self.FAQ['questions'] = self.FAQ['questions'].apply(self.lemmatizer.transform)
        self.vectorizer = TfidfVectorizer()
        vectorized_questions = self.vectorizer.\
            fit_transform(self.FAQ['questions']).toarray()
        self.df_X = pd.DataFrame(vectorized_questions,
                                 columns=self.vectorizer.get_feature_names())