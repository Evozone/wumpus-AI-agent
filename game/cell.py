# Class for a cell in the cave

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_wumpus = False
        self.has_pit = False
        self.has_gold = False
        self.has_breeze = False
        self.has_stench = False

    def __repr__(self):
        return f"Cell(x={self.x}, y={self.y}, has_wumpus={self.has_wumpus}, has_pit={self.has_pit}, has_gold={self.has_gold})"

    def get_cell_properties(self):
        return {
            "x": self.x,
            "y": self.y,
            "has_wumpus": self.has_wumpus,
            "has_pit": self.has_pit,
            "has_gold": self.has_gold,
            "has_breeze": self.has_breeze,
            "has_stench": self.has_stench,
        }

    def set_wumpus(self):
        self.has_wumpus = True

    def set_pit(self):
        self.has_pit = True

    def set_gold(self):
        self.has_gold = True

    def set_visited(self):
        self.visited = True

    def set_breeze(self):
        self.has_breeze = True

    def set_stench(self):
        self.has_stench = True

    def get_pit(self):
        return self.has_pit

    def get_wumpus(self):
        return self.has_wumpus
