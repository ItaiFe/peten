import random


class Weapons:
    empty = 0
    rock = 1
    paper = 2
    scissors = 3
    trap = 4
    flag = 5

    def generate_weapon():
        return random.randint(1, 5)
