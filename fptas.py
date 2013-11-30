#coding: utf-8
from dynamic_programming import dynamic_programming


def FPTAS(number, capacity, weight_cost, scaling_factor=4):
    """Fully polynomial-time approximation scheme method for solving knapsack problem

    :param number: number of existing items
    :param capacity: the capacity of knapsack
    :param weight_cost: list of tuples like: [(weight, cost), (weight, cost), ...]
    :param scaling_factor: how much we want to be precise, bigger factor means coarser solution
    :return: tuple like: (best cost, best combination list(contains 1 and 0))
    """
    new_capacity = int(float(capacity) / scaling_factor)
    new_weight_cost = [(round(float(weight) / scaling_factor) + 1, cost) for weight, cost in weight_cost]
    return dynamic_programming(number, new_capacity, new_weight_cost)
