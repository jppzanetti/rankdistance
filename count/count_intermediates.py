#!/usr/bin/python3

from math import factorial, ceil, floor
import sys
import argparse

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
    parser = argparse.ArgumentParser(description='Counts number of intermediates.')

    parser.add_argument('-c', nargs='*', type=int, default=[],
                        help='list of lengths of cycles')
    parser.add_argument('-p', nargs='*', type=int, default=[],
                        help='list of lengths of paths')

    if len(sys.argv) == 1:
        args = parser.parse_args('-h'.split())
    else:
        args = parser.parse_args()

        k_cycles = []
    for k in args.c:
        if k < 0:
            print("ERROR: Negative cycle size.")
            exit(-1)
        if k == 0:
            print("ERROR: Null cycle size.")
            exit(-1)
        if k % 2 == 1:
            print("ERROR: Odd cycle size.")
            exit(-1)
        if k > 2:
            k_cycles.append(k)

    k_paths = []
    for k in args.p:
        if k < 0:
            print("ERROR: Negative path length.")
            exit(-1)
        if k > 0:
            k_paths.append(k)

    print(count_intermediates(cycles = k_cycles, paths = k_paths))
