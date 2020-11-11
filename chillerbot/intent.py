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
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def fit(self, X):
        return self

    def transform(self, X):
        return [self._clean_text(x) for x in X]

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
            FAQ = pd.read_csv(path)
        except KeyError:
            raise EnvironmentError("PATH_DATASET: path to dataset is not specified")
        except FileNotFoundError:
            raise FileNotFoundError("Dataset not found: {}".format(path))

        vectorizer = TfidfVectorizer()
        self.transform_pipeline1 = Pipeline([
                ('clean text', Lemmatizer()),
                ('tf-idf', vectorizer),
            ])

        vectorized_questions = self.transform_pipeline1\
            .fit(FAQ['questions']).transform(FAQ['questions'])

        self.df_X = pd.DataFrame(vectorized_questions.toarray(),
                                 columns=vectorizer.get_feature_names())

        self.answers = FAQ['answers']
