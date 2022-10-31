import math
import string
from collections import Counter


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.word_count = Counter({})
        self.class_count = {}

    def clean(self, s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator).lower().split()

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        self.class_count = dict.fromkeys(set(y), 0)
        words_length = 0
        for i in range(len(X)):
            title, label = X[i], y[i]
            words_title = self.clean(title)
            for word in words_title:
                self.class_count[label] += 1
                if word not in self.word_count:
                    words_length += 1
                    self.word_count[word] = Counter(dict.fromkeys(set(y), 0))
                self.word_count[word][label] += 1

        for i in self.word_count:
            for j in self.word_count[i]:
                self.word_count[i][j] = (self.word_count[i][j] + self.alpha) / (
                    self.class_count[j] + self.alpha * words_length
                )

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        predicted_label = []
        for x in X:
            words = self.clean(x)
            max_rating = float("-inf")
            expected_label = 0
            for label in self.class_count:
                title_rating = sum(
                    [
                        math.log(self.word_count[wrd][label]) if self.word_count[wrd] else 0
                        for wrd in words
                    ]
                )
                if title_rating > max_rating:
                    max_rating = title_rating
                    expected_label = label
            if max_rating == 0:
                expected_label = "Maybe"
            predicted_label.append(expected_label)
        return predicted_label
