knapsack
========

Implementation of several algorithms for solving 1/0 knapsack problem on Python.

Here are implemented 5 algorithms:
* brute force
* cost/weight ratio greedy
* branches and bounds
* dynamic programming
* FPTAS (fully polynomial-time approximation scheme)
* simulated annealing

The main file is: knapsack\_problem\_solver.py

The *inst* directory contains data for experiments. The *sol* directory contains right answers for experiments checking.

Format of instance files:
* ID
* the number of items
* the knapsack capacity
* sequence of weight-cost pairs

Format of solution files:
* ID
* the number of items
* the best cost value
* sequence of 0/1: if the i-th element of sequence equal to 1 then we take the i-th item to knapsack overwise we don't take the item to knapsack
