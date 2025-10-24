from itertools import combinations
from typing import List, Tuple


def brute_force(number: int, capacity: int, weight_cost: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
    """Brute force method for solving knapsack problem

    :param number: number of existing items
    :param capacity: the capacity of knapsack
    :param weight_cost: list of tuples like: [(weight, cost), (weight, cost), ...]
    :return: tuple like: (best cost, best combination list(contains 1 and 0))
    """
    best_cost = 0  # Initialize to 0 to handle empty knapsack case
    best_combination = [0] * number

    # generating combinations by all ways: C by 1 from n, C by 2 from n, ...
    for way in range(number):
        for comb in combinations(weight_cost, way + 1):
            weight = sum([wc[0] for wc in comb])
            cost = sum([wc[1] for wc in comb])
            if best_cost < cost and weight <= capacity:
                best_cost = cost
                best_combination = [0] * number
                for wc in comb:
                    best_combination[weight_cost.index(wc)] = 1
    return best_cost, best_combination
