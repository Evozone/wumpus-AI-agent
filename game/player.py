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
        return f"Player(x={self.x}, y={self.y}, has_arrow={self.has_arrow}, has_gold={self.has_gold}, alive={self.alive}, score={self.score})"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_has_arrow(self):
        return self.has_arrow

    def set_has_arrow(self, has_arrow):
        self.has_arrow = has_arrow

    def get_has_gold(self):
        return self.has_gold

    def get_alive(self):
        return self.alive

    def set_alive(self, alive):
        self.alive = alive

    def get_score(self):
        return self.score

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_score(self, score):
        self.score = score
