#coding: utf-8
from collections import deque


class SimpleQueue(object):
    def __init__(self):
        self.buffer = deque()

    def push(self, value):
        self.buffer.appendleft(value)

    def pop(self):
        return self.buffer.pop()

    def __len__(self):
        return len(self.buffer)


class Node(object):
    def __init__(self, level, selected_items, cost, weight, bound):
        self.level = level
        self.selected_items = selected_items
        self.cost = cost
        self.weight = weight
        self.bound = bound


def branch_and_bounds(number, capacity, weight_cost):
    """Branch and bounds method for solving knapsack problem
    http://faculty.cns.uni.edu/~east/teaching/153/branch_bound/knapsack/overview_algorithm.html

    :param number: number of existing items
    :param capacity: the capacity of knapsack
    :param weight_cost: list of tuples like: [(weight, cost), (weight, cost), ...]
    :return: tuple like: (best cost, best combination list(contains 1 and 0))
    """
    priority_queue = SimpleQueue()

    #sort items in non-increasing order by benefit/cost
    ratios = [(index, item[1] / float(item[0])) for index, item in enumerate(weight_cost)]
    ratios = sorted(ratios, key=lambda x: x[1], reverse=True)

    best_so_far = Node(0, [], 0.0, 0.0, 0.0)
    a_node = Node(0, [], 0.0, 0.0, calculate_bound(best_so_far, number, capacity, weight_cost, ratios))
    priority_queue.push(a_node)

    while len(priority_queue) > 0:
        curr_node = priority_queue.pop()
        if curr_node.bound > best_so_far.cost:
            curr_node_index = ratios[curr_node.level][0]
            next_item_cost = weight_cost[curr_node_index][1]
            next_item_weight = weight_cost[curr_node_index][0]
            next_added = Node(
                curr_node.level + 1,
                curr_node.selected_items + [curr_node_index],
                curr_node.cost + next_item_cost,
                curr_node.weight + next_item_weight,
                curr_node.bound
            )

            if next_added.weight <= capacity:
                if next_added.cost > best_so_far.cost:
                    best_so_far = next_added

                if next_added.bound > best_so_far.cost:
                    priority_queue.push(next_added)

            next_not_added = Node(curr_node.level + 1, curr_node.selected_items, curr_node.cost,
                                  curr_node.weight, curr_node.bound)
            next_not_added.bound = calculate_bound(next_not_added, number, capacity, weight_cost, ratios)
            if next_not_added.bound > best_so_far.cost:
                priority_queue.push(next_not_added)

    best_combination = [0] * number
    for wc in best_so_far.selected_items:
        best_combination[wc] = 1
    return int(best_so_far.cost), best_combination


def calculate_bound(node, number, capacity, weight_cost, ratios):
    if node.weight >= capacity:
        return 0
    else:
        upper_bound = node.cost
        total_weight = node.weight
        current_level = node.level

        while current_level < number:
            current_index = ratios[current_level][0]

            if total_weight + weight_cost[current_index][0] > capacity:
                cost = weight_cost[current_index][1]
                weight = weight_cost[current_index][0]
                upper_bound += (capacity - total_weight) * cost/weight
                break

            upper_bound += weight_cost[current_index][1]
            total_weight += weight_cost[current_index][0]
            current_level += 1

        return upper_bound
