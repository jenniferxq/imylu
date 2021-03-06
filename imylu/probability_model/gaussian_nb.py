# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2018-07-06 21:13:34
@Last Modified by: tushushu
@Last Modified time: 2018-07-06 21:13:34
"""

from math import pi, exp, sqrt
from collections import Counter


class GaussianNB(object):
    """GaussianNB class support multiple classification.

    Attributes:
        prior: Prior probability.
        avgs: Means of each column and class. e.g. [[0.5, 0.6], [0.2, 0.1]]
        variances: Variances of each column and class.
        n_class: number of classes
    """

    def __init__(self):
        self.prior = None
        self.avgs = None
        self.variances = None
        self.n_class = None

    def _get_prior(self, y):
        """Calculate prior probability.

        Arguments:
            y {list} -- 1d list object with int

        Returns:
            dict -- {y_0: P(y_0), y_1: P(y_1)...y_n: P(y_n)]
        """

        return Counter(y)

    def _get_posterior(self, xij, avg, variance):
        """Calculate posterior probability

        Arguments:
            xij {float}
            avg {float} -- Mean of column of Xj
            variance {float} -- Variance of column of Xj

        Returns:
            float -- P(y_1)
        """

        return 1 / sqrt(2 * pi * variance) * \
            exp(-(xij - avg)**2 / (2 * variance))

    def _get_avg_var(self, X, y, n_class):
        """Calculate the variance and mean of each column of X

        Arguments:
            X {list} -- 2D list with int or float
            y {list} -- 1d list object with int
            n_class {int} -- Number of classes of y

        Returns:
            tuple -- avgs, variances of each column and each class.
        """

        avgs = []
        variances = []
        # Get the shape of X
        m = len(X[0])
        n = len(X)
        for j in range(m):
            # Initialize sum(x) and sum(x ** 2) for column j
            feature_sum = [0] * n_class
            feature_sqr_sum = [0] * n_class
            for i in range(n):
                feature_sum[y[i]] += X[i][j]
                feature_sqr_sum[y[i]] += X[i][j] ** 2
            feature_avg = [x / n for x in feature_sum]
            # D(X) = E{[X-E(X)]^2} = E(X^2)-[E(X)]^2
            feature_var = [x / n - y ** 2 for x,
                           y in zip(feature_sqr_sum, feature_avg)]
            avgs.append(feature_avg)
            variances.append(feature_var)
        return avgs, variances

    def fit(self, X, y):
        """Build a Gauss naive bayes classifier.

        Arguments:
            X {list} -- 2d list with int or float
            y {list} -- 1d list object with int 0 or 1
        """

        # Calculate prior probability.
        self.prior = self._get_prior(y)
        # Count number of classes
        self.n_class = len(self.prior)
        # Calculate the variance and mean of each column of X
        self.avgs, self.variances = self._get_avg_var(X, y, self.n_class)

    def _predict_prob(self, row):
        """Auxiliary function of predict_prob.

        Arguments:
            row {list} -- 1D list with int or float

        Returns:
            float -- probabilities. e.g. [0.02, 0.03, 0.02]
        """

        # Initialize probabilities
        probs = [1] * self.n_class
        # Caculate the joint probabilities of each feature and each class.
        for xij, avgs, variances in zip(row, self.avgs, self.variances):
            probs = [prob * self._get_posterior(xij, avg, var)
                     for prob, avg, var in zip(probs, avgs, variances)]
        # Scale the probabilities
        probs_sum = sum(probs)
        return [prob / probs_sum for prob in probs]

    def predict_prob(self, X):
        """Get the probability that y is positive.

        Arguments:
            X {list} -- 2d list object with int or float

        Returns:
            list -- 1d list object with float
        """

        return [self._predict_prob(row) for row in X]

    def predict(self, X, threshold=0.5):
        """Get the prediction of y.

        Arguments:
            X {list} -- 2d list object with int or float

        Keyword Arguments:
            threshold {float} -- Prediction = 1 when probability >= threshold
            (default: {0.5})

        Returns:
            list -- 1d list object with float
        """

        # Choose the class which has the maximum probability
        return [max(enumerate(y), key=lambda x: x[1])[0]
                for y in self.predict_prob(X)]
