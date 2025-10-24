import argparse
from functools import partial
from time import time
from typing import List, Tuple, Callable, Any

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


def parse_line(line: str) -> Tuple[int, int, int, List[Tuple[int, int]]]:
    """Line parser method
    :param line: line from input file
    :return: tuple like: (instance id, number of items, knapsack capacity,
                            list of tuples like: [(weight, cost), (weight, cost), ...])
    :raises ValueError: if line format is invalid
    """
    try:
        parts = [int(value) for value in line.split()]
        if len(parts) < 3:
            raise ValueError("Line must contain at least 3 values (id, number, capacity)")

        inst_id, number, capacity = parts[0:3]

        if number < 0:
            raise ValueError("Number of items cannot be negative")
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")

        # Check if we have the right number of weight-cost pairs
        if len(parts) != 3 + 2 * number:
            raise ValueError(f"Expected {3 + 2 * number} values, got {len(parts)}")

        weight_cost = [(parts[i], parts[i + 1]) for i in range(3, len(parts), 2)]

        # Validate weight-cost pairs
        for i, (weight, cost) in enumerate(weight_cost):
            if weight < 0:
                raise ValueError(f"Weight {i} cannot be negative")
            if cost < 0:
                raise ValueError(f"Cost {i} cannot be negative")

        return inst_id, number, capacity, weight_cost
    except ValueError as e:
        raise ValueError(f"Invalid line format: {e}")


def solver(method: Callable[[int, int, List[Tuple[int, int]]], Tuple[int, List[int]]],
           inst_file_path: str, solution_file_path: str) -> None:
    """Main method that solves knapsack problem using one of the existing methods

    :param method: knapsack problem solving method
    :param inst_file_path: path to file with input instances
    :param solution_file_path: path to file where solver should write output data
    :raises FileNotFoundError: if input file doesn't exist
    :raises ValueError: if input data is invalid
    """
    try:
        with open(inst_file_path, "r") as inst_file, open(solution_file_path, "w") as sol_file:
            for line_num, line in enumerate(inst_file, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    inst_id, number, capacity, weight_cost = parse_line(line)
                    # get best cost and variables combination
                    best_cost, best_combination = method(number, capacity, weight_cost)
                    best_combination_str = " ".join(str(i) for i in best_combination)
                    # write best result to file
                    sol_file.write(f"{inst_id} {number} {best_cost}  {best_combination_str}\n")
                except (ValueError, IndexError) as e:
                    raise ValueError(f"Invalid data in line {line_num}: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {inst_file_path}")

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

    print(f"Average solving time: {solving_time / args.repeat}s (repetitions count {args.repeat})")
