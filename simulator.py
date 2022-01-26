import numpy as np


class treasureHuntSimulator:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.grid=np.zeros(row*col)
        