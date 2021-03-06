# Copyright (C) 2017-2019 Intel Corporation
#
# SPDX-License-Identifier: MIT

import argparse
from bench import parse_args, time_mean_min, print_header, print_row
import numpy as np
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser(description='scikit-learn linear regression '
                                             'benchmark')
parser.add_argument('--no-fit-intercept', dest='fit_intercept', default=True,
                    action='store_false',
                    help="Don't fit intercept (assume data already centered)")
params = parse_args(parser, size=(1000000, 50), dtypes=('f8', 'f4'),
                    loop_types=('fit', 'predict'))

# Generate random data
X = np.random.rand(*params.shape).astype(params.dtype)
Xp = np.random.rand(*params.shape).astype(params.dtype)
y = np.random.rand(*params.shape).astype(params.dtype)

# Create our regression object
regr = LinearRegression(fit_intercept=params.fit_intercept,
                        n_jobs=params.n_jobs)

columns = ('batch', 'arch', 'prefix', 'function', 'threads', 'dtype', 'size',
           'time')
print_header(columns, params)

# Time fit
fit_time, _ = time_mean_min(regr.fit, X, y,
                            outer_loops=params.fit_outer_loops,
                            inner_loops=params.fit_inner_loops)
print_row(columns, params, function='Linear.fit', time=fit_time)

# Time predict
predict_time, yp = time_mean_min(regr.predict, Xp,
                                 outer_loops=params.predict_outer_loops,
                                 inner_loops=params.predict_inner_loops)
print_row(columns, params, function='Linear.predict', time=predict_time)
