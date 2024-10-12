import numpy as np

"""
Representation of the game in a matrix
"""
class Map:
    def __init__(self, size=5, shape="square"):
        self.generate_square_map(size)

    def generate_square_map(self, size):
        self.n_rows = size
        self.n_columns = size

        m = np.random.randint(1, 5, (self.n_rows, self.n_columns))
        m[0][0] = 1
        self.matrix = m
        self.initial_pos = [0, 0] 
        self.final_pos = [size - 1, size - 1]
        self.generate_key()


    def generate_key(self):
        while True:
            x = np.random.randint(0, self.n_columns)
            y = np.random.randint(0, self.n_rows)
            
            if (x, y) != (0, 0) and (x, y) != (self.n_columns - 1, self.n_rows - 1):
                self.key = (x, y)
                break

    def format_path_coordinates(self, path):
        path_cords = []
        for node in path:
            path_cords.append((node.state["row"], node.state["column"]))
        return path_cords
