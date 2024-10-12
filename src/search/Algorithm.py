import functools
from .Node import Node
from .PriorityQueue import PriorityQueue
from collections import deque


def memoize(fn, slot=None, maxsize=32):

    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn

"""
Implementation of the A* Algorithm in a graph problem
(This will be used when the user asks for help)
"""
def best_first_graph_search(problem, f, display=False):

    f = memoize(f, 'f')
    node = Node(problem.initial)


    if problem.goal_test(node.state):
        return node

    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = deque()

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node.path()
        
        explored.append(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                
                frontier.append(child)

            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def run_algorithm(problem_instance):
    result = astar_search(problem_instance)
    return result
