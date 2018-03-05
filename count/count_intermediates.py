#!/usr/bin/python3

from math import factorial, ceil, floor

def cycle_intermediates(k):
    """Number of intermediates for a k-cycle."""
    x = k / 2
    return int(factorial(k) / (factorial(x) * factorial(x) * (x + 1)))

def path_intermediates(k):
    """Number of intermediates for a k-path."""
    v = k + 1
    return int(factorial(v) / factorial(floor(v / 2)) / factorial(ceil(v / 2)))

def count_intermediates(cycles = [], paths = []):
    """Computes the number of intermediates of a genome."""
    total = 1

    for p in paths:
        total *= path_intermediates(p)
    for c in cycles:
        total *= cycle_intermediates(c)

    return total

if __name__ == '__main__':
    print(count_intermediates(paths = [6]))
    print(count_intermediates(cycles = [6]))
