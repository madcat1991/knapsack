#coding: utf-8


def ratio_greedy(number, capacity, weight_cost):
    """Greedy 1/0 ratio method for solving knapsack problem

    :param number: number of existing items
    :param capacity: the capacity of knapsack
    :param weight_cost: list of tuples like: [(weight, cost), (weight, cost), ...]
    :return: tuple like: (best cost, best combination list(contains 1 and 0))
    """
    ratios = [(index, item[1] / float(item[0])) for index, item in enumerate(weight_cost)]
    ratios = sorted(ratios, key=lambda x: x[1], reverse=True)
    best_combination = [0] * number
    best_cost = 0
    weight = 0
    for index, ratio in ratios:
        if weight_cost[index][0] + weight <= capacity:
            weight += weight_cost[index][0]
            best_cost += weight_cost[index][1]
            best_combination[index] = 1
    return best_cost, best_combination
