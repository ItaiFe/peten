import imp
import socket
from board import Board
from pawn_types import Pawn_Types
from player import Player
from sides import Sides
from pawn import Pawn
import random

BOARD_WIDTH = 7
BOARD_HEIGHT = 6


class Game:
    def __init__(self):
        self.players = [Player(Sides.PLAYER_A, "red", 5000),
                        Player(Sides.PLAYER_B, "blue", 5001)]
        self.board = Board(BOARD_HEIGHT, BOARD_WIDTH)
        self.winner = None

    def initialize_player_pawns(self, player):
        try:
            pawns = player.get_initial_lineup()
            for rows in pawns:
                for pawn_data in rows:
                    pawn_type = Pawn_Types(pawn_data[0])
                    pawn = Pawn(
                        pawn_type, pawn_data[1], player.side if pawn_type != Pawn_Types.TILE else Sides.NON_PLAYER)
                    self.board.put_pawn_on_board(pawn)
        except Exception:
            pass
        while not self.board.is_board_valid(player.side):
            self.board.print_board()
            try: 
                pawns = player.get_initial_lineup()
                for rows in pawns:
                    for pawn_data in rows:
                        pawn_type = Pawn_Types(pawn_data[0])
                        pawn = Pawn(
                            pawn_type, pawn_data[1], player.side if pawn_type != Pawn_Types.TILE else Sides.NON_PLAYER)
                        self.board.put_pawn_on_board(pawn)
            except Exception:
                print("Illegal action")

    def initialize_game(self):
        for player in self.players:
            player.start_game()
            self.initialize_player_pawns(player)
        random.shuffle(self.players)

    def run_game(self):
        self.initialize_game()
        self.board.print_board()
        while not self.check_win():
            self.board.print_board()
            for player in self.players:
                try:
                    player.send_board(self.board)
                    move = player.get_next_move()
                    while not self.board.is_move_valid(move, player.side):
                        player.bad_move()
                        move = player.get_next_move()
                    if self.board.is_fight(move):
                        self.fight(move, player.side)

                    else:
                        self.board.update_board(move)
                except Exception:
                    pass

        for player in self.players:
            if player is self.winner:
                player.set_victory(True)
            else:
                player.set_victory(False)

    def fight(self, move, player_side):
        current_player_weapon = None
        other_player_weapon = None
        while not self.board.fight(move, current_player_weapon, other_player_weapon):
            for player in self.players:
                if player.side == player_side:
                    current_player_weapon = player.change_weapon()
                else:
                    other_player_weapon = player.change_weapon()
        

    def check_win(self):
        side_a = self.board.check_flag(self.players[0].side)
        side_b = self.board.check_flag(self.players[1].side)
        if side_a and side_b:
            return False
        if side_a and not side_b:
            self.winner = self.players[0]
            return True
        else:
            self.winner = self.players[1]
            return True


if __name__ == "__main__":
    game = Game()
    game.run_game()
