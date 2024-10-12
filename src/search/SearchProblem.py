def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)

"""
Class Problem (will be extended to fit our case) which will help us define the initial state and the goal
"""
class Problem:

    def __init__(self, initial, goal=None):

        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError
    

"""
The Problem class ajusted to out case
"""
class SearchProblem(Problem):
    def __init__(self, initial, goal, n_rows, n_columns, matrix):
        self.border_left = 0
        self.border_right = n_columns - 1
        self.border_top = 0
        self.border_bottom = n_rows - 1

        self.matrix = matrix

        initial_value = matrix[0][0]
        final_value = matrix[self.border_right][self.border_bottom]

        initial_dict = {"row": initial[0], "column": initial[1], "hardness": initial_value}
        goal_dict = {"row": goal[0], "column": goal[1], "hardness": final_value}

        super().__init__(initial_dict, goal_dict)

    """
    Looks for all possible actions in a given state
    """
    def actions(self, state):
        action_list = []

        if self.border_top < state['row']:
            action_list.append('up')
        if self.border_bottom > state['row']:
            action_list.append('down')
        if self.border_left < state['column']:
            action_list.append('left')
        if self.border_right > state['column']:
            action_list.append('right')
        
        return action_list


    """
    Calculates a new state given the current one and the desired action
    """
    def result(self, state, action):
        new_state = {}

        match action:
            case 'up':
                new_state = dict({'row':state['row'] - 1, 'column': state['column'], 'hardness': self.matrix[state['row']-1][state['column']]})
            case 'down':
                new_state = dict({'row':state['row'] + 1, 'column':state['column'], 'hardness': self.matrix[state['row']+1][state['column']]})
            case 'left':
                new_state = dict({'row':state['row'], 'column':state['column'] - 1, 'hardness': self.matrix[state['row']][state['column']-1]})
            case 'right':
                new_state = dict({'row':state['row'], 'column':state['column'] + 1, 'hardness': self.matrix[state['row']][state['column']+1]})

        return new_state
    

    def goal_test(self, state):
        return state['row'] == self.goal['row'] and state['column'] == self.goal['column']
    

    """
    The cost of the entire path (keep in mind it is the sum of the hardnesses and the heuristics)
    """
    def path_cost(self, c, state1, action, state2):
        hardness_change_cost = 0

        if state1["hardness"] != state2["hardness"]:
            hardness_change_cost = 2

        return c + hardness_change_cost + state2["hardness"]


    """
    The heuristic metric (in this case we use the distance between the initial point and the goal)
    """
    def h(self, node):
        current_row = node.state['row']
        current_column = node.state['column']
        goal_row = self.goal['row']
        goal_column = self.goal['column']

        cost_goal = max(abs(goal_row - current_row), abs(goal_column - current_column))
        return cost_goal
