"""Analyse persistent homology statistics wrt. their expressivity."""

import argparse

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import euclidean_distances


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('INPUT')

    args = parser.parse_args()

    df = pd.read_csv(args.INPUT, index_col='file')

    X = []

    for name, df_ in df.groupby('name'):
        # This can be seen as an equivalent to the Betti number
        # calculation.
        feature_vector = df_.sort_values(by='dimension')['n_features'].values

        X.append(feature_vector)

    X = np.asarray(X)
    D = euclidean_distances(X)
    n = len(X)

    # Number of graph pairs with equal feature vectors, not accounting
    # for the diagonal because every graph is equal to itself.
    n_equal_pairs = (np.triu(D == 0).sum()) - n
    fraction_equal_pairs = n_equal_pairs / (n * (n - 1) // 2)

    print(
        f'{n} graphs, {n_equal_pairs} / {n * (n - 1) // 2:d} pairs '
        f'({100 * fraction_equal_pairs:.2f}%)'
    )
