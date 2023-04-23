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
        self.has_visited = False

    def get_cell_properties(self):
        return {
            "x": self.x,
            "y": self.y,
            "has_wumpus": self.has_wumpus,
            "has_pit": self.has_pit,
            "has_gold": self.has_gold,
            "has_breeze": self.has_breeze,
            "has_stench": self.has_stench,
            "has_visited": self.has_visited,
        }

    # Wumpus
    def set_wumpus(self, wumpus):
        self.has_wumpus = wumpus

    def get_wumpus(self):
        return self.has_wumpus

    # Pit
    def set_pit(self):
        self.has_pit = True

    def get_pit(self):
        return self.has_pit

    # Gold
    def set_gold(self, gold):
        self.has_gold = gold

    def get_gold(self):
        return self.has_gold

    # Breeze
    def set_breeze(self):
        self.has_breeze = True

    def get_breeze(self):
        return self.has_breeze

    # Stench
    def set_stench(self, stench):
        self.has_stench = stench

    def get_stench(self):
        return self.has_stench

    # Glitter
    def get_glitter(self):
        return self.has_gold

    # Visited
    def set_visited(self):
        self.has_visited = True

    def get_visited(self):
        return self.has_visited
