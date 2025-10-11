import random
from models.character import Character

class Orc(Character):

    def __init__(self):
        self.race = "Orc"
        self.health = 18
        self.attack = 4
        self.armor = 12
    
    def damage_roll(self):
        return self.d8() + self.attack
