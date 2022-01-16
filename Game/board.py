import random
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

        if list(filter(self.check_flag, self.board[0])) == []:
            self.board[0][random.randint(0, self.width-1)].weapon = Weapons.flag
        if list(filter(self.check_flag, self.board[self.height - 1])) == []:
            self.board[0][random.randint(0, self.width-1)].weapon = Weapons.flag
            
    def check_flag(player):
        return player.weapon == Weapons.flag

    def move_player(self, id, location):
        for row in self.board:
            for player in row:
                if player.id == id:
                    if self.check_move(player):
                        self.board[player.location[0]][player.location[1]].location = location
                            

    def fight(self, player1, player2):
        if player1.weapon == Weapons.rock:
            if player2.weapon == Weapons.paper:
                return player2
            elif player2.weapon == Weapons.scissors:
                return player1
        elif player1.weapon == Weapons.scissors:
            if player2.weapon == Weapons.rock:
                return player2
            elif player2.weapon == Weapons.paper:
                return player1
        
        elif player1.weapon == Weapons.paper:
            if player2.weapon == Weapons.scissors:
                return player2
            elif player2.weapon == Weapons.rock:
                return player1