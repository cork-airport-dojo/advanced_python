from models.character import Character

class Dwarf(Character):

    def __init__(self):
        self.race = "Dwarf"
        self.health = 16
        self.attack = 2
        self.armor = 14
