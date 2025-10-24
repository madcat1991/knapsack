# Knapsack Problem Solver

A comprehensive Python 3 implementation of multiple algorithms for solving the 0/1 knapsack problem.

## Overview

This project implements 6 different algorithms for solving the classic 0/1 knapsack optimization problem:

- **Brute Force** - Exhaustive search through all possible combinations
- **Greedy (Cost/Weight Ratio)** - Heuristic approach selecting items by best value-to-weight ratio
- **Dynamic Programming** - Optimal solution using memoization
- **Branch and Bound** - Optimized search with pruning
- **FPTAS** - Fully Polynomial-Time Approximation Scheme
- **Simulated Annealing** - Metaheuristic optimization approach

## Requirements

- Python 3.7 or higher
- No external dependencies required

## Installation

1. Clone or download this repository
2. No additional installation steps required - all dependencies are built into Python

## Usage

### Basic Usage

```bash
python3 knapsack_problem_solver.py -f <input_file> -o <output_file> -m <method>
```

### Command Line Arguments

- `-f, --inst-file`: Path to input instance file (required)
- `-o, --output`: Path to output solution file (default: `output.sol.dat`)
- `-m, --method`: Algorithm to use (default: `brute`)
- `-r, --repeat`: Number of repetitions for timing (default: 1)
- `-s, --scaling-factor`: Scaling factor for FPTAS (default: 4.0)
- `-t, --temperature`: Initial temperature for simulated annealing (default: 100)
- `-n, --steps`: Number of steps for simulated annealing (default: 100)

### Available Methods

- `brute` - Brute force (exhaustive search)
- `ratio` - Greedy ratio method
- `dynamic` - Dynamic programming
- `bandb` - Branch and bound
- `fptas` - FPTAS approximation
- `sa` - Simulated annealing

### Examples

```bash
# Solve using dynamic programming
python3 knapsack_problem_solver.py -f inst/knap_10.inst.dat -o solution.sol.dat -m dynamic

# Run FPTAS with custom scaling factor
python3 knapsack_problem_solver.py -f inst/knap_20.inst.dat -m fptas -s 2.0

# Test simulated annealing with custom parameters
python3 knapsack_problem_solver.py -f inst/knap_15.inst.dat -m sa -t 200 -n 50

# Run multiple repetitions for timing analysis
python3 knapsack_problem_solver.py -f inst/knap_25.inst.dat -m dynamic -r 10
```

## Input Format

Instance files (`.inst.dat`) contain one problem per line with the format:
```
<instance_id> <number_of_items> <capacity> <weight1> <cost1> <weight2> <cost2> ...
```

Example:
```
9000 4 100 18 114 42 136 88 192 3 223
```

## Output Format

Solution files (`.sol.dat`) contain one solution per line with the format:
```
<instance_id> <number_of_items> <best_cost> <item1_selected> <item2_selected> ...
```

Where `item_selected` is 1 if the item is included in the knapsack, 0 otherwise.

Example:
```
9000 4 473  1 1 0 1
```

## Algorithm Details

### Brute Force
- **Time Complexity**: O(2^n)
- **Space Complexity**: O(n)
- **Optimality**: Guaranteed optimal
- **Best for**: Small problems (n ≤ 20)

### Dynamic Programming
- **Time Complexity**: O(nW) where W is capacity
- **Space Complexity**: O(nW)
- **Optimality**: Guaranteed optimal
- **Best for**: Medium problems with reasonable capacity

### Branch and Bound
- **Time Complexity**: O(2^n) worst case, much better in practice
- **Space Complexity**: O(n)
- **Optimality**: Guaranteed optimal
- **Best for**: Medium to large problems where DP is too memory-intensive

### Greedy (Ratio)
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Optimality**: Approximation (not guaranteed optimal)
- **Best for**: Quick approximate solutions

### FPTAS
- **Time Complexity**: O(n^3/ε) where ε is approximation factor
- **Space Complexity**: O(n^2/ε)
- **Optimality**: (1-ε) approximation
- **Best for**: Large problems requiring near-optimal solutions

### Simulated Annealing
- **Time Complexity**: O(iterations × n)
- **Space Complexity**: O(n)
- **Optimality**: Heuristic (no optimality guarantee)
- **Best for**: Very large problems or when other methods are too slow

## Test Data

The `inst/` directory contains test instances of varying sizes:
- `knap_4.inst.dat` - 4 items (for testing)
- `knap_10.inst.dat` - 10 items
- `knap_15.inst.dat` - 15 items
- `knap_20.inst.dat` - 20 items
- `knap_25.inst.dat` - 25 items
- `knap_30.inst.dat` - 30 items
- `knap_32.inst.dat` - 32 items
- `knap_35.inst.dat` - 35 items
- `knap_37.inst.dat` - 37 items
- `knap_40.inst.dat` - 40 items

The `sol/` directory contains the corresponding optimal solutions for verification.

## Performance Comparison

For the provided test instances, typical performance characteristics:

| Algorithm | knap_10 | knap_20 | knap_30 | knap_40 |
|-----------|---------|---------|---------|---------|
| Brute Force | ~0.001s | ~0.1s | ~10s | >100s |
| Dynamic Programming | ~0.001s | ~0.001s | ~0.001s | ~0.001s |
| Branch and Bound | ~0.001s | ~0.01s | ~0.1s | ~1s |
| Greedy | ~0.0001s | ~0.0001s | ~0.0001s | ~0.0001s |
| FPTAS | ~0.001s | ~0.001s | ~0.001s | ~0.001s |
| Simulated Annealing | ~0.01s | ~0.01s | ~0.01s | ~0.01s |

*Times are approximate and may vary based on system and problem characteristics.*

## Development

### Code Structure

- `knapsack_problem_solver.py` - Main entry point and command-line interface
- `brute_force.py` - Brute force implementation
- `dynamic_programming.py` - Dynamic programming with memoization
- `branch_bounds.py` - Branch and bound algorithm
- `ratio_greedy.py` - Greedy ratio algorithm
- `fptas.py` - FPTAS approximation algorithm
- `sa.py` - Simulated annealing implementation
- `decorators.py` - Memoization decorator for dynamic programming

### Type Hints

All functions include comprehensive type hints for better code maintainability and IDE support.

### Error Handling

The solver includes robust error handling for:
- Invalid input file formats
- Malformed data lines
- File I/O errors
- Invalid algorithm parameters

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please ensure:
- Code follows Python 3 standards
- Type hints are included for all functions
- Error handling is comprehensive
- Performance is optimized where possible
