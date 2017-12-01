"""Test for miscellaneous samplers objects."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

import pytest

from scipy import sparse

from sklearn.datasets import load_iris
from sklearn.utils.testing import assert_array_equal

from imblearn.datasets import make_imbalance
from imblearn.misc import FunctionSampler
from imblearn.under_sampling import RandomUnderSampler

iris = load_iris()
X, y = make_imbalance(iris.data, iris.target, ratio={0: 10, 1: 25},
                      random_state=0)


@pytest.mark.parametrize("X,y", [(X, y),
                                 (sparse.csr_matrix(X), y),
                                 (sparse.csc_matrix(X), y)])
def test_function_sampler_identity(X, y):
    sampler = FunctionSampler()
    X_res, y_res = sampler.fit_sample(X, y)
    if sparse.issparse(X):
        X = X.toarray()
        X_res = X_res.toarray()
    assert_array_equal(X_res, X)
    assert_array_equal(y_res, y)


@pytest.mark.parametrize("X,y", [(X, y),
                                 (sparse.csr_matrix(X), y),
                                 (sparse.csc_matrix(X), y)])
def test_function_sampler_func(X, y):

    def func(X, y):
        return X[:10], y[:10]

    sampler = FunctionSampler(func=func)
    X_res, y_res = sampler.fit_sample(X, y)
    if sparse.issparse(X):
        X = X.toarray()
        X_res = X_res.toarray()
    assert_array_equal(X_res, X[:10])
    assert_array_equal(y_res, y[:10])


@pytest.mark.parametrize("X,y", [(X, y),
                                 (sparse.csr_matrix(X), y),
                                 (sparse.csc_matrix(X), y)])
def test_function_sampler_func_kwargs(X, y):

    def func(X, y, ratio, random_state):
        rus = RandomUnderSampler(ratio=ratio, random_state=random_state)
        return rus.fit_sample(X, y)

    sampler = FunctionSampler(func=func, kw_args={'ratio': 'auto',
                                                  'random_state': 0})
    X_res, y_res = sampler.fit_sample(X, y)
    X_res_2, y_res_2 = RandomUnderSampler(random_state=0).fit_sample(X, y)
    if sparse.issparse(X):
        X = X.toarray()
        X_res = X_res.toarray()
        X_res_2 = X_res_2.toarray()
    assert_array_equal(X_res, X_res_2)
    assert_array_equal(y_res, y_res_2)
