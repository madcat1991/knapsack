#coding: utf-8
import argparse
from functools import partial
from time import time

from branch_bounds import branch_and_bounds
from brute_force import brute_force
from dynamic_programming import dynamic_programming
from fptas import FPTAS
from sa import annealing_algorithm
from ratio_greedy import ratio_greedy

BRUTE_FORCE_METHOD = "brute"
RATIO_GREEDY_METHOD = "ratio"
DYNAMIC_PROGRAMMING_METHOD = "dynamic"
BRANCH_AND_BOUNDS_METHOD = "bandb"
FPTAS_METHOD = "fptas"
GENETIC_METHOD = "sa"


def parse_line(line):
    """Line parser method
    :param line: line from input file
    :return: tuple like: (instance id, number of items, knapsack capacity,
                            list of tuples like: [(weight, cost), (weight, cost), ...])
    """
    parts = [int(value) for value in line.split()]
    inst_id, number, capacity = parts[0:3]
    weight_cost = [(parts[i], parts[i + 1]) for i in range(3, len(parts), 2)]
    return inst_id, number, capacity, weight_cost


def solver(method, inst_file_path, solution_file_path):
    """Main method that solves knapsack problem using one of the existing methods

    :param method: knapsack problem solving method
    :param inst_file_path: path to file with input instances
    :param solution_file_path: path to file where solver should write output data
    """
    inst_file = open(inst_file_path, "r")
    sol_file = open(solution_file_path, "w")

    for line in inst_file:
        inst_id, number, capacity, weight_cost = parse_line(line)
        # get best cost and variables combination
        best_cost, best_combination = method(number, capacity, weight_cost)
        best_combination_str = " ".join("%s" % i for i in best_combination)
        # write best result to file
        sol_file.write("%s %s %s  %s\n" % (inst_id, number, best_cost, best_combination_str))

    inst_file.close()
    sol_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script solving the 0/1 knapsack problem')
    parser.add_argument('-f', '--inst-file', required=True, type=str, dest="inst_file_path", 
                        help='Path to inst *.dat file')
    parser.add_argument('-o', type=str, dest="solution_file_path", default="output.sol.dat",
                        help='Path to file where solutions will be saved. Default value: output.sol.dat')
    parser.add_argument('-r', type=int, dest="repeat", default=1,
                        help='Number of repetitions. Default value: 1')
    parser.add_argument("-m", default=BRUTE_FORCE_METHOD, type=str, dest="method",
                        choices=[BRUTE_FORCE_METHOD, RATIO_GREEDY_METHOD, DYNAMIC_PROGRAMMING_METHOD,
                                 BRANCH_AND_BOUNDS_METHOD, FPTAS_METHOD, GENETIC_METHOD],
                        help="Solving method. Default value: brute force method")
    parser.add_argument('-s', type=float, dest="scaling_factor", default=4.0,
                        help='Scaling factor for FPTAS algorithm. Default value: 4.0')
    parser.add_argument('-t', type=int, dest="temperature", default=100,
                        help='Initial temperature for annealing approach. Default value: 100')
    parser.add_argument('-n', type=int, dest="steps", default=100,
                        help='Number of steps for annealing approach iteration. Default value: 100')
    args = parser.parse_args()

    # selecting knapsack problem solving method
    if args.method == BRUTE_FORCE_METHOD:
        method = brute_force
    elif args.method == RATIO_GREEDY_METHOD:
        method = ratio_greedy
    elif args.method == DYNAMIC_PROGRAMMING_METHOD:
        method = dynamic_programming
    elif args.method == BRANCH_AND_BOUNDS_METHOD:
        method = branch_and_bounds
    elif args.method == FPTAS_METHOD:
        if args.scaling_factor <= 1:
            raise Exception("Scaling factor for FPTAS must be greater than 1")
        method = partial(FPTAS, scaling_factor=args.scaling_factor)
    elif args.method == GENETIC_METHOD:
        if args.temperature < 1:
            raise Exception("Initial temperature for annealing approach must be greater than 0")
        if args.steps < 1:
            raise Exception("Number of steps for annealing approach iteration must be greater than 0")
        method = partial(annealing_algorithm, init_temp=args.temperature, steps=args.steps)
    else:
        raise Exception("Unknown solving method")

    solving_time = 0
    # repeating "repeat" time to get average solving time
    for i in range(args.repeat):
        t_start = time()
        solver(method, args.inst_file_path, args.solution_file_path)
        t_finish = time()
        solving_time += (t_finish - t_start)

    print "Average solving time: %ss (repetitions count %s)" % (solving_time / args.repeat, args.repeat)