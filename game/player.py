# Crete a class for Player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.previous_cells = {
            -1: (-1, -1),
            -2: (-1, -1),
            -3: (-1, -1),
            -4: (-1, -1),
        }
        self.has_arrow = True
        self.has_gold = False
        self.direction = 'east'
        self.alive = True
        self.score = 2000
        self.num_moves = 0

    # Player position
    def get_player_position(self):
        return self.x, self.y

    def set_player_position(self, x, y):
        self.previous_cells[-4] = self.previous_cells[-3]
        self.previous_cells[-3] = self.previous_cells[-2]
        self.previous_cells[-2] = self.previous_cells[-1]
        self.previous_cells[-1] = (self.x, self.y)
        self.x = x
        self.y = y

    def get_previous_position(self, nth_last_move):
        return self.previous_cells[nth_last_move]

    def set_previous_position(self, x, y, nth_last_move=-1):
        self.previous_cells[nth_last_move] = (x, y)

    # Player direction
    def get_player_direction(self):
        return self.direction

    def set_player_direction(self, direction):
        self.direction = direction

    # Player Arrow
    def set_has_arrow(self, has_arrow):
        self.has_arrow = has_arrow

    def get_has_arrow(self):
        return self.has_arrow

    # Player Gold
    def set_has_gold(self, has_gold):
        self.has_gold = has_gold

    def get_has_gold(self):
        return self.has_gold

    # Player Mortality
    def get_alive(self):
        return self.alive

    def set_alive(self, alive):
        self.alive = alive

    # Player Score
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    # Player Number of Moves
    def get_num_moves(self):
        return self.num_moves

    def set_num_moves(self, num_moves):
        self.num_moves = num_moves
