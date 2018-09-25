# -*- coding: utf-8 -*-
"""
__author__ = z0305
__date__ = 08/26/2018
"""

from sklearn.datasets import load_iris
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score

iris = load_iris()
clf = AdaBoostClassifier(n_estimators=100)
""" 参数介绍: 
"""
scores = cross_val_score(clf, iris.data, iris.target)
print(scores.mean())
