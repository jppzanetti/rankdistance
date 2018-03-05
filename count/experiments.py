#!/usr/bin/python3

import re
import sys
from count_rank_scenarios import count_rank_scenarios
from count_intermediates import count_intermediates
import argparse

class Graph:
    """Class that represents graphs using a dict of lists."""

    def __init__(self):
        """Returns an empty graph."""
        self.edge = dict()

    def add_node(self, v):
        """Adds one vertice v to the graph, disconnected from others."""
        if v not in self.edge:
            self.edge[v] = []        

    def add_edge(self, x, y):
        """Adds one edge (x, y) to the graph."""
        if x not in self.edge:
            self.edge[x] = []
        self.edge[x].append(y)
        
        if y not in self.edge:
            self.edge[y] = []
        self.edge[y].append(x)

    def __str__(self):
        graph_str = ''
        for v in self.edge:
            graph_str += str(v) + ' ' + str(self.edge[v]) + '\n'
        return graph_str

class Genome(Graph):
    """Extends Graph to represent a genome."""

    def __init__(self, source_str):
        """Reads a genome from a string in a simplified GRIMM format."""

        super().__init__()

        for line in source_str.splitlines():
            if line[0] == '>':
                self.name = line[1:].strip()
            elif line[0] != '#':
                self._add_chromosome(line)

    def _add_chromosome(self, chr):
        """Takes one line of the simplified GRIMM file and adds the chromosome to the genome"""

        # Stores the last extremity read
        prev = None

        # Stores the first extremity
        first = None

        for symb in chr.strip().split():
            match = re.match(r'^(?P<sign>[+-]?)(?P<gene>[0-9a-zA-Z_-]+)$', symb)
            
            if match:
                sign = match.group('sign')
                gene = match.group('gene')

                # Gene extremities
                first_ext = gene + '_t'
                last_ext = gene + '_h'

                # Reversed gene
                if sign == '-':
                    tmp = first_ext
                    first_ext = last_ext
                    last_ext = tmp

                # Add the adjacency if possible
                if prev:
                    self.add_edge(prev, first_ext)
                else:
                    first = first_ext

                # Update last extremity
                prev = last_ext

            elif symb == '$':
                # End of linear chromosome
                self.add_node(first)
                self.add_node(prev)

            elif symb == '@':
                # Close circular chromosome
                self.add_edge(first, prev)

class BreakpointGraph(Graph):
    """Breakpoint graph, uncolored."""
    
    def __init__(self, g1, g2):
        """Returns a breakpoint graph of g1 and g2."""
        super().__init__()

        for v in g1.edge:
            self.add_node(v)
            for u in g1.edge[v]:
                if u > v:
                    self.add_edge(u, v)
        for v in g2.edge:
            self.add_node(v)
            for u in g2.edge[v]:
                if u > v:
                    self.add_edge(u, v)

    def components(self):
        """Executes a DFS and returns a list of the connected components."""
        component_list = []
        not_visited = set(self.edge.keys())

        stack = []

        while not_visited:
            # Get a not visited node
            v = not_visited.pop()

            # Put it back in not_visited
            # Yes, it's a hack
            not_visited.add(v)

            stack.append(v)
            component = []
            while stack:
                v = stack.pop()
                if v in not_visited:
                    # Visit node
                    not_visited.remove(v)
                    component.append(v)

                    # Add neighbours to stack
                    for u in self.edge[v]:
                        stack.append(u)

            component_list.append(list(component))

        return component_list

    def cycles_and_paths(self, big = True):
        """Returns two lists: one of the lengths of the cycles in the graph,
           and another for the paths. If big is true, only counts big components."""
        cycle_lengths = []
        path_lengths = []

        components = self.components()
        for component in components:
            # Single node is small component
            if big and len(component) == 1:
                continue

            # Path
            if True in [len(self.edge[v]) <= 1 for v in component]:
                path_lengths.append(len(component) - 1)

            # Cycle
            else:
                # 2-cycle is also a small component
                if (not big) or (len(component) > 2):
                    cycle_lengths.append(len(component))

        return cycle_lengths, path_lengths

    def distance(self):
        """The distance between g1 and g2."""
        n = len(self.edge.keys())
        cycles, paths = self.cycles_and_paths(big = False)
        return n - 2 * len(cycles) - len(paths)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs experiments on the given file.')
    parser.add_argument('filename', type=str, help='input file')
    parser.add_argument('--print', dest='print_mode', choices=['long', 'sci', 'table'], default='long', help='how to print the results, default is long')
    parser.add_argument('--dist', '-d', action='store_true', help='computes the distance')
    parser.add_argument('--scenarios', '-s', action='store_true', help='computes the number of scenarios')
    parser.add_argument('--inter', '-i', action='store_true', help='computes the number of intermediates')

        
    args = parser.parse_args()

    # Read genomes
    genomes = []

    with open(args.filename, 'r') as grimm_file:
        genome_str = ''
        for line in grimm_file:
            if not line.strip():
                continue
            if genome_str and line[0] == '>':
                genomes.append(Genome(genome_str))
                genome_str = ''
            genome_str += line
        genomes.append(Genome(genome_str))

    # Compute pairwise results
    for i in range(len(genomes)):
        for j in range(i + 1, len(genomes)):
            bg = BreakpointGraph(genomes[i], genomes[j])
            k_cycles, k_paths = bg.cycles_and_paths()

            separator = '\n'
            eol = ''
            long_format = '{:d}'
            if args.print_mode == 'sci':
                long_format = '{:.2e}'
            if args.print_mode == 'table':
                separator = ' & '
                eol = '\\\\'
                long_format = '${:.2e}$'

            results = []
            results.append(genomes[i].name.split()[0])
            results.append(genomes[j].name.split()[0])

            if args.dist:
                results.append('{:d}'.format(bg.distance()))
                
            if args.scenarios:
                results.append(long_format.format(count_rank_scenarios(k_cycles, k_paths)))
                
            if args.inter:
                results.append(long_format.format(count_intermediates(k_cycles, k_paths)))

            print(separator.join(results) + eol)
            
