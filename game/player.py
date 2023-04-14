# Crete a class for Player and put the move function in it

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_arrow = True
        self.has_gold = False
        self.alive = True
        self.score = 0

    def __repr__(self):
        return f"Player(x={self.x}, y={self.y}, visited={self.visited}, has_wumpus={self.has_wumpus}, has_pit={self.has_pit}, has_gold={self.has_gold})"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
