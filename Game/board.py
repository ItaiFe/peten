import Weapons
import Player


class Board:
    def __init__(self, height, width):
        self.sides = ["red", "blue"]
        self.height = height
        self.width = width
        self.board = [[Weapons.empty] * self.width] * self.height

    def create_board(self):
        for i in range(self.height):
            for j in range(self.width):
                weapon = Weapons.generate_weapon()
                if i != 0 or i != self.height - 1:
                    while weapon == Weapons.flag:
                        weapon = Weapons.generate_weapon()
                # id, location, weapon, side
                if i == 0 or i == 1:
                    self.board[i][j] = Player(
                        self.width * self.height, [i, j], weapon, self.sides[1])
                
                if i == self.height - 2 or i == self.height - 1:
                    self.board[i][j] = Player(
                        self.width * self.height, [i, j], weapon, self.sides[0])

    def move_player(self, id, location):
        pass

    def fight(self):
        pass
