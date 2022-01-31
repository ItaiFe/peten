from operator import truediv
from re import S, T
import re
from pawn import Pawn
from pawn_types import Pawn_Types
from sides import Sides

RULES = {Pawn_Types.TRAP: [Pawn_Types.SCISSORS, Pawn_Types.ROCK, Pawn_Types.PAPER],
         Pawn_Types.PAPER: [Pawn_Types.ROCK, Pawn_Types.FLAG],
         Pawn_Types.ROCK: [Pawn_Types.SCISSORS, Pawn_Types.FLAG],
         Pawn_Types.SCISSORS: [Pawn_Types.PAPER, Pawn_Types.FLAG],
         Pawn_Types.FLAG: []}

REQUIRED_PAWNS = 14


class Board:
    def __init__(self, height, width):
        self.board = [[Pawn(Pawn_Types.TILE, [i, j])
                       for j in range(width)] for i in range(height)]
        self.height = height
        self.width = width

    def update_board(self, move):
        source = [move[1][0], move[1][1]]
        dest = [move[2][0], move[2][1]]
        self.board[dest[0]][dest[1]].id = self.board[source[0]][source[1]].id
        self.board[dest[0]][dest[1]
                            ].weapon = self.board[source[0]][source[1]].weapon
        self.board[dest[0]][dest[1]
                            ].side = self.board[source[0]][source[1]].side
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
        source = [move[1][0], move[1][1]]
        dest = [move[2][0], move[2][1]]
        if current_player_weapon is None:
            current_player_weapon = self.board[source[0]][source[1]].weapon
        if other_player_weapon is None:
            other_player_weapon = self.board[dest[0]][dest[1]].weapon
        print(current_player_weapon, other_player_weapon)
        if Pawn_Types(other_player_weapon) in RULES[Pawn_Types(current_player_weapon)]:
            self.update_board(move)
            return True
        elif current_player_weapon == other_player_weapon:
            return False
        else:
            self.board[source[0]][source[1]] = (Pawn(location=source))
            return True

    def is_tie(self, move):
        source = [move[1][0], move[1][1]]
        dest = [move[2][0], move[2][1]]
        return self.board[dest[0]][dest[1]].weapon == self.board[source[0]][source[1]].weapon

    def is_fight(self, move):
        dest = [move[2][0], move[2][1]]
        return self.board[dest[0]][dest[1]].side != Sides.NON_PLAYER

    def put_pawn_on_board(self, pawn):
        if self.board[pawn.location[0]][pawn.location[1]].weapon is Pawn_Types.TILE:
            self.board[pawn.location[0]][pawn.location[1]] = pawn

    def is_board_valid(self, side):
        side_pawn_count = 0
        side_flag = False
        for row in self.board:
            for pawn in row:
              
                if side == Sides.PLAYER_A:
                    if pawn.side == side and pawn.weapon != Pawn_Types.TILE and pawn.location[0] > 1:
                        return False
             
                if side == Sides.PLAYER_B:
                    if pawn.side == side and pawn.weapon != Pawn_Types.TILE and pawn.location[0] < self.height - 2:
                        return False
              
                if pawn.side == side:
                    side_pawn_count += 1
            
                if pawn.side == side and pawn.weapon == Pawn_Types.FLAG:
                    side_flag = True

        return side_pawn_count == REQUIRED_PAWNS and side_flag

    def is_move_valid(self, move, side):
        source = [move[1][0], move[1][1]]
        dest = [move[2][0], move[2][1]]

        # Can't move other players pawns
        if not self._check_side(source, side):
            return False

        # Can't move different pawn id from what's on the board
        if not self._check_id(source, move[0]):
            return False

        # Can't move to -1 or over the size of board
        if not self._check_borders(dest):
            return False

        # Can't move illegaly (more specific in function)
        if not self._check_movement(source, dest):
            return False

        # Can't move flag or trap
        if not self._check_illegal_pawns(source):
            return False
        # Can't fight you own pawns
        if not self._own_pawns(source, dest):
            return False

        return True

    def _own_pawns(self, source, dest):
        return self.board[source[0]][source[1]].side != self.board[dest[0]][dest[1]].side

    def _check_side(self, source, side):

        return self.board[source[0]][source[1]].side == side

    def _check_id(self, source, recived_id):

        return recived_id == self.board[source[0]][source[1]].id

    def _check_movement(self, source, dest):

        # Can't move in diagonal
        if source[0] + 1 == dest[0] and source[1] + 1 == dest[1]:
            return False
        if source[0] - 1 == dest[0] and source[1] - 1 == dest[1]:
            return False
        if source[0] - 1 == dest[0] and source[1] + 1 == dest[1]:
            return False
        if source[0] + 1 == dest[0] and source[1] - 1 == dest[1]:
            return False

        # Can't stay in place
        if source[0] == dest[0] and source[1] == dest[1]:
            return False

        # Can't move more than 1 square
        if source[0] + 1 < dest[0] or source[1] + 1 < dest[1]:
            return False

        return True

    def _check_borders(self, dest):
        return dest[0] >= 0 and dest[0] < self.width and dest[1] >= 0 and dest[1] < self.height

    def _check_illegal_pawns(self, source):
        if self.board[source[0]][source[1]].weapon == Pawn_Types.FLAG:
            return False
        if self.board[source[0]][source[1]].weapon == Pawn_Types.TRAP:
            return False
        return True

    def to_serializable(self, side):
        return [[self.board[i][j].to_serilizable(side) for j in range(self.width)] for i in range(self.height)]

    def print_board(self):
        board = ""
        for row in self.board:
            for pawn in row:
                board += " [{weapon}, {side}] ".format(
                    weapon=pawn.weapon, side=pawn.side)
            board += "\n\n"
        print(board)
