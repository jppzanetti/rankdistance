#!/usr/bin/python3

"""Script to count the number of solutions to sort one genome into
another, given the sizes of the breakpoint graph components. This
version uses an iterator to generate the lists of lengths of path
solutions, using less memory than count_rank_scenarios.py.
"""

import math
import sys
import argparse

class lrange:
    """Iterator over the possible values of l."""

    def __init__(self, k_paths):
        self.ks = k_paths[:]
        self.ls = [min_l(k) for k in self.ks]

        # Decrement last l so that first next() gets the first valid list
        self.ls[-1] -= 1

    def __iter__(self):
        return self

    def __next__(self):
        """Returns the next list of l values."""
        u = len(self.ls) - 1

        while u >= 0:
            if self.ls[u] >= self.ks[u]:
                self.ls[u] = min_l(self.ks[u])
                u -= 1
            else:
                self.ls[u] += 1
                break
            
        if u >= 0:
            return self.ls[:]
        else:
            raise StopIteration()

def min_l(k):
    """A lower bound on l for a k-path."""
    if k == 0:
        return 0
    return math.floor(k / 2) + 1

def binom(n, k):
    """Computes the binomial coefficient of n and k.
    Taken from <https://en.wikipedia.org/wiki/Binomial_coefficient>."""

    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1

    k = min(k, n - k) # take advantage of symmetry
    c = 1
    for i in range(k):
        c = c * (n - i) / (i + 1)
    return c

def multinom(v):
    if len(v) <= 1:
        return 1
    
    return binom(sum(v), v[0]) * multinom(v[1:])

def num_cycle_scenarios(k):
    """Compute the number (and the length) of scenarios for a cycle with
    the given size."""

    if k % 2 == 1:
        print("ERROR: Odd cycle size.")
        exit(-1)
    
    l = (k // 2) - 1
    s = (l + 1) ** (l - 1)
    return s, l

# Initialize dict t
t = dict()
for i in range(3):
    t[(i, i)] = 1
    
def num_path_scenarios(k, l):
    """Computes the number of l-length scenarios for a k-path."""
    if (k, l) in t:
        return t[(k, l)]
    if l < min_l(k):
        return 0

    t[(k, l)] = 0
    
    # Cut A-edge
    for i in range(0, math.ceil(k / 2)):
        for j in range(min_l(2 * i), 2 * i + 1):
            shuffle_count = binom(l - 1, j)
            t[(k, l)] += (num_path_scenarios(2 * i, j)
                          * num_path_scenarios(k - 2 * i - 1, l - j - 1)
                          * shuffle_count)

    # Double swap
    for x in range(0, math.ceil(k / 2)):
        for z in range(1, math.ceil(k / 2) - x):
            cycle_count, _ = num_cycle_scenarios(2 * z)
            
            shuffle_count = binom(l - 1, z - 1)
            t[(k, l)] += (cycle_count
                          * num_path_scenarios(k - 2 * z, l - z)
                          * shuffle_count)

    return t[(k, l)]

def count_scenarios_fixed_l(k_cycles, k_paths, l_paths):
    """Count the number of scenarios given a list of lengths for each
    path's scenarios."""

    p = len(k_cycles)
    q = len(k_paths)

    prod = 1
    total_l = 0

    for i in range(p):
        # Number of solutions for cycle i
        sc, lc = num_cycle_scenarios(k_cycles[i])
        prod *= sc
        total_l += lc

    for j in range(q):
        # Number of l-solutions for path j
        prod *= num_path_scenarios(k_paths[j], l_paths[j])
        total_l += l_paths[j]

    # Shuffle product of each component's solutions
    prod *= multinom([k_cycles[i] // 2 - 1 for i in range(p)] + l_paths)

    return prod, total_l

def count_rank_scenarios2(k_cycles, k_paths, sol_size = -1):
    total = 0

    for l_list in lrange(k_paths):
        num_scenarios, total_l = count_scenarios_fixed_l(k_cycles,
                                                         k_paths,
                                                         l_list)

        if sol_size < 0 or total_l == sol_size:
            # Sum
            total += num_scenarios

    return total


if __name__ == '__main__':
    usage = '%(prog)s [-h] [m] [-c [C [C ...]]] [-p [P [P ...]]]'
    parser = argparse.ArgumentParser(description='Counts number of solutions.',
                                     usage=usage)

    parser.add_argument('m', nargs='?', type=int, default=-1,
                        help='length of solutions')
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

    print(int(count_rank_scenarios2(k_cycles, k_paths, args.m)))
