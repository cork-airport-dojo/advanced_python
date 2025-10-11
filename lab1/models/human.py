from .character import Character

class Human(Character):

    def __init__(self):
        self.health = 15
        self.armor = 13
        self.attack = 3
        self.race = "Human"
