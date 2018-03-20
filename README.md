# rankdistance

This repository contains methods and scripts for the rank distance model of genome rearrangement. They are implemented in Python 3.

## Counting

### Counting co-optimal sorting scenarios

There are two Python files with code for counting scenarios: `count/count_rank_scenarios.py` and `count/count_rank_scenarios2.py`. We will describe the usage of `count_rank_scenarios.py` only, because `count_rank_scenarios2.py` is similar in usage, its difference is that it tries to use less memory.

To count the number of scenarios between two genomes A and B, the only data we need is the size and type of each component in the breakpoint graph of A and B.

To use as a script:

```
$ ./count_rank_scenarios.py -h
$ ./count_rank_scenarios.py [m] [-c C C ...] [-p P P ...]
```

Examples:

```
$ ./count_rank_scenarios.py -c 6 -p 6
7635
$ ./count_rank_scenarios.py 8 -c 6 -p 6
5124
```

To use in Python code:

```py
from count_rank_scenarios import count_rank_scenarios

count_rank_scenarios(k_cycles, k_paths, sol_size = -1)
```

Examples:

```py
from count_rank_scenarios import count_rank_scenarios

count_rank_scenarios([6], [6]) # 7635
count_rank_scenarios([6], [6], sol_size = 8) # 5124
```

### Counting intermediate genomes

The number of intermediate genomes is computed using `count/count_intermediates.py`. As in the preceding section, the input data is the size and type of each component in the breakpoint graph of A and B.

To use as a script:

```
$ ./count_intermediates.py -h
```

```
$ ./count_intermediates.py [-c C C ...] [-p P P ...]
```

Example:

```
$ ./count_intermediates.py -c 6 -p 6
175
```

To use in Python code:

```py
from count_intermediates import count_intermediates

count_intermediates(cycles = [], paths = [])
```

Example:

```py
from count_intermediates import count_intermediates

count_intermediates(cycles = [6], paths = [6]) # 175
```

### Experiments

The file `count/experiments.py` is the script used to run the experiments in the paper.

To show the usage message:

```
$ ./experiments.py -h
```

To run the script:

```
$ ./experiments.py [--print {long,sci,table}] [--dist] [--scenarios] [--inter] filename
```

The arguments `--dist, -d`, `--scenarios, -s`, and `--inter, -i` toggle the computation of the distance between the genomes, the number of scenarios, and the number of intermediates, respectively.

The argument `--print` defines the printing format. The default `long` prints the numbers in decimal notation. The `sci` option prints the numbers in scientific notation. The `table` option prints the numbers in scientific notation, and prints the results for each instance in the format of a LaTeX table.

The input file format is a simplified version of the [GRIMM input file](http://grimm.ucsd.edu/GRIMM/grimm_instr.html). Each genome starts with a line '>name', and every subsequent line is a chromosome. A chromosome is a sequence of markers, separated by spaces. If a marker is reversed, it is preceded by a minus sign. If the chromosome ends with a '@', it is circular, and if it ends with a '$' it is linear. An example of an input file:

```
>A
1 2 3 4 5 $
>B
2 3 $
1 -5 -4 $
```

Is this example, genome A has one linear chromosome with 5 markers, and genome B has two linear chromosomes, with two and three markers.

## References

Zanetti, Joao Paulo Pereira, and Joao Meidanis. "Counting sorting scenarios and intermediate genomes for the rank distance". To be submitted.

Zanetti, Joao Paulo Pereira, Priscila Biller, and Joao Meidanis. "Median approximations for genomes modeled as matrices." Bulletin of Mathematical Biology 78, no. 4 (2016): 786-814.

Meidanis, Joao, Priscila Biller, and Joao Paulo Pereira Zanetti. "A Matrix-Based Theory for Genome Rearrangements." Technical Report IC-17-11. Institute of Computing, Unicamp, Brazil. August 2017. Available at http://www.ic.unicamp.br/~reltech/2017/17-11.pdf.
