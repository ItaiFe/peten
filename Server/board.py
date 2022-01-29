from operator import truediv
from pawn import Pawn
from pawn_types import Pawn_Types
from sides import Sides

RULES = {Pawn_Types.TRAP: [Pawn_Types.SCISSORS, Pawn_Types.ROCK, Pawn_Types.PAPER],
         Pawn_Types.PAPER: [Pawn_Types.ROCK],
         Pawn_Types.ROCK: [Pawn_Types.SCISSORS],
         Pawn_Types.SCISSORS: [Pawn_Types.PAPER],
         Pawn_Types.FLAG: []}

REQUIRED_PAWNS = 14


class Board:
    def __init__(self, height, width):
        self.board = [[Pawn(Pawn_Types.TILE, [i, j])
                       for j in range(width)] for i in range(height)]
        self.height = height
        self.width = width

    def update_board(self, move):
        source = [move[1][0]], [move[1][1]]
        dest = [move[2][0]], [move[2][1]]
        self.board[dest[0]][dest[1]] = self.board[source[0]][source[1]]
        self.board[source[0]][source[1]] = Pawn(
            Pawn_Types.TILE, source, Sides.NON_PLAYER)

    def check_flag(self, side):
        side_flag = False
        for row in self.board:
            for pawn in row:
                if pawn.side == side and pawn.weapon == Pawn_Types.FLAG:
                    side_flag = True

        return side_flag

    def fight(self, move, current_player_weapon, other_player_weapon):
        source = [move[1][0]], [move[1][1]]
        if current_player_weapon in RULES[other_player_weapon]:
            self.update_board(move)
        else:
            self.put_pawn_on_board(Pawn(location=source))

    def is_tie(self, move):
        source = [move[1][0]], [move[1][1]]
        dest = [move[2][0]], [move[2][1]]
        return self.board[dest[0]][dest[1]].weapon == self.board[source[0]][source[1]].weapon

    def is_fight(self, move):
        dest = [move[2][0]], [move[2][1]]
        return self.board[dest[0]][dest[1]].side != Sides.NON_PLAYER

    def put_pawn_on_board(self, pawn):
        self.board[pawn.location[0]][pawn.location[1]] = pawn

    def is_board_valid(self, side):
        side_pawn_count = 0
        side_flag = False
        for row in self.board:
            for pawn in row:
                if side == Sides.PLAYER_A:
                    if pawn.weapon != Pawn_Types.TILE and pawn.location[0] > 1:
                        return False
                if side == Sides.PLAYER_B:
                    if pawn.weapon != Pawn_Types.TILE and pawn.location[0] < self.height - 2:
                        return False
                if pawn.side == side:
                    side_pawn_count += 1
                if pawn.side == side and pawn.weapon == Pawn_Types.FLAG:
                    side_flag = True
        print(side_pawn_count)
        return side_pawn_count == REQUIRED_PAWNS and side_flag

    def is_move_valid(self, move):
        if not move[0] == self.board[move[1][0]][move[1][1]].id:
            return False
        if move[1][0] + 1 != move[2][0] or move[1][0] - 1 != move[2][0]:
            return False
        if move[1][1] + 1 != move[2][1] or move[1][1] - 1 != move[2][1]:
            return False
        if move[2][0] >= self.height or move[2][1] >= self.width:
            return False
        if move[2][0] < 0 or move[2][1] < 0:
            return False
        if self.board[move[1][0]][move[1][1]].side == self.board[move[2][0]][move[2][1]].side:
            return False
        return True

    def to_serializable(self):
        return [[self.board[i][j].to_serilizable(self.board[i][j].side) for j in range(self.width)] for i in range(self.height)]

    def print_board(self):
        board = ""
        for row in self.board:
            for pawn in row:
                board += " [{weapon}] ".format(weapon=pawn.weapon)
            board += "\n\n"
        print(board)
