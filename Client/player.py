class Player:
    def __init__(self, id, location, weapon, side):
        self.id = id
        self.location = location
        self.weapon = weapon
        self.side = side

    def move(self, location):
        self.location = location
    
    def change_weapon(self, weapon):
        self.weapon = weapon
