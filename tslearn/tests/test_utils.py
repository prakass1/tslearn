import numpy as np
import pickle

import tslearn.utils

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def test_arraylike_copy():
    X_npy = np.array([1, 2, 3])
    np.testing.assert_allclose(tslearn.utils._arraylike_copy(X_npy), X_npy)
    np.testing.assert_allclose(tslearn.utils._arraylike_copy(X_npy) is X_npy,
                               False)


def test_save_load():
    n, sz, d = 15, 10, 3
    rng = np.random.RandomState(0)
    dataset = rng.randn(n, sz, d)
    tslearn.utils.save_timeseries_txt("tmp-tslearn-test.txt", dataset)
    reloaded_dataset = tslearn.utils.load_timeseries_txt(
        "tmp-tslearn-test.txt")
    np.testing.assert_allclose(dataset, reloaded_dataset)

    dataset = tslearn.utils.to_time_series_dataset([[1, 2, 3, 4], [1, 2, 3]])
    tslearn.utils.save_timeseries_txt("tmp-tslearn-test.txt", dataset)
    reloaded_dataset = tslearn.utils.load_timeseries_txt(
        "tmp-tslearn-test.txt")
    for ts0, ts1 in zip(dataset, reloaded_dataset):
        np.testing.assert_allclose(ts0[:tslearn.utils.ts_size(ts0)],
                                   ts1[:tslearn.utils.ts_size(ts1)])


def test_label_categorizer():
    y = np.array([-1, 2, 1, 1, 2])
    lc = tslearn.utils.LabelCategorizer()
    lc.fit(y)

    s = pickle.dumps(lc)
    lc2 = pickle.loads(s)
    y_tr = lc2.inverse_transform([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    ref = np.array([1., 2., -1.])

    np.testing.assert_allclose(ref, y_tr)
