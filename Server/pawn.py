from pawn_types import Pawn_Types
from sides import Sides

class Pawn:
    id = 0
    def __init__(self, weapon=None, location=None, side=None):
        self.id = Pawn.id
        self.location = location if location is not None else [0,0]
        self.weapon = weapon if weapon is not None else Pawn_Types.TILE
        self.side = side if weapon is not None else Sides.NON_PLAYER
        Pawn.id += 1
    
    def to_serilizable(self, side):
        weapon = self.weapon if self.side == side else ""
        return [self.id, weapon.value, self.side, self.location]